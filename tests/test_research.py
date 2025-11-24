"""
Tests for the composer researcher module.
"""

import pytest
from src.research.researcher import ComposerResearcher


def test_researcher_initialization():
    """Test that researcher can be initialized."""
    researcher = ComposerResearcher()
    assert researcher is not None


def test_researcher_with_config():
    """Test researcher initialization with config."""
    config = {
        'cache': {
            'enabled': False
        }
    }
    researcher = ComposerResearcher(config)
    assert researcher.cache_enabled is False


def test_sanitize_filename():
    """Test filename sanitization."""
    researcher = ComposerResearcher()
    
    assert researcher._sanitize_filename("Edvard Grieg") == "Edvard_Grieg"
    assert researcher._sanitize_filename("J.S. Bach") == "JS_Bach"
    assert researcher._sanitize_filename("Mozart!!!") == "Mozart"


def test_research_basic(sample_composer_data):
    """Test basic research functionality."""
    researcher = ComposerResearcher({'cache': {'enabled': False}})
    
    # This will make actual API calls in a real scenario
    # For testing, we might want to mock the responses
    result = researcher.research("Edvard Grieg")
    
    assert result is not None
    assert 'name' in result
    assert result['name'] == "Edvard Grieg"
