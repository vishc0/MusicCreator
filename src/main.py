#!/usr/bin/env python3
"""
MusicCreator CLI - Main entry point for the application.

Usage:
    python src/main.py --composer "Edvard Grieg"
    python src/main.py --composer "Mozart" --instruments piano violin --difficulty intermediate
    python src/main.py --composer "Bach" --instruments piano --difficulty advanced --output-dir ./outputs
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
import yaml

# Import our modules
from research.researcher import ComposerResearcher
from analysis.analyzer import StyleAnalyzer
from generation.generator import MusicGenerator
from sheet_music.creator import SheetMusicCreator
from audio.synthesizer import AudioSynthesizer


# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: Optional[str] = None) -> dict:
    """Load configuration from YAML file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        
        # If config doesn't exist, use example
        if not config_path.exists():
            config_path = Path(__file__).parent.parent / "config" / "config.example.yaml"
    
    config_path = Path(config_path)
    if not config_path.exists():
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return {}
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description='MusicCreator - Generate music in the style of any composer'
    )
    parser.add_argument(
        '--composer',
        type=str,
        required=True,
        help='Name of the composer (e.g., "Edvard Grieg", "Mozart")'
    )
    parser.add_argument(
        '--instruments',
        type=str,
        nargs='+',
        default=['piano'],
        help='Instruments to compose for (e.g., piano violin flute). Multiple instruments can be specified.'
    )
    parser.add_argument(
        '--difficulty',
        type=str,
        choices=['beginner', 'intermediate', 'advanced', 'expert'],
        default='intermediate',
        help='Difficulty level of the composition (default: intermediate)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='outputs',
        help='Output directory for generated files'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (default: config/config.yaml)'
    )
    parser.add_argument(
        '--num-compositions',
        type=int,
        default=5,
        help='Number of compositions to generate (default: 5)'
    )
    
    # Advanced options
    advanced = parser.add_argument_group('Advanced Options')
    advanced.add_argument(
        '--software',
        type=str,
        choices=['musescore', 'lilypond', 'auto'],
        default='auto',
        help='Software to use for sheet music rendering (default: auto)'
    )
    advanced.add_argument(
        '--mood',
        type=str,
        help='Mood/tone of the music (e.g., happy, melancholic, dramatic, peaceful, energetic)'
    )
    advanced.add_argument(
        '--time-signature',
        type=str,
        help='Time signature (e.g., 4/4, 3/4, 6/8). Overrides composer style.'
    )
    advanced.add_argument(
        '--key-signature',
        type=str,
        help='Key signature (e.g., "C major", "A minor", "Eb"). Overrides composer style.'
    )
    advanced.add_argument(
        '--tempo',
        type=int,
        help='Tempo in BPM (e.g., 120). Overrides composer style.'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without actually generating files (for testing)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    config = load_config(args.config)
    
    # Update config with CLI args
    if args.num_compositions:
        config.setdefault('generation', {})['num_compositions'] = args.num_compositions
    
    # Add instruments and difficulty to config
    config.setdefault('generation', {})['instruments'] = args.instruments
    config.setdefault('generation', {})['difficulty'] = args.difficulty
    
    # Add advanced options to config
    if args.mood:
        config.setdefault('generation', {})['mood'] = args.mood
    if args.time_signature:
        config.setdefault('generation', {})['time_signature'] = args.time_signature
    if args.key_signature:
        config.setdefault('generation', {})['key'] = args.key_signature
    if args.tempo:
        config.setdefault('generation', {})['tempo'] = args.tempo
    
    # Sheet music software preference
    config.setdefault('sheet_music', {})['software'] = args.software
    
    logger.info(f"🎵 MusicCreator v0.1.0")
    logger.info(f"📝 Composer: {args.composer}")
    logger.info(f"🎼 Instruments: {', '.join(args.instruments)}")
    logger.info(f"📊 Difficulty: {args.difficulty}")
    
    # Log advanced options if specified
    if args.mood:
        logger.info(f"🎭 Mood: {args.mood}")
    if args.time_signature:
        logger.info(f"⏱️  Time Signature: {args.time_signature}")
    if args.key_signature:
        logger.info(f"🎹 Key Signature: {args.key_signature}")
    if args.tempo:
        logger.info(f"🎼 Tempo: {args.tempo} BPM")
    if args.software != 'auto':
        logger.info(f"💻 Software: {args.software}")
    
    logger.info(f"📁 Output directory: {args.output_dir}")
    
    if args.dry_run:
        logger.info("🏃 DRY RUN MODE - No files will be generated")
    
    try:
        # Create output directory
        output_path = Path(args.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Research the composer
        logger.info("🔍 Step 1/5: Researching composer...")
        researcher = ComposerResearcher(config.get('research', {}))
        composer_data = researcher.research(args.composer)
        logger.info(f"✓ Found information about {composer_data.get('name', args.composer)}")
        
        # Step 2: Analyze musical style
        logger.info("🎼 Step 2/5: Analyzing musical style...")
        analyzer = StyleAnalyzer(config.get('analysis', {}))
        style_profile = analyzer.analyze(composer_data)
        logger.info(f"✓ Analyzed style characteristics")
        
        # Step 3: Generate compositions
        logger.info("🎹 Step 3/5: Generating compositions...")
        generator = MusicGenerator(config.get('generation', {}))
        compositions = generator.generate(style_profile, args.num_compositions)
        logger.info(f"✓ Generated {len(compositions)} compositions")
        
        if args.dry_run:
            logger.info("✓ Dry run complete - stopping before file generation")
            return 0
        
        # Step 4: Create sheet music
        logger.info("📄 Step 4/5: Creating sheet music...")
        sheet_music_creator = SheetMusicCreator(config.get('sheet_music', {}))
        sheet_music_files = []
        for i, composition in enumerate(compositions, 1):
            output_file = output_path / f"{args.composer.replace(' ', '_')}_composition_{i}.pdf"
            sheet_music_creator.create(composition, output_file)
            sheet_music_files.append(output_file)
            logger.info(f"  ✓ Created sheet music {i}/{len(compositions)}")
        
        # Step 5: Generate audio
        logger.info("🎵 Step 5/5: Generating audio...")
        synthesizer = AudioSynthesizer(config.get('audio', {}))
        audio_files = []
        for i, composition in enumerate(compositions, 1):
            output_file = output_path / f"{args.composer.replace(' ', '_')}_composition_{i}.mp3"
            synthesizer.synthesize(composition, output_file)
            audio_files.append(output_file)
            logger.info(f"  ✓ Generated audio {i}/{len(compositions)}")
        
        # Success!
        logger.info("=" * 60)
        logger.info("✨ Success! Generated files:")
        logger.info(f"   📄 Sheet music: {len(sheet_music_files)} files")
        logger.info(f"   🎵 Audio: {len(audio_files)} files")
        logger.info(f"   📁 Location: {output_path.absolute()}")
        logger.info("=" * 60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())
