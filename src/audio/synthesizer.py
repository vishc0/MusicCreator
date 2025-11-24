"""
Audio Synthesizer - Generates audio files from compositions.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from music21 import stream

logger = logging.getLogger(__name__)


class AudioSynthesizer:
    """Synthesizes audio from compositions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the synthesizer with configuration."""
        self.config = config or {}
        self.format = self.config.get('format', 'midi')
    
    def synthesize(self, composition: stream.Score, output_path: Path) -> None:
        """
        Synthesize audio from composition.
        
        Args:
            composition: music21 Score object
            output_path: Path for output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # For now, we'll create MIDI files
        # In the future, we can add MP3/WAV synthesis using FluidSynth
        logger.debug(f"Creating audio: {output_path}")
        
        if output_path.suffix in ['.mp3', '.wav']:
            # Try to synthesize to audio format
            self._create_audio(composition, output_path)
        else:
            # Create MIDI
            self._create_midi(composition, output_path)
    
    def _create_midi(self, composition: stream.Score, output_path: Path) -> None:
        """Create MIDI file."""
        logger.debug(f"Creating MIDI: {output_path}")
        midi_path = output_path.with_suffix('.mid')
        composition.write('midi', fp=str(midi_path))
    
    def _create_audio(self, composition: stream.Score, output_path: Path) -> None:
        """Create audio file (MP3 or WAV)."""
        logger.debug(f"Creating audio: {output_path}")
        
        try:
            # First create MIDI
            midi_path = output_path.with_suffix('.mid')
            composition.write('midi', fp=str(midi_path))
            
            # TODO: In a full implementation, we would use FluidSynth here
            # to convert MIDI to audio. For now, we just create MIDI.
            logger.info(f"Created MIDI file: {midi_path}")
            logger.info("Audio synthesis (MP3/WAV) requires additional setup (FluidSynth)")
            
        except Exception as e:
            logger.error(f"Audio synthesis failed: {e}")
            # Fallback to MIDI
            self._create_midi(composition, output_path)
