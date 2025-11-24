"""
Tests for the music generator module.
"""

import pytest
from src.generation.generator import MusicGenerator
from music21 import stream


def test_generator_initialization():
    """Test that generator can be initialized."""
    generator = MusicGenerator()
    assert generator is not None


def test_generator_with_config():
    """Test generator initialization with config."""
    config = {
        'num_compositions': 3,
        'length_measures': 16,
        'temperature': 0.9
    }
    generator = MusicGenerator(config)
    assert generator.num_compositions == 3
    assert generator.length_measures == 16


def test_generate_compositions(sample_style_profile):
    """Test composition generation."""
    generator = MusicGenerator({'num_compositions': 2, 'length_measures': 8})
    
    compositions = generator.generate(sample_style_profile)
    
    assert len(compositions) == 2
    assert all(isinstance(comp, stream.Score) for comp in compositions)


def test_single_composition(sample_style_profile):
    """Test single composition generation."""
    generator = MusicGenerator({'length_measures': 4})
    
    composition = generator._generate_single_composition(sample_style_profile, seed=42)
    
    assert isinstance(composition, stream.Score)
    assert composition.metadata is not None
    assert len(composition.parts) > 0


def test_choose_key():
    """Test key selection."""
    generator = MusicGenerator()
    
    romantic_profile = {'era': 'Romantic'}
    key = generator._choose_key(romantic_profile)
    
    assert isinstance(key, str)
    assert len(key) > 0


def test_choose_tempo():
    """Test tempo selection."""
    generator = MusicGenerator()
    
    classical_profile = {'era': 'Classical'}
    tempo = generator._choose_tempo(classical_profile)
    
    assert isinstance(tempo, int)
    assert 60 <= tempo <= 200
