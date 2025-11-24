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
        self.software = self.config.get('software', 'auto')  # musescore, lilypond, auto
        
        # Detect available software
        self.available_software = self._detect_software()
    
    def _detect_software(self) -> Dict[str, bool]:
        """Detect which music notation software is available."""
        import shutil
        
        return {
            'musescore': shutil.which('musescore') or shutil.which('mscore') or shutil.which('MuseScore') is not None,
            'lilypond': shutil.which('lilypond') is not None,
        }
    
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
        """Create PDF file using the specified or detected software."""
        logger.debug(f"Creating PDF: {output_path}")
        
        # Determine which software to use
        if self.software == 'musescore' or (self.software == 'auto' and self.available_software.get('musescore')):
            self._create_pdf_musescore(composition, output_path)
        elif self.software == 'lilypond' or (self.software == 'auto' and self.available_software.get('lilypond')):
            self._create_pdf_lilypond(composition, output_path)
        else:
            # Fallback: try music21's built-in PDF generation
            self._create_pdf_builtin(composition, output_path)
    
    def _create_pdf_musescore(self, composition: stream.Score, output_path: Path) -> None:
        """Create PDF using MuseScore."""
        try:
            logger.info(f"Using MuseScore to generate PDF: {output_path}")
            composition.write('musicxml.pdf', fp=str(output_path))
        except Exception as e:
            logger.warning(f"MuseScore PDF generation failed: {e}")
            self._fallback_to_musicxml(composition, output_path)
    
    def _create_pdf_lilypond(self, composition: stream.Score, output_path: Path) -> None:
        """Create PDF using LilyPond."""
        try:
            logger.info(f"Using LilyPond to generate PDF: {output_path}")
            # First create LilyPond file, then compile to PDF
            ly_path = output_path.with_suffix('.ly')
            composition.write('lilypond', fp=str(ly_path))
            
            # LilyPond compilation would happen here
            # For now, we'll keep the .ly file
            logger.info(f"Created LilyPond file: {ly_path}")
            logger.info("Note: Run 'lilypond {ly_path}' to generate PDF")
        except Exception as e:
            logger.warning(f"LilyPond PDF generation failed: {e}")
            self._fallback_to_musicxml(composition, output_path)
    
    def _create_pdf_builtin(self, composition: stream.Score, output_path: Path) -> None:
        """Create PDF using music21's built-in methods."""
        try:
            logger.info(f"Using music21 built-in PDF generation: {output_path}")
            composition.write('musicxml.pdf', fp=str(output_path))
        except Exception as e:
            logger.warning(f"Built-in PDF generation failed: {e}")
            self._fallback_to_musicxml(composition, output_path)
    
    def _fallback_to_musicxml(self, composition: stream.Score, output_path: Path) -> None:
        """Fallback to creating MusicXML when PDF generation fails."""
        logger.info("Falling back to MusicXML export")
        xml_path = output_path.with_suffix('.xml')
        self._create_musicxml(composition, xml_path)
        logger.info(f"Created MusicXML instead: {xml_path}")
        logger.info("You can open this file in MuseScore or other notation software to create a PDF")
    
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
