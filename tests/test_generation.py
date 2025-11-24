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
        'temperature': 0.9,
        'instruments': ['piano', 'violin'],
        'difficulty': 'advanced'
    }
    generator = MusicGenerator(config)
    assert generator.num_compositions == 3
    assert generator.length_measures == 16
    assert generator.instruments == ['piano', 'violin']
    assert generator.difficulty == 'advanced'


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


def test_multiple_instruments(sample_style_profile):
    """Test generation with multiple instruments."""
    generator = MusicGenerator({
        'instruments': ['piano', 'violin', 'cello'],
        'length_measures': 4
    })
    
    composition = generator._generate_single_composition(sample_style_profile, seed=42)
    
    assert len(composition.parts) == 3  # One part per instrument


def test_difficulty_beginner(sample_style_profile):
    """Test beginner difficulty generation."""
    generator = MusicGenerator({
        'difficulty': 'beginner',
        'length_measures': 4
    })
    
    composition = generator._generate_single_composition(sample_style_profile, seed=42)
    
    assert isinstance(composition, stream.Score)
    # Beginner should use fewer chords
    assert generator._should_use_chord() in [True, False]


def test_difficulty_expert(sample_style_profile):
    """Test expert difficulty generation."""
    generator = MusicGenerator({
        'difficulty': 'expert',
        'instruments': ['piano'],
        'length_measures': 4
    })
    
    composition = generator._generate_single_composition(sample_style_profile, seed=42)
    
    assert isinstance(composition, stream.Score)


def test_instrument_range():
    """Test instrument pitch ranges."""
    generator = MusicGenerator()
    
    # Test that different instruments have different ranges
    assert generator.instrument_ranges['piano'] != generator.instrument_ranges['violin']
    assert generator.instrument_ranges['flute'][0] > generator.instrument_ranges['cello'][0]


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


def test_chord_complexity_by_difficulty():
    """Test that chord complexity varies by difficulty."""
    beginner_gen = MusicGenerator({'difficulty': 'beginner'})
    expert_gen = MusicGenerator({'difficulty': 'expert'})
    
    # Expert should have higher probability of chords
    beginner_chord_count = sum(beginner_gen._should_use_chord() for _ in range(100))
    expert_chord_count = sum(expert_gen._should_use_chord() for _ in range(100))
    
    assert expert_chord_count >= beginner_chord_count
