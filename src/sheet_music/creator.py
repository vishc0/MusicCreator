"""
Sheet Music Creator - Creates sheet music from compositions.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from music21 import stream, converter

logger = logging.getLogger(__name__)


class SheetMusicCreator:
    """Creates sheet music files from compositions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the sheet music creator with configuration."""
        self.config = config or {}
        self.format = self.config.get('format', 'musicxml')
    
    def create(self, composition: stream.Score, output_path: Path) -> None:
        """
        Create sheet music file from composition.
        
        Args:
            composition: music21 Score object
            output_path: Path for output file
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Determine format from file extension or config
        if output_path.suffix == '.pdf':
            self._create_pdf(composition, output_path)
        elif output_path.suffix == '.xml' or output_path.suffix == '.musicxml':
            self._create_musicxml(composition, output_path)
        elif output_path.suffix == '.ly':
            self._create_lilypond(composition, output_path)
        else:
            # Default to MusicXML
            self._create_musicxml(composition, output_path.with_suffix('.xml'))
    
    def _create_musicxml(self, composition: stream.Score, output_path: Path) -> None:
        """Create MusicXML file."""
        logger.debug(f"Creating MusicXML: {output_path}")
        composition.write('musicxml', fp=str(output_path))
    
    def _create_pdf(self, composition: stream.Score, output_path: Path) -> None:
        """Create PDF file using MuseScore or LilyPond."""
        logger.debug(f"Creating PDF: {output_path}")
        
        try:
            # Try to use MuseScore if available
            composition.write('musicxml.pdf', fp=str(output_path))
        except Exception as e:
            logger.warning(f"PDF generation failed: {e}")
            logger.info("Falling back to MusicXML export")
            # Fallback to MusicXML
            xml_path = output_path.with_suffix('.xml')
            self._create_musicxml(composition, xml_path)
            logger.info(f"Created MusicXML instead: {xml_path}")
    
    def _create_lilypond(self, composition: stream.Score, output_path: Path) -> None:
        """Create LilyPond file."""
        logger.debug(f"Creating LilyPond: {output_path}")
        
        try:
            composition.write('lilypond', fp=str(output_path))
        except Exception as e:
            logger.warning(f"LilyPond generation failed: {e}")
            # Fallback to MusicXML
            xml_path = output_path.with_suffix('.xml')
            self._create_musicxml(composition, xml_path)
