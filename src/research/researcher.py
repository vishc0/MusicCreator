"""
Composer Researcher - Gathers information about composers from various sources.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ComposerResearcher:
    """Researches composers using web scraping and APIs."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the researcher with configuration."""
        self.config = config or {}
        self.cache_enabled = self.config.get('cache', {}).get('enabled', True)
        self.cache_dir = Path(self.config.get('cache', {}).get('directory', '.cache/research'))
        
        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def research(self, composer_name: str) -> Dict[str, Any]:
        """
        Research a composer and return structured information.
        
        Args:
            composer_name: Name of the composer to research
            
        Returns:
            Dictionary with composer information
        """
        # Check cache first
        if self.cache_enabled:
            cached_data = self._load_from_cache(composer_name)
            if cached_data:
                logger.info(f"Loaded cached data for {composer_name}")
                return cached_data
        
        logger.info(f"Researching composer: {composer_name}")
        
        # Gather data from various sources
        composer_data = {
            'name': composer_name,
            'era': None,
            'birth_year': None,
            'death_year': None,
            'nationality': None,
            'influences': [],
            'characteristics': [],
            'notable_works': [],
            'biography': None
        }
        
        # Try to get Wikipedia data
        try:
            wiki_data = self._fetch_wikipedia(composer_name)
            composer_data.update(wiki_data)
        except Exception as e:
            logger.warning(f"Failed to fetch Wikipedia data: {e}")
        
        # Try to get IMSLP data
        try:
            imslp_data = self._fetch_imslp(composer_name)
            composer_data['notable_works'].extend(imslp_data.get('works', []))
        except Exception as e:
            logger.warning(f"Failed to fetch IMSLP data: {e}")
        
        # Save to cache
        if self.cache_enabled:
            self._save_to_cache(composer_name, composer_data)
        
        return composer_data
    
    def _fetch_wikipedia(self, composer_name: str) -> Dict[str, Any]:
        """Fetch composer information from Wikipedia."""
        # Use Wikipedia API
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            'action': 'opensearch',
            'search': composer_name,
            'limit': 1,
            'namespace': 0,
            'format': 'json'
        }
        
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json()
        
        if not results[1]:  # No results found
            logger.warning(f"No Wikipedia article found for {composer_name}")
            return {}
        
        article_title = results[1][0]
        article_url = results[3][0]
        
        # Get article content
        content_params = {
            'action': 'query',
            'titles': article_title,
            'prop': 'extracts|categories',
            'exintro': True,
            'explaintext': True,
            'format': 'json'
        }
        
        content_response = requests.get(search_url, params=content_params, timeout=10)
        content_response.raise_for_status()
        data = content_response.json()
        
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        extract = pages[page_id].get('extract', '')
        
        # Parse the extract for basic info
        info = self._parse_wikipedia_extract(extract)
        info['source_url'] = article_url
        
        return info
    
    def _parse_wikipedia_extract(self, extract: str) -> Dict[str, Any]:
        """Parse Wikipedia extract for composer information."""
        info = {}
        
        # Try to extract birth/death years (format: "1843-1907")
        import re
        year_pattern = r'\b(\d{4})\s*[-–]\s*(\d{4})\b'
        match = re.search(year_pattern, extract)
        if match:
            info['birth_year'] = int(match.group(1))
            info['death_year'] = int(match.group(2))
        
        # Store biography excerpt
        # Take first 500 characters
        info['biography'] = extract[:500] + '...' if len(extract) > 500 else extract
        
        # Detect era from common keywords
        extract_lower = extract.lower()
        if 'baroque' in extract_lower:
            info['era'] = 'Baroque'
        elif 'classical' in extract_lower and 'romantic' not in extract_lower:
            info['era'] = 'Classical'
        elif 'romantic' in extract_lower:
            info['era'] = 'Romantic'
        elif 'modern' in extract_lower or 'contemporary' in extract_lower:
            info['era'] = 'Modern'
        elif 'renaissance' in extract_lower:
            info['era'] = 'Renaissance'
        elif 'impressionist' in extract_lower:
            info['era'] = 'Impressionist'
        
        return info
    
    def _fetch_imslp(self, composer_name: str) -> Dict[str, Any]:
        """Fetch composer works from IMSLP (International Music Score Library Project)."""
        # Note: IMSLP doesn't have a free API, so we'll simulate this for now
        # In a real implementation, you could scrape the IMSLP website carefully
        # respecting their robots.txt and rate limits
        
        logger.debug(f"IMSLP lookup for {composer_name} (placeholder)")
        return {'works': []}
    
    def _load_from_cache(self, composer_name: str) -> Optional[Dict[str, Any]]:
        """Load composer data from cache."""
        cache_file = self.cache_dir / f"{self._sanitize_filename(composer_name)}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            return None
    
    def _save_to_cache(self, composer_name: str, data: Dict[str, Any]) -> None:
        """Save composer data to cache."""
        cache_file = self.cache_dir / f"{self._sanitize_filename(composer_name)}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string to be used as a filename."""
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
