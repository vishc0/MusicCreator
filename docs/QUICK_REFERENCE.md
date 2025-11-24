# MusicCreator Quick Reference Guide

## Command-Line Options

### Required
```bash
--composer "Name"          # Composer to emulate (e.g., "Mozart", "Beethoven")
```

### Basic Options
```bash
--instruments [list]       # One or more instruments (default: piano)
--difficulty [level]       # beginner | intermediate | advanced | expert
--num-compositions [n]     # Number of pieces to generate (default: 5)
--output-dir [path]        # Where to save files (default: outputs)
```

### Advanced Options
```bash
--mood [mood]             # Emotional tone of the music
--time-signature [sig]    # Force specific time signature (e.g., 3/4, 6/8)
--key-signature [key]     # Force specific key (e.g., "C", "a", "Eb")
--tempo [bpm]             # Force specific tempo in BPM
--software [choice]       # musescore | lilypond | auto
```

### Utility Options
```bash
--dry-run                 # Test without generating files
--verbose                 # Show detailed logs
--config [path]           # Use custom config file
```

---

## Instruments (20+ supported)

### Keyboard
`piano` `organ` `harpsichord`

### Strings
`violin` `viola` `cello` `bass` `guitar` `harp`

### Woodwinds
`flute` `clarinet` `oboe` `bassoon`

### Brass
`trumpet` `trombone` `french horn` `tuba`

### Voice
`voice` `soprano` `alto` `tenor` `bass`

---

## Difficulty Levels

| Level | Rhythms | Intervals | Chords | Characteristics |
|-------|---------|-----------|--------|-----------------|
| **beginner** | ♩ ♪ 𝅗𝅥 | Small (≤ 4th) | Few, simple triads | Simple, easy to play |
| **intermediate** | + ♫ | Medium (≤ 5th) | Some triads + 7ths | Moderate complexity |
| **advanced** | + ♬ | Large (≤ octave) | Many, with 7ths | Complex patterns |
| **expert** | + dotted | Very large (> octave) | Complex (dim, aug) | Virtuosic, challenging |

---

## Mood Options

| Mood | Key Preference | Tempo | Complexity | Example Usage |
|------|---------------|-------|------------|---------------|
| **happy** | Major | Fast (×1.2) | Simple | Joyful celebration |
| **sad** | Minor | Slow (×0.7) | Simple | Sorrowful lament |
| **melancholic** | Minor | Moderate-slow | Moderate | Wistful reflection |
| **dramatic** | Any | Fast (×1.3) | Complex | Intense, theatrical |
| **peaceful** | Major | Slow (×0.7) | Simple | Calm, serene |
| **energetic** | Major | Very fast (×1.4) | Complex | Dynamic, exciting |
| **mysterious** | Minor | Moderate | Moderate | Enigmatic, suspenseful |
| **triumphant** | Major | Moderate-fast | Complex | Victorious, heroic |
| **romantic** | Major | Moderate-slow | Moderate | Tender, loving |
| **playful** | Major | Fast (×1.25) | Moderate | Light, whimsical |

---

## Software Options

| Option | Description | Requires |
|--------|-------------|----------|
| **musescore** | Use MuseScore for PDF rendering | MuseScore installed |
| **lilypond** | Use LilyPond for professional engraving | LilyPond installed |
| **auto** | Auto-detect available software | Nothing (falls back to MusicXML) |

---

## Quick Examples

### Simple Piano Piece
```bash
python src/main.py --composer "Mozart"
```

### String Quartet
```bash
python src/main.py --composer "Haydn" \
  --instruments violin violin viola cello \
  --difficulty intermediate
```

### Dramatic Piano Solo
```bash
python src/main.py --composer "Chopin" \
  --instruments piano \
  --difficulty expert \
  --mood dramatic \
  --tempo 144
```

### Peaceful Beginner Piece in 3/4
```bash
python src/main.py --composer "Schumann" \
  --instruments piano \
  --difficulty beginner \
  --mood peaceful \
  --time-signature 3/4 \
  --tempo 90
```

### Full Woodwind Quintet
```bash
python src/main.py --composer "Mozart" \
  --instruments flute oboe clarinet bassoon \
  --difficulty advanced \
  --num-compositions 3
```

### Romantic Waltz
```bash
python src/main.py --composer "Strauss" \
  --instruments piano violin \
  --mood romantic \
  --time-signature 3/4 \
  --key-signature "F" \
  --tempo 168
```

### Energetic Orchestral Excerpt
```bash
python src/main.py --composer "Beethoven" \
  --instruments violin viola cello trumpet \
  --difficulty expert \
  --mood energetic \
  --software lilypond
```

---

## Common Time Signatures

| Signature | Name | Feel | Common Uses |
|-----------|------|------|-------------|
| **4/4** | Common time | Four quarter beats | Most common, marches |
| **3/4** | Triple time | Three quarter beats | Waltz, minuet |
| **6/8** | Compound duple | Six eighth beats | Jig, pastoral |
| **2/4** | Duple time | Two quarter beats | Polka, march |
| **5/4** | Quintuple time | Five quarter beats | Modern, jazz |
| **12/8** | Compound quadruple | Twelve eighth beats | Slow blues, ballad |

---

## Common Key Signatures

### Major Keys
`C` `G` `D` `A` `E` `F` `Bb` `Eb` `Ab` `Db`

### Minor Keys (lowercase)
`a` `e` `b` `f#` `c#` `d` `g` `c` `f` `bb`

### Example Usage
- C major: `--key-signature "C"`
- A minor: `--key-signature "a"`
- E♭ major: `--key-signature "Eb"`
- F# minor: `--key-signature "f#"`

---

## Tempo Guidelines (BPM)

| Tempo | BPM Range | Musical Term | Character |
|-------|-----------|--------------|-----------|
| Very Slow | 40-60 | Largo, Grave | Solemn, serious |
| Slow | 60-80 | Adagio | Slow and stately |
| Moderate | 80-100 | Andante | Walking pace |
| Moderately Fast | 100-120 | Moderato | Moderate speed |
| Fast | 120-150 | Allegro | Fast and lively |
| Very Fast | 150-180 | Vivace, Presto | Quick and lively |
| Extremely Fast | 180+ | Prestissimo | As fast as possible |

---

## Tips for Best Results

1. **Start Simple**: Begin with beginner difficulty and piano to learn the system
2. **Match Era**: Research the composer's era and typical instruments
3. **Combine Features**: Mix instruments, difficulty, and mood for unique results
4. **Experiment**: Try different combinations to discover interesting music
5. **Use Dry Run**: Test settings with `--dry-run` before generating files
6. **Check Output**: Review MusicXML files in notation software for best editing

---

## Troubleshooting

### No PDF files generated?
- Install MuseScore or LilyPond
- Or open the generated .xml files in any notation software

### Music sounds too simple?
- Increase difficulty level
- Add more instruments
- Try expert difficulty with dramatic mood

### Music sounds too complex?
- Decrease difficulty level
- Use beginner difficulty
- Try peaceful or happy mood

### Want specific key/tempo?
- Use advanced options: `--key-signature` and `--tempo`
- These override composer style detection

---

## File Outputs

### Sheet Music
- `.xml` - MusicXML (universal format)
- `.pdf` - PDF (requires MuseScore/LilyPond)
- `.ly` - LilyPond source

### Audio
- `.mid` - MIDI file (playable in any MIDI player)
- `.mp3` - MP3 audio (future feature, requires FluidSynth)

---

## Configuration File

For persistent settings, edit `config/config.yaml`:

```yaml
generation:
  instruments: [piano]
  difficulty: intermediate
  mood: peaceful
  length_measures: 32
  
sheet_music:
  software: auto
  format: pdf
```

Then run without options:
```bash
python src/main.py --composer "Brahms"
```
