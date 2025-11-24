"""
Web Interface - Flask application for MusicCreator with sheet music viewer and audio player.
"""

import os
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from research.researcher import ComposerResearcher
from analysis.analyzer import StyleAnalyzer
from generation.generator import MusicGenerator
from sheet_music.creator import SheetMusicCreator
from audio.synthesizer import AudioSynthesizer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = Path('outputs')
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# Routes
@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/viewer')
def viewer():
    """Sheet music viewer page."""
    return render_template('viewer.html')

@app.route('/api/composers', methods=['GET'])
def get_composers():
    """Get list of popular composers."""
    composers = [
        {'name': 'Johann Sebastian Bach', 'era': 'Baroque', 'years': '1685-1750'},
        {'name': 'Wolfgang Amadeus Mozart', 'era': 'Classical', 'years': '1756-1791'},
        {'name': 'Ludwig van Beethoven', 'era': 'Classical/Romantic', 'years': '1770-1827'},
        {'name': 'Frédéric Chopin', 'era': 'Romantic', 'years': '1810-1849'},
        {'name': 'Johannes Brahms', 'era': 'Romantic', 'years': '1833-1897'},
        {'name': 'Pyotr Ilyich Tchaikovsky', 'era': 'Romantic', 'years': '1840-1893'},
        {'name': 'Claude Debussy', 'era': 'Impressionist', 'years': '1862-1918'},
        {'name': 'Edvard Grieg', 'era': 'Romantic', 'years': '1843-1907'},
        {'name': 'Antonio Vivaldi', 'era': 'Baroque', 'years': '1678-1741'},
        {'name': 'Franz Schubert', 'era': 'Classical/Romantic', 'years': '1797-1828'},
        {'name': 'Robert Schumann', 'era': 'Romantic', 'years': '1810-1856'},
        {'name': 'Franz Liszt', 'era': 'Romantic', 'years': '1811-1886'},
    ]
    return jsonify(composers)

@app.route('/api/generate', methods=['POST'])
def generate_music():
    """Generate music compositions."""
    try:
        data = request.json
        composer = data.get('composer', 'Mozart')
        instruments = data.get('instruments', ['piano'])
        difficulty = data.get('difficulty', 'intermediate')
        mood = data.get('mood', None)
        time_signature = data.get('timeSignature', None)
        key_signature = data.get('keySignature', None)
        tempo = data.get('tempo', None)
        num_compositions = data.get('numCompositions', 3)
        
        logger.info(f"Generating music: {composer}, {instruments}, {difficulty}")
        
        # Create unique output directory for this generation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = app.config['UPLOAD_FOLDER'] / f"{composer.replace(' ', '_')}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure generation
        config = {
            'research': {'cache': {'enabled': True}},
            'analysis': {'cache': {'enabled': True}},
            'generation': {
                'num_compositions': num_compositions,
                'instruments': instruments,
                'difficulty': difficulty,
                'mood': mood,
                'time_signature': time_signature,
                'key': key_signature,
                'tempo': tempo
            },
            'sheet_music': {'software': 'auto'},
            'audio': {'format': 'midi'}
        }
        
        # Step 1: Research composer
        researcher = ComposerResearcher(config.get('research', {}))
        composer_data = researcher.research(composer)
        
        # Step 2: Analyze style
        analyzer = StyleAnalyzer(config.get('analysis', {}))
        style_profile = analyzer.analyze(composer_data)
        
        # Step 3: Generate compositions
        generator = MusicGenerator(config.get('generation', {}))
        compositions = generator.generate(style_profile, num_compositions)
        
        # Step 4 & 5: Create sheet music and audio
        sheet_music_creator = SheetMusicCreator(config.get('sheet_music', {}))
        synthesizer = AudioSynthesizer(config.get('audio', {}))
        
        generated_files = []
        
        for i, composition in enumerate(compositions, 1):
            base_name = f"{composer.replace(' ', '_')}_composition_{i}"
            
            # Create sheet music (MusicXML)
            xml_path = output_dir / f"{base_name}.xml"
            sheet_music_creator.create(composition, xml_path)
            
            # Create audio (MIDI)
            midi_path = output_dir / f"{base_name}.mid"
            synthesizer.synthesize(composition, midi_path)
            
            generated_files.append({
                'number': i,
                'sheetMusic': f"/outputs/{output_dir.name}/{xml_path.name}",
                'audio': f"/outputs/{output_dir.name}/{midi_path.name}",
                'title': f"Composition {i} in the style of {composer}"
            })
        
        return jsonify({
            'status': 'success',
            'message': f'Generated {len(compositions)} compositions',
            'composer': composer,
            'outputDir': str(output_dir.name),
            'files': generated_files
        })
        
    except Exception as e:
        logger.error(f"Error in generate_music: {e}", exc_info=True)
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/compositions', methods=['GET'])
def get_compositions():
    """Get list of all generated compositions."""
    compositions = []
    output_folder = app.config['UPLOAD_FOLDER']
    
    if not output_folder.exists():
        return jsonify([])
    
    for composer_dir in sorted(output_folder.iterdir(), reverse=True):
        if composer_dir.is_dir():
            midi_files = list(composer_dir.glob('*.mid'))
            xml_files = list(composer_dir.glob('*.xml'))
            
            for midi_file in midi_files:
                xml_file = composer_dir / midi_file.name.replace('.mid', '.xml')
                
                compositions.append({
                    'name': midi_file.stem,
                    'composer': composer_dir.name.split('_')[0].replace('_', ' '),
                    'date': composer_dir.name.split('_')[-2:],
                    'sheetMusic': f"/outputs/{composer_dir.name}/{xml_file.name}" if xml_file.exists() else None,
                    'audio': f"/outputs/{composer_dir.name}/{midi_file.name}",
                })
    
    return jsonify(compositions)

@app.route('/outputs/<path:filename>')
def serve_output(filename):
    """Serve generated files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/delete/<path:filename>', methods=['DELETE'])
def delete_composition(filename):
    """Delete a composition."""
    try:
        file_path = app.config['UPLOAD_FOLDER'] / filename
        if file_path.exists():
            file_path.unlink()
            return jsonify({'status': 'success', 'message': 'File deleted'})
        return jsonify({'status': 'error', 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'MusicCreator API',
        'version': '0.1.0'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
