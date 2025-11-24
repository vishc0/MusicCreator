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
| `--output-dir` | string | `outputs` | Output directory for generated files |
| `--config` | string | `config/config.yaml` | Path to configuration file |
| `--num-compositions` | integer | 5 | Number of compositions to generate |
| `--dry-run` | flag | false | Run without generating files (testing) |
| `--verbose` | flag | false | Enable verbose logging |

### Examples

```bash
# Generate 5 compositions for Edvard Grieg
python src/main.py --composer "Edvard Grieg"

# Generate 3 compositions with verbose output
python src/main.py --composer "Mozart" --num-compositions 3 --verbose

# Test configuration without generating files
python src/main.py --composer "Bach" --dry-run

# Specify custom output directory
python src/main.py --composer "Debussy" --output-dir ./my-music
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

# Initialize generator
generator = MusicGenerator(config={
    'num_compositions': 5,
    'length_measures': 32,
    'temperature': 0.8
})

# Generate compositions
compositions = generator.generate(style_profile, num_compositions=5)

# Returns: List of music21.stream.Score objects
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
