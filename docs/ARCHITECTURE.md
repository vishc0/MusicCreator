# MusicCreator Architecture

## System Overview

MusicCreator is a modular, pipeline-based system that transforms a composer's name into original musical compositions with sheet music and audio.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          User Input                              │
│                     (Composer Name)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Research Module                               │
│  • Web scraping (Wikipedia, IMSLP)                              │
│  • API queries (Classical archives)                             │
│  • Data aggregation                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Analysis Module                               │
│  • LLM-based style analysis                                     │
│  • Pattern detection (harmony, melody, rhythm)                  │
│  • Characteristic extraction                                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Generation Module                              │
│  • AI model inference                                           │
│  • Music theory rules                                           │
│  • Generate 5 compositions                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
    ┌──────────────────────┐  ┌──────────────────────┐
    │  Sheet Music Module  │  │   Audio Module       │
    │  • MusicXML export   │  │   • MIDI creation    │
    │  • LilyPond render   │  │   • Audio synthesis  │
    │  • PDF generation    │  │   • MP3/WAV export   │
    └──────────────────────┘  └──────────────────────┘
                  │                     │
                  └──────────┬──────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Output Storage                              │
│  • Local file system                                            │
│  • GitHub Pages (published examples)                            │
│  • Metadata and cataloging                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Module Details

### 1. Research Module (`src/research/`)

**Purpose**: Gather comprehensive information about the composer.

**Components**:
- `scraper.py`: Web scraping using BeautifulSoup
- `api.py`: API integrations for structured data
- `cache.py`: Caching layer to minimize API calls

**Data Sources**:
- Wikipedia: Biographical information, era, influences
- IMSLP (International Music Score Library Project): Works catalog
- Classical Archives: Style characteristics

**Output**: Structured JSON with:
```json
{
  "composer": "Edvard Grieg",
  "era": "Romantic",
  "birth_year": 1843,
  "death_year": 1907,
  "nationality": "Norwegian",
  "influences": ["Norwegian folk music", "Robert Schumann"],
  "characteristics": ["Lyrical melodies", "National romanticism"],
  "notable_works": ["Peer Gynt", "Piano Concerto in A minor"]
}
```

### 2. Analysis Module (`src/analysis/`)

**Purpose**: Extract compositional style patterns using AI.

**Components**:
- `analyzer.py`: LLM integration for style understanding
- `patterns.py`: Music theory pattern detection
- `prompts.py`: Engineered prompts for LLMs

**Process**:
1. Feed research data to LLM
2. Ask for style characteristics:
   - Harmonic progressions
   - Melodic contours
   - Rhythmic patterns
   - Formal structures
   - Instrumentation preferences

**Models Used** (free-tier):
- Hugging Face: `mistralai/Mistral-7B-Instruct-v0.2`
- Alternative: `meta-llama/Llama-2-7b-chat-hf`

**Output**: Style profile JSON:
```json
{
  "harmonic_style": {
    "common_progressions": ["I-IV-V-I", "vi-IV-I-V"],
    "chromaticism_level": "moderate",
    "modulation_frequency": "frequent"
  },
  "melodic_style": {
    "contour": "arch-shaped",
    "range": "moderate",
    "ornamentation": "folk-inspired"
  },
  "rhythmic_style": {
    "time_signatures": ["3/4", "4/4"],
    "rhythmic_patterns": ["dotted rhythms", "syncopation"]
  }
}
```

### 3. Generation Module (`src/generation/`)

**Purpose**: Create original compositions based on style profile.

**Components**:
- `generator.py`: Main generation orchestrator
- `models.py`: AI model interfaces
- `constraints.py`: Music theory constraints
- `postprocess.py`: Clean up and validate output

**Approach**:
1. Use LLM to generate music in ABC notation or MIDI-like format
2. Apply music theory constraints
3. Post-process for playability
4. Generate 5 variations with different seeds

**Libraries**:
- `music21`: Music theory and notation
- `midiutil`: MIDI file creation
- Custom generation logic

### 4. Sheet Music Module (`src/sheet_music/`)

**Purpose**: Convert compositions to readable sheet music.

**Components**:
- `musicxml.py`: Export to MusicXML format
- `lilypond.py`: Generate LilyPond source
- `renderer.py`: Render to PDF

**Formats Supported**:
- MusicXML: Standard interchange format
- LilyPond: High-quality engraving
- PDF: Final sheet music

**Process**:
1. Parse generated music structure
2. Convert to MusicXML
3. Optionally render with LilyPond to PDF

### 5. Audio Module (`src/audio/`)

**Purpose**: Generate playable audio from compositions.

**Components**:
- `midi.py`: Create MIDI files
- `synthesis.py`: Synthesize audio using soundfonts
- `export.py`: Export to various formats

**Synthesis Pipeline**:
1. Generate MIDI from music structure
2. Use FluidSynth with free soundfonts
3. Export to MP3/WAV

**Free Tools**:
- FluidSynth: Software synthesizer
- MuseScore soundfonts: Free, high-quality
- pydub: Audio format conversion

### 6. Web Interface (`src/web/`)

**Purpose**: User-friendly web UI for the application.

**Components**:
- `app.py`: Flask web server
- `templates/`: HTML templates
- `static/`: CSS, JS, assets

**Features**:
- Composer input form
- Progress tracking
- Download generated files
- Gallery of examples

## Data Flow

```
1. User Input
   ↓
2. Research (cached)
   ↓
3. Analysis (cached by composer)
   ↓
4. Generation (5 compositions)
   ↓
5. Parallel Processing:
   - Sheet Music Generation
   - Audio Synthesis
   ↓
6. Output Packaging
   ↓
7. Storage/Display
```

## Technology Choices

### Why These Technologies?

1. **Python**: Rich ecosystem for AI/ML and music processing
2. **Hugging Face**: Free-tier LLM access, open-source models
3. **music21**: Comprehensive music theory library
4. **FluidSynth**: Free, high-quality audio synthesis
5. **Flask**: Lightweight, easy to deploy
6. **GitHub Actions**: Free CI/CD for public repos
7. **GitHub Pages**: Free static site hosting

### Zero-Cost Architecture

- **Compute**: GitHub Actions runners (free tier: 2000 min/month)
- **Storage**: GitHub repository + GitHub Pages
- **AI/ML**: Hugging Face Inference API (free tier)
- **Hosting**: GitHub Pages (static frontend)

## Scaling Considerations

### Current Limitations
- API rate limits (manageable with caching)
- GitHub Actions minutes (2000/month free)
- Single-user focused

### Future Scaling
- Add job queue for multiple requests
- Cache all composer analyses
- Pre-generate popular composers
- CDN for audio/sheet music files

## Security & Privacy

- No user data storage
- API keys via GitHub Secrets
- No external database (stateless)
- All processing ephemeral

## Performance Optimizations

1. **Caching**:
   - Research results by composer
   - Style analyses by composer
   - Generated compositions (optional)

2. **Parallel Processing**:
   - Generate all 5 compositions in parallel
   - Create sheet music and audio concurrently

3. **Lazy Loading**:
   - Load AI models only when needed
   - Stream large audio files

## Deployment

### Development
```bash
python src/main.py --composer "Mozart"
```

### Production (GitHub Actions)
- Triggered by PR comments or schedule
- Runs pipeline in cloud
- Publishes to GitHub Pages

### Web Interface
- Static frontend on GitHub Pages
- Backend API (optional): GitHub Actions webhook

## Error Handling

- Graceful degradation if API fails
- Retry logic with exponential backoff
- Fallback to cached data
- Clear error messages to users

## Testing Strategy

- Unit tests for each module
- Integration tests for pipeline
- Example-based validation
- Music theory validation (music21)

## Future Enhancements

- Support for multiple instruments
- Longer compositions
- Real-time generation
- User feedback loop for improvement
- Collaboration features
