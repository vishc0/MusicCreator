"""
Tests for the style analyzer module.
"""

import pytest
from src.analysis.analyzer import StyleAnalyzer


def test_analyzer_initialization():
    """Test that analyzer can be initialized."""
    analyzer = StyleAnalyzer()
    assert analyzer is not None


def test_analyzer_with_config():
    """Test analyzer initialization with config."""
    config = {
        'model': 'test-model',
        'temperature': 0.5,
        'cache': {'enabled': False}
    }
    analyzer = StyleAnalyzer(config)
    assert analyzer.model == 'test-model'
    assert analyzer.temperature == 0.5


def test_infer_harmonic_style():
    """Test harmonic style inference."""
    analyzer = StyleAnalyzer()
    
    baroque_style = analyzer._infer_harmonic_style('Baroque')
    assert 'progressions' in baroque_style
    assert baroque_style['chromaticism'] == 'low'
    
    romantic_style = analyzer._infer_harmonic_style('Romantic')
    assert romantic_style['chromaticism'] == 'high'


def test_analyze_with_fallback(sample_composer_data):
    """Test analysis with fallback (no API key)."""
    analyzer = StyleAnalyzer({'cache': {'enabled': False}})
    
    style_profile = analyzer.analyze(sample_composer_data)
    
    assert style_profile is not None
    assert 'composer' in style_profile
    assert style_profile['composer'] == 'Edvard Grieg'
    assert 'harmonic_style' in style_profile
    assert 'melodic_style' in style_profile
