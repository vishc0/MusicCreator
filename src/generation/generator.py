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
        self.instruments = self.config.get('instruments', ['piano'])
        self.difficulty = self.config.get('difficulty', 'intermediate')
        
        # Advanced options
        self.mood = self.config.get('mood', None)
        self.time_signature_override = self.config.get('time_signature', None)
        self.key_override = self.config.get('key', None)
        self.tempo_override = self.config.get('tempo', None)
        
        # Mood to musical characteristics mapping
        self.mood_characteristics = {
            'happy': {
                'prefer_major': True,
                'tempo_modifier': 1.2,  # Faster
                'rhythm_complexity': 'simple',
                'dynamics': 'forte'
            },
            'sad': {
                'prefer_major': False,
                'tempo_modifier': 0.7,  # Slower
                'rhythm_complexity': 'simple',
                'dynamics': 'piano'
            },
            'melancholic': {
                'prefer_major': False,
                'tempo_modifier': 0.8,
                'rhythm_complexity': 'moderate',
                'dynamics': 'mezzo-piano'
            },
            'dramatic': {
                'prefer_major': None,  # Can be either
                'tempo_modifier': 1.3,
                'rhythm_complexity': 'complex',
                'dynamics': 'fortissimo'
            },
            'peaceful': {
                'prefer_major': True,
                'tempo_modifier': 0.7,
                'rhythm_complexity': 'simple',
                'dynamics': 'pianissimo'
            },
            'energetic': {
                'prefer_major': True,
                'tempo_modifier': 1.4,
                'rhythm_complexity': 'complex',
                'dynamics': 'forte'
            },
            'mysterious': {
                'prefer_major': False,
                'tempo_modifier': 0.9,
                'rhythm_complexity': 'moderate',
                'dynamics': 'piano'
            },
            'triumphant': {
                'prefer_major': True,
                'tempo_modifier': 1.1,
                'rhythm_complexity': 'complex',
                'dynamics': 'fortissimo'
            },
            'romantic': {
                'prefer_major': True,
                'tempo_modifier': 0.85,
                'rhythm_complexity': 'moderate',
                'dynamics': 'mezzo-forte'
            },
            'playful': {
                'prefer_major': True,
                'tempo_modifier': 1.25,
                'rhythm_complexity': 'moderate',
                'dynamics': 'mezzo-forte'
            }
        }
        
        # Instrument to clef mapping
        self.instrument_clefs = {
            'piano': [clef.TrebleClef(), clef.BassClef()],
            'violin': [clef.TrebleClef()],
            'viola': [clef.AltoClef()],
            'cello': [clef.BassClef()],
            'flute': [clef.TrebleClef()],
            'clarinet': [clef.TrebleClef()],
            'oboe': [clef.TrebleClef()],
            'bassoon': [clef.BassClef()],
            'trumpet': [clef.TrebleClef()],
            'trombone': [clef.BassClef()],
            'french horn': [clef.TrebleClef()],
            'tuba': [clef.BassClef()],
            'guitar': [clef.TrebleClef()],
            'harp': [clef.TrebleClef(), clef.BassClef()],
            'voice': [clef.TrebleClef()],
            'soprano': [clef.TrebleClef()],
            'alto': [clef.TrebleClef()],
            'tenor': [clef.Treble8vbClef()],
            'bass': [clef.BassClef()],
        }
        
        # Instrument pitch ranges (MIDI note numbers)
        self.instrument_ranges = {
            'piano': (21, 108),      # A0 to C8
            'violin': (55, 103),     # G3 to G7
            'viola': (48, 84),       # C3 to C6
            'cello': (36, 72),       # C2 to C5
            'flute': (60, 96),       # C4 to C7
            'clarinet': (50, 91),    # D3 to G6
            'oboe': (58, 91),        # Bb3 to G6
            'bassoon': (34, 67),     # Bb1 to G4
            'trumpet': (55, 82),     # G3 to Bb5
            'trombone': (40, 72),    # E2 to C5
            'french horn': (41, 77), # F2 to F5
            'tuba': (28, 58),        # E1 to Bb3
            'guitar': (40, 83),      # E2 to B5
            'harp': (23, 103),       # B0 to G7
            'voice': (48, 79),       # C3 to G5
            'soprano': (60, 84),     # C4 to C6
            'alto': (55, 79),        # G3 to G5
            'tenor': (48, 72),       # C3 to C5
            'bass': (40, 64),        # E2 to E4
        }
    
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
        
        # Set time signature (use override if provided, otherwise from style)
        if self.time_signature_override:
            time_sig_str = self.time_signature_override
        else:
            time_sigs = style_profile.get('rhythmic_style', {}).get('time_signatures', ['4/4'])
            time_sig_str = random.choice(time_sigs)
        
        numerator, denominator = map(int, time_sig_str.split('/'))
        
        # Set key (use override if provided, otherwise choose from style)
        if self.key_override and self.key_override != 'auto':
            composition_key = self.key_override
        else:
            composition_key = self._choose_key(style_profile)
        
        # Set tempo (use override if provided, otherwise choose from style and mood)
        if self.tempo_override:
            bpm = self.tempo_override
        else:
            bpm = self._choose_tempo(style_profile)
        
        # Create parts for each instrument
        for instrument_name in self.instruments:
            part = self._create_instrument_part(
                instrument_name,
                style_profile,
                numerator,
                denominator,
                composition_key,
                bpm
            )
            score.insert(0, part)
        
        return score
    
    def _create_metadata(self, style_profile: Dict[str, Any]) -> Any:
        """Create metadata for the composition."""
        from music21 import metadata
        
        md = metadata.Metadata()
        instruments_str = ', '.join(self.instruments)
        
        title_parts = [f"Composition for {instruments_str} in the style of {style_profile.get('composer', 'Unknown')}"]
        if self.mood:
            title_parts.append(f"({self.mood} mood)")
        
        md.title = ' '.join(title_parts)
        md.composer = f"AI (style: {style_profile.get('composer', 'Unknown')})"
        
        copyright_parts = [f"Difficulty: {self.difficulty.capitalize()}"]
        if self.mood:
            copyright_parts.append(f"Mood: {self.mood.capitalize()}")
        
        md.copyright = ' | '.join(copyright_parts)
        
        return md
    
    def _create_instrument_part(
        self,
        instrument_name: str,
        style_profile: Dict[str, Any],
        time_sig_num: int,
        time_sig_denom: int,
        composition_key: str,
        bpm: int
    ) -> stream.Part:
        """Create a part for a specific instrument."""
        from music21 import instrument as m21_instrument
        
        part = stream.Part()
        
        # Set instrument
        try:
            # Try to set the instrument from music21's library
            instr_class = getattr(m21_instrument, instrument_name.replace(' ', '').capitalize(), None)
            if instr_class:
                part.insert(0, instr_class())
            else:
                # Fallback to generic instrument
                part.partName = instrument_name.capitalize()
        except AttributeError:
            part.partName = instrument_name.capitalize()
        
        # Add clefs for this instrument
        clefs = self.instrument_clefs.get(instrument_name.lower(), [clef.TrebleClef()])
        for c in clefs:
            part.insert(0, c)
        
        # Set time signature
        part.insert(0, meter.TimeSignature(f'{time_sig_num}/{time_sig_denom}'))
        
        # Set key - handle both simple keys like "C" and full names like "C major" or "C minor"
        try:
            # Try to create key object
            key_obj = key.Key(composition_key)
            part.insert(0, key_obj)
        except Exception as e:
            logger.warning(f"Failed to parse key '{composition_key}': {e}, using C major")
            part.insert(0, key.Key('C'))
        
        # Set tempo
        part.insert(0, tempo.MetronomeMark(number=bpm))
        
        # Generate measures for this instrument
        measures = self._generate_measures(
            style_profile,
            self.length_measures,
            time_sig_num,
            time_sig_denom,
            instrument_name
        )
        for measure in measures:
            part.append(measure)
        
        return part
    
    def _choose_key(self, style_profile: Dict[str, Any]) -> str:
        """Choose an appropriate key for the composition."""
        era = style_profile.get('era', 'Classical')
        
        # Keys organized by era
        keys = {
            'Baroque': ['C', 'G', 'D', 'A', 'F', 'Bb', 'a', 'd', 'e'],
            'Classical': ['C', 'G', 'D', 'F', 'Bb', 'Eb', 'a', 'd', 'g'],
            'Romantic': ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B', 'c#', 'f#', 'b'],
            'Impressionist': ['C', 'Db', 'D', 'Eb', 'E', 'F#', 'Ab', 'Bb', 'c', 'c#', 'f#']
        }
        
        available_keys = keys.get(era, keys['Classical'])
        
        # If mood is specified, prefer major or minor keys
        if self.mood:
            mood_chars = self.mood_characteristics.get(self.mood.lower(), {})
            prefer_major = mood_chars.get('prefer_major', None)
            
            if prefer_major is True:
                # Filter for major keys (uppercase first letter)
                major_keys = [k for k in available_keys if k[0].isupper()]
                if major_keys:
                    available_keys = major_keys
            elif prefer_major is False:
                # Filter for minor keys (lowercase first letter)
                minor_keys = [k for k in available_keys if k[0].islower()]
                if minor_keys:
                    available_keys = minor_keys
        
        return random.choice(available_keys)
    
    def _choose_tempo(self, style_profile: Dict[str, Any]) -> int:
        """Choose an appropriate tempo, considering mood if specified."""
        era = style_profile.get('era', 'Classical')
        
        tempos = {
            'Baroque': (100, 120),
            'Classical': (90, 120),
            'Romantic': (60, 140),
            'Impressionist': (70, 100)
        }
        
        tempo_range = tempos.get(era, (90, 120))
        base_tempo = random.randint(*tempo_range)
        
        # Apply mood modifier if mood is specified
        if self.mood:
            mood_chars = self.mood_characteristics.get(self.mood.lower(), {})
            tempo_modifier = mood_chars.get('tempo_modifier', 1.0)
            base_tempo = int(base_tempo * tempo_modifier)
        
        # Keep tempo in reasonable range
        base_tempo = max(40, min(200, base_tempo))
        
        return base_tempo
    
    def _generate_measures(
        self,
        style_profile: Dict[str, Any],
        num_measures: int,
        time_sig_num: int,
        time_sig_denom: int,
        instrument_name: str = 'piano'
    ) -> List[stream.Measure]:
        """Generate musical measures for an instrument."""
        measures = []
        
        # Get pitch range for this instrument
        pitch_range = self.instrument_ranges.get(instrument_name.lower(), (48, 84))
        min_pitch, max_pitch = pitch_range
        
        # Start at a comfortable mid-range pitch
        current_pitch = (min_pitch + max_pitch) // 2
        
        for i in range(num_measures):
            measure = stream.Measure(number=i + 1)
            
            # Generate notes for this measure based on difficulty
            beats_left = time_sig_num
            
            while beats_left > 0:
                # Choose note duration based on difficulty
                duration = self._choose_duration(beats_left, style_profile)
                
                # Decide note vs chord vs rest based on difficulty
                use_chord = self._should_use_chord()
                use_rest = self._should_use_rest()
                
                if use_rest:
                    # Add a rest
                    musical_element = note.Rest(quarterLength=duration)
                elif use_chord and instrument_name.lower() in ['piano', 'guitar', 'harp']:
                    # Only certain instruments can play chords easily
                    musical_element = self._create_chord(current_pitch, duration, style_profile)
                else:
                    # Choose pitch (with random walk)
                    current_pitch = self._choose_next_pitch(
                        current_pitch,
                        style_profile,
                        min_pitch,
                        max_pitch
                    )
                    musical_element = note.Note(current_pitch, quarterLength=duration)
                
                measure.append(musical_element)
                beats_left -= duration
            
            measures.append(measure)
        
        return measures
    
    def _should_use_chord(self) -> bool:
        """Determine if a chord should be used based on difficulty."""
        difficulty_chord_prob = {
            'beginner': 0.1,      # Very few chords
            'intermediate': 0.25,  # Some chords
            'advanced': 0.35,      # More chords
            'expert': 0.45         # Many chords
        }
        prob = difficulty_chord_prob.get(self.difficulty, 0.25)
        return random.random() < prob
    
    def _should_use_rest(self) -> bool:
        """Determine if a rest should be used."""
        # All difficulties benefit from some rests for musical phrasing
        return random.random() < 0.15  # 15% chance of rest
    
    def _choose_duration(self, beats_left: float, style_profile: Dict[str, Any]) -> float:
        """Choose a note duration based on difficulty."""
        # Difficulty affects rhythm complexity
        difficulty_durations = {
            'beginner': [4.0, 2.0, 1.0],                    # Whole, half, quarter notes
            'intermediate': [4.0, 2.0, 1.0, 0.5],           # Add eighth notes
            'advanced': [4.0, 2.0, 1.0, 0.5, 0.25],         # Add sixteenth notes
            'expert': [4.0, 2.0, 1.0, 0.5, 0.25, 1.5, 0.75] # Add dotted notes
        }
        
        available_durations = difficulty_durations.get(self.difficulty, [4.0, 2.0, 1.0, 0.5])
        
        # Filter durations that fit in remaining beats
        possible_durations = [d for d in available_durations if d <= beats_left]
        
        if not possible_durations:
            return beats_left
        
        return random.choice(possible_durations)
    
    def _choose_next_pitch(
        self,
        current_pitch: int,
        style_profile: Dict[str, Any],
        min_pitch: int = 48,
        max_pitch: int = 84
    ) -> int:
        """Choose the next pitch using a random walk, constrained by difficulty."""
        melodic_style = style_profile.get('melodic_style', {})
        range_type = melodic_style.get('range', 'moderate')
        
        # Difficulty affects interval complexity
        difficulty_max_steps = {
            'beginner': 5,      # Up to fourth
            'intermediate': 7,  # Up to fifth
            'advanced': 12,     # Up to octave
            'expert': 19        # Up to octave + fifth
        }
        
        base_max_step = difficulty_max_steps.get(self.difficulty, 7)
        
        # Adjust based on melodic range
        if range_type == 'narrow':
            max_step = min(3, base_max_step)
        elif range_type == 'wide':
            max_step = base_max_step
        else:
            max_step = min(7, base_max_step)
        
        # Random walk with preference for smaller intervals
        step = random.choices(
            range(-max_step, max_step + 1),
            weights=[1 / (abs(i) + 1) for i in range(-max_step, max_step + 1)]
        )[0]
        
        new_pitch = current_pitch + step
        
        # Keep within instrument range
        new_pitch = max(min_pitch, min(max_pitch, new_pitch))
        
        return new_pitch
    
    def _create_chord(self, root_pitch: int, duration: float, style_profile: Dict[str, Any]) -> chord.Chord:
        """Create a chord with complexity based on difficulty."""
        # Difficulty affects chord complexity
        if self.difficulty == 'beginner':
            # Simple triads only
            chord_types = ['major', 'minor']
        elif self.difficulty == 'intermediate':
            # Triads and simple seventh chords
            chord_types = ['major', 'minor', 'dominant7']
        elif self.difficulty == 'advanced':
            # More complex chords
            chord_types = ['major', 'minor', 'dominant7', 'major7', 'minor7']
        else:  # expert
            # Very complex chords
            chord_types = ['major', 'minor', 'dominant7', 'major7', 'minor7', 'diminished', 'augmented']
        
        chord_type = random.choice(chord_types)
        
        # Define intervals for each chord type
        chord_intervals = {
            'major': [0, 4, 7],
            'minor': [0, 3, 7],
            'dominant7': [0, 4, 7, 10],
            'major7': [0, 4, 7, 11],
            'minor7': [0, 3, 7, 10],
            'diminished': [0, 3, 6],
            'augmented': [0, 4, 8]
        }
        
        intervals = chord_intervals.get(chord_type, [0, 4, 7])
        pitches = [root_pitch + interval for interval in intervals]
        
        return chord.Chord(pitches, quarterLength=duration)
