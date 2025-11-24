# MusicCreator API Documentation

## Command Line Interface

### Basic Usage

```bash
python src/main.py --composer "Composer Name" [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--composer` | string | required | Name of the composer (e.g., "Edvard Grieg") |
| `--instruments` | list | `['piano']` | Instruments to compose for. Multiple can be specified (e.g., `piano violin flute`) |
| `--difficulty` | string | `intermediate` | Difficulty level: `beginner`, `intermediate`, `advanced`, or `expert` |
| `--output-dir` | string | `outputs` | Output directory for generated files |
| `--config` | string | `config/config.yaml` | Path to configuration file |
| `--num-compositions` | integer | 5 | Number of compositions to generate |
| `--dry-run` | flag | false | Run without generating files (testing) |
| `--verbose` | flag | false | Enable verbose logging |

### Advanced Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--software` | string | `auto` | Sheet music software: `musescore`, `lilypond`, or `auto` (auto-detect) |
| `--mood` | string | none | Mood/tone of music (e.g., happy, sad, dramatic, peaceful, energetic, melancholic, mysterious, triumphant, romantic, playful) |
| `--time-signature` | string | style-based | Time signature (e.g., `4/4`, `3/4`, `6/8`, `5/4`). Overrides composer style. |
| `--key-signature` | string | style-based | Key signature (e.g., `"C major"`, `"A minor"`, `"Eb"`). Overrides composer style. |
| `--tempo` | integer | style-based | Tempo in BPM (e.g., 60, 120, 144). Overrides composer style. |

### Supported Instruments

- **Keyboard**: piano, organ, harpsichord
- **Strings**: violin, viola, cello, bass, guitar, harp
- **Woodwinds**: flute, clarinet, oboe, bassoon
- **Brass**: trumpet, trombone, french horn, tuba
- **Voice**: voice, soprano, alto, tenor, bass

### Difficulty Levels

- **Beginner**: Simple rhythms (whole, half, quarter notes), limited pitch range, simple intervals, few chords
- **Intermediate**: Adds eighth notes, moderate pitch range, more intervals, some chords
- **Advanced**: Adds sixteenth notes, wider pitch range, complex intervals, more chords, seventh chords
- **Expert**: Includes dotted rhythms, full instrument range, large intervals, complex chords (diminished, augmented, etc.)

### Mood Options

Each mood affects the musical characteristics:

- **Happy**: Major keys, faster tempo, simple rhythms, forte dynamics
- **Sad**: Minor keys, slower tempo, simple rhythms, piano dynamics
- **Melancholic**: Minor keys, moderate tempo, moderate complexity, soft dynamics
- **Dramatic**: Any key, fast tempo, complex rhythms, very loud dynamics
- **Peaceful**: Major keys, slow tempo, simple rhythms, very soft dynamics
- **Energetic**: Major keys, very fast tempo, complex rhythms, loud dynamics
- **Mysterious**: Minor keys, moderate tempo, moderate complexity, soft dynamics
- **Triumphant**: Major keys, moderate-fast tempo, complex rhythms, very loud dynamics
- **Romantic**: Major keys, slow-moderate tempo, moderate complexity, moderate dynamics
- **Playful**: Major keys, fast tempo, moderate complexity, moderate dynamics

### Software Options

- **musescore**: Use MuseScore for PDF rendering (requires MuseScore installation)
- **lilypond**: Use LilyPond for high-quality engraving (requires LilyPond installation)
- **auto**: Automatically detect and use available software (default)

### Examples

```bash
# Generate 5 compositions for Edvard Grieg (piano, intermediate)
python src/main.py --composer "Edvard Grieg"

# Generate for multiple instruments
python src/main.py --composer "Mozart" --instruments violin viola cello

# Generate beginner-level piano music
python src/main.py --composer "Bach" --instruments piano --difficulty beginner

# Generate expert-level chamber music
python src/main.py --composer "Beethoven" --instruments piano violin cello --difficulty expert --num-compositions 3

# Generate for full woodwind quintet
python src/main.py --composer "Debussy" --instruments flute oboe clarinet bassoon --difficulty advanced

# Advanced: Dramatic music in C minor at 144 BPM
python src/main.py --composer "Chopin" \
  --instruments piano \
  --difficulty advanced \
  --mood dramatic \
  --key-signature "C minor" \
  --tempo 144 \
  --software musescore

# Advanced: Peaceful waltz in 3/4 time
python src/main.py --composer "Strauss" \
  --instruments piano violin \
  --difficulty intermediate \
  --mood peaceful \
  --time-signature 3/4 \
  --tempo 168

# Advanced: Happy baroque music using LilyPond
python src/main.py --composer "Vivaldi" \
  --instruments violin cello \
  --difficulty advanced \
  --mood happy \
  --software lilypond

# Test configuration without generating files
python src/main.py --composer "Bach" --dry-run

# Specify custom output directory
python src/main.py --composer "Grieg" --instruments piano --output-dir ./my-music
```

## Python API

### Composer Research

```python
from src.research.researcher import ComposerResearcher

# Initialize researcher
researcher = ComposerResearcher(config={
    'cache': {'enabled': True, 'directory': '.cache/research'},
    'max_results': 10
})

# Research a composer
composer_data = researcher.research("Edvard Grieg")

# Returns:
# {
#     'name': 'Edvard Grieg',
#     'era': 'Romantic',
#     'birth_year': 1843,
#     'death_year': 1907,
#     'nationality': 'Norwegian',
#     'influences': [...],
#     'characteristics': [...],
#     'notable_works': [...],
#     'biography': '...'
# }
```

### Style Analysis

```python
from src.analysis.analyzer import StyleAnalyzer

# Initialize analyzer
analyzer = StyleAnalyzer(config={
    'model': 'mistralai/Mistral-7B-Instruct-v0.2',
    'temperature': 0.7,
    'max_tokens': 2000,
    'cache': {'enabled': True}
})

# Analyze style
style_profile = analyzer.analyze(composer_data)

# Returns:
# {
#     'composer': 'Edvard Grieg',
#     'era': 'Romantic',
#     'harmonic_style': {...},
#     'melodic_style': {...},
#     'rhythmic_style': {...},
#     'formal_style': {...},
#     'instrumentation': {...}
# }
```

### Music Generation

```python
from src.generation.generator import MusicGenerator

# Initialize generator with instruments and difficulty
generator = MusicGenerator(config={
    'num_compositions': 5,
    'length_measures': 32,
    'temperature': 0.8,
    'instruments': ['piano', 'violin'],
    'difficulty': 'advanced'
})

# Generate compositions
compositions = generator.generate(style_profile, num_compositions=5)

# Returns: List of music21.stream.Score objects with multiple parts
```

**Configuration Options:**

- `instruments`: List of instrument names (default: `['piano']`)
- `difficulty`: One of `'beginner'`, `'intermediate'`, `'advanced'`, `'expert'` (default: `'intermediate'`)
- `num_compositions`: Number of pieces to generate
- `length_measures`: Length of each composition in measures
- `temperature`: Creativity parameter (0.0-1.0)

**Example with different difficulties:**

```python
# Beginner level - simple rhythms and intervals
beginner_config = {
    'instruments': ['piano'],
    'difficulty': 'beginner',
    'length_measures': 16
}
beginner_gen = MusicGenerator(beginner_config)
beginner_pieces = beginner_gen.generate(style_profile)

# Expert level - complex rhythms, chords, and wide intervals
expert_config = {
    'instruments': ['piano', 'violin', 'cello'],
    'difficulty': 'expert',
    'length_measures': 64
}
expert_gen = MusicGenerator(expert_config)
expert_pieces = expert_gen.generate(style_profile)
```

### Sheet Music Creation

```python
from src.sheet_music.creator import SheetMusicCreator
from pathlib import Path

# Initialize creator
creator = SheetMusicCreator(config={
    'format': 'pdf'
})

# Create sheet music
for i, composition in enumerate(compositions):
    output_path = Path(f'output/composition_{i+1}.pdf')
    creator.create(composition, output_path)
```

### Audio Synthesis

```python
from src.audio.synthesizer import AudioSynthesizer
from pathlib import Path

# Initialize synthesizer
synthesizer = AudioSynthesizer(config={
    'format': 'midi'
})

# Synthesize audio
for i, composition in enumerate(compositions):
    output_path = Path(f'output/composition_{i+1}.mid')
    synthesizer.synthesize(composition, output_path)
```

## Configuration File API

### YAML Configuration

```yaml
# config/config.yaml

research:
  sources:
    - wikipedia
    - imslp
  max_results: 10
  cache:
    enabled: true
    ttl_days: 30
    directory: .cache/research

analysis:
  model: "mistralai/Mistral-7B-Instruct-v0.2"
  temperature: 0.7
  max_tokens: 2000
  cache:
    enabled: true
    ttl_days: 90
    directory: .cache/analysis

generation:
  num_compositions: 5
  length_measures: 32
  temperature: 0.8
  time_signature: "4/4"
  key: "auto"

sheet_music:
  format: "pdf"
  musicxml:
    include_annotations: true
  lilypond:
    paper_size: "letter"

audio:
  format: "midi"
  midi:
    tempo: 120
    velocity: 80
  synthesis:
    sample_rate: 44100
```

## Environment Variables

Required environment variables:

```bash
# Hugging Face API Key (required)
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx

# Optional: Additional LLM APIs
OPENAI_API_KEY=sk_xxxxxxxxxxxxx
ANTHROPIC_API_KEY=xxxxxxxxxxxxx

# Publishing
ENABLE_PUBLISH=false
PUBLISH_TOKEN=ghp_xxxxxxxxxxxxx

# Web Interface
FLASK_ENV=development
SECRET_KEY=your-secret-key

# Logging
LOG_LEVEL=INFO

# Cache
ENABLE_CACHE=true
CACHE_DIR=.cache
```

## GitHub Actions API

### Workflow Dispatch

Trigger music generation via GitHub Actions:

```bash
# Via GitHub CLI
gh workflow run ci-cd.yml -f composer="Edvard Grieg"

# Via GitHub UI
# Go to Actions → CI/CD Pipeline → Run workflow
# Enter composer name
```

### Scheduled Generation

The scheduled workflow runs weekly on Sunday at 00:00 UTC:

```yaml
# .github/workflows/scheduled-generation.yml
on:
  schedule:
    - cron: '0 0 * * 0'
```

## HTTP API (Future)

### Web Interface Endpoints

When the web interface is implemented:

```
POST /api/generate
Content-Type: application/json

{
  "composer": "Edvard Grieg",
  "num_compositions": 5,
  "format": "pdf"
}

Response:
{
  "job_id": "abc123",
  "status": "processing"
}
```

```
GET /api/status/{job_id}

Response:
{
  "job_id": "abc123",
  "status": "completed",
  "files": [
    "/downloads/composition_1.pdf",
    "/downloads/composition_1.mid"
  ]
}
```

## Data Models

### ComposerData

```python
{
  "name": str,              # Composer name
  "era": str,               # Musical era
  "birth_year": int,        # Birth year
  "death_year": int,        # Death year
  "nationality": str,       # Nationality
  "influences": List[str],  # Musical influences
  "characteristics": List[str],  # Style characteristics
  "notable_works": List[str],    # Famous works
  "biography": str          # Biography excerpt
}
```

### StyleProfile

```python
{
  "composer": str,
  "era": str,
  "harmonic_style": {
    "progressions": List[str],
    "chromaticism": str,
    "modulation": str
  },
  "melodic_style": {
    "contour": str,
    "range": str,
    "ornamentation": str
  },
  "rhythmic_style": {
    "time_signatures": List[str],
    "complexity": str
  },
  "formal_style": {
    "forms": List[str]
  },
  "instrumentation": {
    "instruments": List[str],
    "texture": str
  }
}
```

## Error Handling

All API functions may raise the following exceptions:

- `ValueError`: Invalid input parameters
- `FileNotFoundError`: Configuration or data files not found
- `requests.RequestException`: API call failures
- `Exception`: General errors (check logs for details)

Example error handling:

```python
try:
    researcher = ComposerResearcher()
    data = researcher.research("Invalid Composer")
except Exception as e:
    logger.error(f"Research failed: {e}")
    # Handle error
```

## Rate Limits

When using Hugging Face API:
- Free tier: ~30 requests per hour
- Caching is enabled by default to minimize API calls
- Failed requests will retry with exponential backoff

## Versioning

Current version: 0.1.0

API versioning will follow semantic versioning (semver):
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes
