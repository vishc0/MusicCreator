"""
Test configuration and utilities.
"""

import pytest
from pathlib import Path


@pytest.fixture
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_composer_data():
    """Provide sample composer data for testing."""
    return {
        'name': 'Edvard Grieg',
        'era': 'Romantic',
        'birth_year': 1843,
        'death_year': 1907,
        'nationality': 'Norwegian',
        'influences': ['Norwegian folk music', 'Robert Schumann'],
        'characteristics': ['Lyrical melodies', 'National romanticism'],
        'notable_works': ['Peer Gynt', 'Piano Concerto in A minor'],
        'biography': 'Edvard Grieg was a Norwegian composer and pianist.'
    }


@pytest.fixture
def sample_style_profile():
    """Provide sample style profile for testing."""
    return {
        'composer': 'Edvard Grieg',
        'era': 'Romantic',
        'harmonic_style': {
            'progressions': ['I-IV-V-I', 'vi-IV-I-V'],
            'chromaticism': 'high',
            'modulation': 'frequent and distant'
        },
        'melodic_style': {
            'contour': 'expressive',
            'range': 'wide',
            'ornamentation': 'lyrical'
        },
        'rhythmic_style': {
            'time_signatures': ['4/4', '3/4', '6/8'],
            'complexity': 'complex'
        },
        'formal_style': {
            'forms': ['symphonic poem', 'art song', 'character piece']
        },
        'instrumentation': {
            'instruments': ['piano', 'full orchestra'],
            'texture': 'rich homophonic'
        }
    }
