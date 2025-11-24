"""
Music Generator - Generates original compositions based on style profiles.
"""

import logging
import random
from typing import Dict, Any, List, Optional
from music21 import stream, note, chord, meter, key, tempo, clef

logger = logging.getLogger(__name__)


class MusicGenerator:
    """Generates music compositions based on style profiles."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the generator with configuration."""
        self.config = config or {}
        self.num_compositions = self.config.get('num_compositions', 5)
        self.length_measures = self.config.get('length_measures', 32)
        self.temperature = self.config.get('temperature', 0.8)
    
    def generate(self, style_profile: Dict[str, Any], num_compositions: Optional[int] = None) -> List[stream.Score]:
        """
        Generate compositions based on style profile.
        
        Args:
            style_profile: Style profile from analyzer
            num_compositions: Number of compositions to generate (overrides config)
            
        Returns:
            List of music21 Score objects
        """
        num = num_compositions or self.num_compositions
        logger.info(f"Generating {num} compositions")
        
        compositions = []
        for i in range(num):
            logger.debug(f"Generating composition {i+1}/{num}")
            composition = self._generate_single_composition(style_profile, seed=i)
            compositions.append(composition)
        
        return compositions
    
    def _generate_single_composition(self, style_profile: Dict[str, Any], seed: int = 0) -> stream.Score:
        """Generate a single composition."""
        # Set random seed for reproducibility with variation
        random.seed(seed)
        
        # Create a score
        score = stream.Score()
        
        # Add metadata
        score.metadata = self._create_metadata(style_profile)
        
        # Create a part (piano for simplicity)
        part = stream.Part()
        part.insert(0, clef.TrebleClef())
        
        # Set time signature
        time_sigs = style_profile.get('rhythmic_style', {}).get('time_signatures', ['4/4'])
        time_sig_str = random.choice(time_sigs)
        numerator, denominator = map(int, time_sig_str.split('/'))
        part.insert(0, meter.TimeSignature(f'{numerator}/{denominator}'))
        
        # Set key
        composition_key = self._choose_key(style_profile)
        part.insert(0, key.Key(composition_key))
        
        # Set tempo
        bpm = self._choose_tempo(style_profile)
        part.insert(0, tempo.MetronomeMark(number=bpm))
        
        # Generate measures
        measures = self._generate_measures(style_profile, self.length_measures, numerator, denominator)
        for measure in measures:
            part.append(measure)
        
        # Add part to score
        score.insert(0, part)
        
        return score
    
    def _create_metadata(self, style_profile: Dict[str, Any]) -> Any:
        """Create metadata for the composition."""
        from music21 import metadata
        
        md = metadata.Metadata()
        md.title = f"Composition in the style of {style_profile.get('composer', 'Unknown')}"
        md.composer = f"AI (style: {style_profile.get('composer', 'Unknown')})"
        
        return md
    
    def _choose_key(self, style_profile: Dict[str, Any]) -> str:
        """Choose an appropriate key for the composition."""
        # Common keys for different eras
        era = style_profile.get('era', 'Classical')
        
        keys = {
            'Baroque': ['C', 'G', 'D', 'A', 'F', 'Bb', 'a', 'd', 'e'],
            'Classical': ['C', 'G', 'D', 'F', 'Bb', 'Eb', 'a', 'd', 'g'],
            'Romantic': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B', 'c#', 'f#', 'b'],
            'Impressionist': ['C', 'Db', 'D', 'Eb', 'E', 'F#', 'Ab', 'Bb', 'c', 'c#', 'f#']
        }
        
        available_keys = keys.get(era, keys['Classical'])
        return random.choice(available_keys)
    
    def _choose_tempo(self, style_profile: Dict[str, Any]) -> int:
        """Choose an appropriate tempo."""
        era = style_profile.get('era', 'Classical')
        
        tempos = {
            'Baroque': (100, 120),
            'Classical': (90, 120),
            'Romantic': (60, 140),
            'Impressionist': (70, 100)
        }
        
        tempo_range = tempos.get(era, (90, 120))
        return random.randint(*tempo_range)
    
    def _generate_measures(
        self,
        style_profile: Dict[str, Any],
        num_measures: int,
        time_sig_num: int,
        time_sig_denom: int
    ) -> List[stream.Measure]:
        """Generate musical measures."""
        measures = []
        current_pitch = 60  # Middle C
        
        for i in range(num_measures):
            measure = stream.Measure(number=i + 1)
            
            # Generate notes for this measure
            beats_left = time_sig_num
            
            while beats_left > 0:
                # Choose note duration
                duration = self._choose_duration(beats_left, style_profile)
                
                # Choose whether to use a note or chord
                if random.random() < 0.3:  # 30% chance of chord
                    musical_element = self._create_chord(current_pitch, duration, style_profile)
                else:
                    # Choose pitch (with random walk)
                    current_pitch = self._choose_next_pitch(current_pitch, style_profile)
                    musical_element = note.Note(current_pitch, quarterLength=duration)
                
                measure.append(musical_element)
                beats_left -= duration
            
            measures.append(measure)
        
        return measures
    
    def _choose_duration(self, beats_left: float, style_profile: Dict[str, Any]) -> float:
        """Choose a note duration."""
        # Common durations based on beats left
        possible_durations = []
        
        if beats_left >= 4.0:
            possible_durations.extend([4.0, 2.0, 1.0, 0.5])
        elif beats_left >= 2.0:
            possible_durations.extend([2.0, 1.0, 0.5])
        elif beats_left >= 1.0:
            possible_durations.extend([1.0, 0.5])
        else:
            possible_durations.append(beats_left)
        
        return random.choice(possible_durations)
    
    def _choose_next_pitch(self, current_pitch: int, style_profile: Dict[str, Any]) -> int:
        """Choose the next pitch using a random walk."""
        melodic_style = style_profile.get('melodic_style', {})
        range_type = melodic_style.get('range', 'moderate')
        
        # Define step range based on melodic style
        if range_type == 'narrow':
            max_step = 3  # Up to minor third
        elif range_type == 'wide':
            max_step = 12  # Up to octave
        else:
            max_step = 7  # Up to fifth
        
        # Random walk with preference for smaller intervals
        step = random.choices(
            range(-max_step, max_step + 1),
            weights=[1 / (abs(i) + 1) for i in range(-max_step, max_step + 1)]
        )[0]
        
        new_pitch = current_pitch + step
        
        # Keep within reasonable range (C3 to C6)
        new_pitch = max(48, min(84, new_pitch))
        
        return new_pitch
    
    def _create_chord(self, root_pitch: int, duration: float, style_profile: Dict[str, Any]) -> chord.Chord:
        """Create a chord."""
        # Simple triads for now
        chord_types = ['major', 'minor']
        chord_type = random.choice(chord_types)
        
        if chord_type == 'major':
            intervals = [0, 4, 7]  # Major triad
        else:
            intervals = [0, 3, 7]  # Minor triad
        
        pitches = [root_pitch + interval for interval in intervals]
        return chord.Chord(pitches, quarterLength=duration)
