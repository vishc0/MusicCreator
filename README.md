# MusicCreator 🎵

Create sheet music and audio compositions in the style of any composer you want.

## Overview

MusicCreator is an AI-powered application that:
- Researches composers and their musical styles
- Analyzes compositional patterns and techniques
- Generates original music compositions in the composer's style
- Creates professional sheet music (MusicXML/PDF)
- Produces audio files (MIDI/MP3)

## Features

- 🌐 **Web Interface**: Beautiful, intuitive interface with sheet music viewer and audio player
- 🔍 **Composer Research**: Automatically gathers information about composers from online sources
- 🎼 **Style Analysis**: Uses AI to understand compositional patterns and characteristics
- 🎹 **Music Generation**: Creates 5 sample compositions in the target composer's style
- 🎻 **Multiple Instruments**: Support for 20+ instruments (piano, violin, flute, etc.)
- 📊 **Difficulty Levels**: Generate music for beginner, intermediate, advanced, or expert levels
- 🎭 **Mood Control**: Specify the mood/tone (happy, sad, dramatic, peaceful, energetic, etc.)
- ⏱️ **Musical Parameters**: Control time signature, key signature, and tempo
- 💻 **Software Choice**: Use MuseScore, LilyPond, or auto-detect for sheet music rendering
- 📄 **Sheet Music**: Generates professional-quality sheet music documents (view in browser!)
- 🎵 **Audio Output**: Produces playable audio files from generated compositions
- 💰 **Zero-Cost Deployment**: Multiple free hosting options available

## Quick Start

### Web Interface (Recommended)

**Run locally:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start web server
python src/web/app.py

# 3. Open browser
# Visit: http://localhost:5000
```

**Deploy for free:**
- See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for zero-cost hosting options
- Options: Railway.app, Render.com, Replit, GitHub Pages

### Command Line

**Basic usage:**
```bash
python src/main.py --composer "Edvard Grieg"
```

**With instruments and difficulty:**
```bash
python src/main.py --composer "Mozart" --instruments piano violin --difficulty advanced
```

**With mood and musical parameters (Advanced):**
```bash
python src/main.py --composer "Beethoven" \
  --instruments piano violin cello \
  --difficulty expert \
  --mood dramatic \
  --time-signature 3/4 \
  --key-signature "C minor" \
  --tempo 120 \
  --software musescore
```

**More examples:**
```bash
# Peaceful beginner piano piece in 6/8 time
python src/main.py --composer "Debussy" \
  --instruments piano \
  --difficulty beginner \
  --mood peaceful \
  --time-signature 6/8 \
  --tempo 72

# Energetic string quartet
python src/main.py --composer "Haydn" \
  --instruments violin violin viola cello \
  --difficulty advanced \
  --mood energetic

# Romantic woodwind quintet with LilyPond output
python src/main.py --composer "Brahms" \
  --instruments flute oboe clarinet bassoon \
  --difficulty intermediate \
  --mood romantic \
  --software lilypond
```

#### Web Interface

Start the web server:
```bash
python src/web/app.py
```

Then open http://localhost:5000 in your browser.

## Architecture

```
MusicCreator/
├── src/                    # Source code
│   ├── research/          # Composer research module
│   ├── analysis/          # Style analysis module
│   ├── generation/        # Music generation module
│   ├── sheet_music/       # Sheet music creation
│   ├── audio/             # Audio generation
│   └── web/               # Web interface
├── docs/                   # Documentation
├── tests/                  # Test suite
├── config/                 # Configuration files
├── examples/              # Example outputs
└── workflows/             # CI/CD workflows
```

## Technology Stack

- **AI/ML**: Hugging Face Transformers, OpenAI-compatible APIs
- **Music Generation**: Music21, MIDIUtil
- **Sheet Music**: LilyPond, MusicXML
- **Audio**: FluidSynth, pydub
- **Web**: Flask, Bootstrap
- **CI/CD**: GitHub Actions
- **Deployment**: GitHub Pages (frontend), zero-cost hosting

## Documentation

- 🚀 **[Deployment Guide](docs/DEPLOYMENT.md)** - Zero-cost hosting options
- ⚙️ **[Configuration Guide](docs/CONFIGURE.md)** - Setup and API configuration
- 🤝 **[Contributing Guidelines](docs/CONTRIBUTING.md)** - How to contribute
- 🏗️ **[Architecture Details](docs/ARCHITECTURE.md)** - System design
- 📖 **[API Documentation](docs/API.md)** - Complete API reference
- ⚡ **[Quick Reference](docs/QUICK_REFERENCE.md)** - Fast lookup guide

## Examples

Try these composers:
- Edvard Grieg (Romantic, Norwegian folk influences)
- Johann Sebastian Bach (Baroque, contrapuntal)
- Wolfgang Amadeus Mozart (Classical, elegant melodies)
- Claude Debussy (Impressionist, innovative harmonies)
- Ludwig van Beethoven (Classical/Romantic, dramatic)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Roadmap

- [x] Project setup and architecture
- [ ] Composer research module
- [ ] Style analysis with LLMs
- [ ] Music generation pipeline
- [ ] Sheet music creation
- [ ] Audio synthesis
- [ ] Web interface
- [ ] Publishing pipeline
- [ ] Example compositions gallery

## Support

For questions or issues, please [open an issue](https://github.com/vishc0/MusicCreator/issues).

## Acknowledgments

Built with free-tier APIs and open-source tools to ensure zero-cost operation.
