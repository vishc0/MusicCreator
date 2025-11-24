"""
Style Analyzer - Uses LLMs to analyze and understand composer's musical style.
"""

import logging
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)


class StyleAnalyzer:
    """Analyzes composer style using LLMs."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the analyzer with configuration."""
        self.config = config or {}
        self.model = self.config.get('model', 'mistralai/Mistral-7B-Instruct-v0.2')
        self.temperature = self.config.get('temperature', 0.7)
        self.max_tokens = self.config.get('max_tokens', 2000)
        self.cache_enabled = self.config.get('cache', {}).get('enabled', True)
        self.cache_dir = Path(self.config.get('cache', {}).get('directory', '.cache/analysis'))
        
        # Get API key from environment
        self.api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not self.api_key:
            logger.warning("HUGGINGFACE_API_KEY not set. Style analysis will use fallback data.")
        
        if self.cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze(self, composer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a composer's style using LLMs.
        
        Args:
            composer_data: Information about the composer
            
        Returns:
            Dictionary with style profile
        """
        composer_name = composer_data.get('name', 'Unknown')
        
        # Check cache first
        if self.cache_enabled:
            cached_profile = self._load_from_cache(composer_name)
            if cached_profile:
                logger.info(f"Loaded cached style profile for {composer_name}")
                return cached_profile
        
        logger.info(f"Analyzing style for {composer_name}")
        
        # If no API key, use fallback
        if not self.api_key:
            return self._get_fallback_style(composer_data)
        
        # Create prompt for LLM
        prompt = self._create_analysis_prompt(composer_data)
        
        # Call LLM
        try:
            analysis_text = self._call_llm(prompt)
            style_profile = self._parse_analysis(analysis_text, composer_data)
        except Exception as e:
            logger.warning(f"LLM analysis failed: {e}. Using fallback.")
            style_profile = self._get_fallback_style(composer_data)
        
        # Save to cache
        if self.cache_enabled:
            self._save_to_cache(composer_name, style_profile)
        
        return style_profile
    
    def _create_analysis_prompt(self, composer_data: Dict[str, Any]) -> str:
        """Create a prompt for the LLM to analyze composer style."""
        composer_name = composer_data.get('name', 'Unknown')
        era = composer_data.get('era', 'Unknown')
        biography = composer_data.get('biography', 'No biography available.')
        
        prompt = f"""You are a music theory expert. Analyze the compositional style of {composer_name}.

Composer Information:
- Name: {composer_name}
- Era: {era}
- Biography: {biography}

Please provide a detailed analysis of this composer's musical style including:

1. Harmonic Style:
   - Common chord progressions
   - Chromaticism level (none/low/moderate/high)
   - Modulation patterns
   - Typical cadences

2. Melodic Style:
   - Melodic contour (ascending/descending/arch-shaped/wave-like)
   - Range (narrow/moderate/wide)
   - Ornamentation style
   - Characteristic intervals

3. Rhythmic Style:
   - Typical time signatures
   - Rhythmic complexity (simple/moderate/complex)
   - Common rhythmic patterns
   - Use of syncopation

4. Formal Structure:
   - Preferred forms (sonata, rondo, variation, etc.)
   - Typical movement structures
   - Sectional organization

5. Instrumentation:
   - Preferred instruments
   - Orchestration style
   - Texture (monophonic/homophonic/polyphonic)

Provide your analysis in a structured format."""

        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call the Hugging Face Inference API."""
        api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_tokens,
                "return_full_text": False
            }
        }
        
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '')
        
        return str(result)
    
    def _parse_analysis(self, analysis_text: str, composer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the LLM's analysis into a structured format."""
        # For now, we'll create a structured profile
        # In a more sophisticated version, we could parse the LLM output
        
        era = composer_data.get('era', 'Unknown')
        
        # Build style profile with reasonable defaults based on era
        style_profile = {
            'composer': composer_data.get('name'),
            'era': era,
            'analysis_text': analysis_text,
            'harmonic_style': self._infer_harmonic_style(era),
            'melodic_style': self._infer_melodic_style(era),
            'rhythmic_style': self._infer_rhythmic_style(era),
            'formal_style': self._infer_formal_style(era),
            'instrumentation': self._infer_instrumentation(era)
        }
        
        return style_profile
    
    def _get_fallback_style(self, composer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get a fallback style profile when LLM is not available."""
        era = composer_data.get('era', 'Unknown')
        
        return {
            'composer': composer_data.get('name'),
            'era': era,
            'harmonic_style': self._infer_harmonic_style(era),
            'melodic_style': self._infer_melodic_style(era),
            'rhythmic_style': self._infer_rhythmic_style(era),
            'formal_style': self._infer_formal_style(era),
            'instrumentation': self._infer_instrumentation(era)
        }
    
    def _infer_harmonic_style(self, era: str) -> Dict[str, Any]:
        """Infer harmonic style from era."""
        styles = {
            'Baroque': {
                'progressions': ['I-IV-V-I', 'I-V-vi-IV'],
                'chromaticism': 'low',
                'modulation': 'frequent to related keys'
            },
            'Classical': {
                'progressions': ['I-IV-V-I', 'I-V-I', 'ii-V-I'],
                'chromaticism': 'low',
                'modulation': 'to dominant and relative keys'
            },
            'Romantic': {
                'progressions': ['I-IV-V-I', 'vi-IV-I-V', 'ii-V-I'],
                'chromaticism': 'high',
                'modulation': 'frequent and distant'
            },
            'Impressionist': {
                'progressions': ['parallel chords', 'whole tone scales'],
                'chromaticism': 'very high',
                'modulation': 'ambiguous tonality'
            }
        }
        return styles.get(era, styles['Classical'])
    
    def _infer_melodic_style(self, era: str) -> Dict[str, Any]:
        """Infer melodic style from era."""
        styles = {
            'Baroque': {'contour': 'sequential', 'range': 'moderate', 'ornamentation': 'trills and mordents'},
            'Classical': {'contour': 'balanced', 'range': 'moderate', 'ornamentation': 'minimal'},
            'Romantic': {'contour': 'expressive', 'range': 'wide', 'ornamentation': 'lyrical'},
            'Impressionist': {'contour': 'floating', 'range': 'wide', 'ornamentation': 'coloristic'}
        }
        return styles.get(era, styles['Classical'])
    
    def _infer_rhythmic_style(self, era: str) -> Dict[str, Any]:
        """Infer rhythmic style from era."""
        styles = {
            'Baroque': {'time_signatures': ['4/4', '3/4', '2/4'], 'complexity': 'moderate'},
            'Classical': {'time_signatures': ['4/4', '3/4'], 'complexity': 'simple'},
            'Romantic': {'time_signatures': ['4/4', '3/4', '6/8'], 'complexity': 'complex'},
            'Impressionist': {'time_signatures': ['4/4', '3/4', '5/4'], 'complexity': 'complex'}
        }
        return styles.get(era, styles['Classical'])
    
    def _infer_formal_style(self, era: str) -> Dict[str, Any]:
        """Infer formal style from era."""
        styles = {
            'Baroque': {'forms': ['fugue', 'suite', 'concerto grosso']},
            'Classical': {'forms': ['sonata', 'symphony', 'string quartet']},
            'Romantic': {'forms': ['symphonic poem', 'art song', 'character piece']},
            'Impressionist': {'forms': ['prelude', 'nocturne', 'free form']}
        }
        return styles.get(era, styles['Classical'])
    
    def _infer_instrumentation(self, era: str) -> Dict[str, Any]:
        """Infer instrumentation preferences from era."""
        styles = {
            'Baroque': {'instruments': ['harpsichord', 'strings', 'winds'], 'texture': 'polyphonic'},
            'Classical': {'instruments': ['piano', 'strings', 'winds'], 'texture': 'homophonic'},
            'Romantic': {'instruments': ['piano', 'full orchestra'], 'texture': 'rich homophonic'},
            'Impressionist': {'instruments': ['piano', 'woodwinds', 'harp'], 'texture': 'coloristic'}
        }
        return styles.get(era, styles['Classical'])
    
    def _load_from_cache(self, composer_name: str) -> Optional[Dict[str, Any]]:
        """Load style profile from cache."""
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
        """Save style profile to cache."""
        cache_file = self.cache_dir / f"{self._sanitize_filename(composer_name)}.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string to be used as a filename."""
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')
