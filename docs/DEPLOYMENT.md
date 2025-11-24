# MusicCreator Deployment Guide - Zero Cost

## Overview

This guide shows how to deploy MusicCreator at absolutely **zero cost** using only free services.

## Zero-Cost Architecture

### Option 1: GitHub Pages + GitHub Actions (Recommended)

**What you get:**
- ✅ Static website hosting (GitHub Pages)
- ✅ Music generation via GitHub Actions
- ✅ File storage in repository
- ✅ Completely free for public repositories

**Limitations:**
- GitHub Actions: 2000 minutes/month free
- Each generation takes ~2-5 minutes
- Public repository required

**Setup:**

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` or `main`
   - Folder: `/docs` or `/` (root)

2. **Copy static files to docs/**:
   ```bash
   mkdir -p docs
   cp -r src/web/templates/index.html docs/
   cp -r src/web/static docs/
   # Edit index.html to use relative paths for CSS/JS
   ```

3. **Generate music using GitHub Actions**:
   - Go to Actions tab
   - Select "CI/CD Pipeline"
   - Click "Run workflow"
   - Enter parameters
   - Download artifacts after completion

### Option 2: Local Deployment with Web Interface

**What you get:**
- ✅ Full web interface with sheet music viewer
- ✅ Audio player
- ✅ Live generation
- ✅ Completely free (runs on your machine)

**Setup:**

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the web server**:
   ```bash
   python src/web/app.py
   ```

3. **Open in browser**:
   ```
   http://localhost:5000
   ```

### Option 3: Replit (Free Cloud Hosting)

**What you get:**
- ✅ Cloud hosting
- ✅ Web IDE
- ✅ Always accessible
- ✅ Free tier available

**Setup:**

1. Go to [Replit](https://replit.com)
2. Create new Repl from GitHub
3. Import: `https://github.com/vishc0/MusicCreator`
4. Run: `python src/web/app.py`
5. Replit will provide a public URL

**Free tier limits:**
- CPU time limits
- Memory limits
- Goes to sleep when inactive

### Option 4: Railway.app (Free Tier)

**What you get:**
- ✅ $5/month free credit
- ✅ Always running
- ✅ Custom domain support
- ✅ Automatic deployments

**Setup:**

1. Create `railway.json`:
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python src/web/app.py",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

2. Create `Procfile`:
   ```
   web: python src/web/app.py
   ```

3. Deploy:
   - Go to [Railway.app](https://railway.app)
   - New Project → Deploy from GitHub
   - Select MusicCreator repository
   - Deploy

### Option 5: Render.com (Free Tier)

**What you get:**
- ✅ Free web services
- ✅ Auto-deploy from GitHub
- ✅ Custom domains
- ✅ SSL included

**Setup:**

1. Create `render.yaml`:
   ```yaml
   services:
     - type: web
       name: musiccreator
       env: python
       buildCommand: "pip install -r requirements.txt"
       startCommand: "python src/web/app.py"
       envVars:
         - key: FLASK_ENV
           value: production
   ```

2. Deploy:
   - Go to [Render.com](https://render.com)
   - New → Web Service
   - Connect GitHub repository
   - Deploy

**Free tier limits:**
- Services sleep after 15 min of inactivity
- Limited bandwidth

## Web Interface Features

### 1. Music Generation Page (`/`)
- Select composer
- Choose instruments
- Set difficulty level
- Configure mood and advanced options
- Generate music directly in browser

### 2. Compositions Viewer (`/viewer`)
- View all generated compositions
- Sheet music viewer using OpenSheetMusicDisplay
- Audio player for MIDI files
- Download files

### 3. API Endpoints

All available at `/api/`:

- `GET /api/composers` - List of composers
- `POST /api/generate` - Generate music
- `GET /api/compositions` - List generated music
- `GET /outputs/<file>` - Serve generated files

## Running Locally

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start web server
python src/web/app.py

# 3. Open browser
# Navigate to: http://localhost:5000
```

### Using the Web Interface

1. **Generate Music**:
   - Fill in the form on the home page
   - Click "Generate Music"
   - Wait for generation to complete
   - View results with sheet music and audio

2. **View Your Compositions**:
   - Click "My Compositions" in navigation
   - Browse all generated music
   - Click "View Sheet Music" to see notation
   - Click "Play Audio" to hear the music

3. **Download Files**:
   - MusicXML files for sheet music
   - MIDI files for audio
   - Open in MuseScore, Finale, or other software

## Production Deployment

### Environment Variables

Set these in your hosting platform:

```bash
# Required
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Optional
HUGGINGFACE_API_KEY=hf_xxxxx
PORT=5000
```

### Security Considerations

1. **Change SECRET_KEY**:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

2. **Disable Debug Mode**:
   ```bash
   export FLASK_ENV=production
   ```

3. **Use HTTPS**:
   - Most free hosts provide SSL automatically
   - If not, use Cloudflare (free)

## Cost Breakdown

| Service | Cost | Limits |
|---------|------|--------|
| GitHub Pages | **FREE** | 100GB bandwidth/month, public repos |
| GitHub Actions | **FREE** | 2000 minutes/month |
| Replit | **FREE** | CPU/memory limits, sleeps when inactive |
| Railway.app | **FREE** | $5/month credit (≈500 hours) |
| Render.com | **FREE** | Sleeps after 15 min, 750 hours/month |
| Vercel | **FREE** | 100GB bandwidth, serverless functions |

**Recommendation**: Use GitHub Pages + GitHub Actions for truly zero-cost, always-available deployment.

## Troubleshooting

### Port Already in Use

```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
export PORT=8080
python src/web/app.py
```

### Dependencies Won't Install

```bash
# Update pip
pip install --upgrade pip

# Install with no cache
pip install -r requirements.txt --no-cache-dir
```

### Web Server Won't Start

```bash
# Check Python version (need 3.9+)
python --version

# Check Flask installation
python -c "import flask; print(flask.__version__)"
```

### Sheet Music Won't Display

The sheet music viewer requires a browser with JavaScript enabled and internet connection (for OpenSheetMusicDisplay CDN). Download the MusicXML file and open in:
- MuseScore (free)
- Finale
- Sibelius
- Any notation software

## Next Steps

1. **Add your API keys** (optional, for enhanced style analysis)
2. **Generate some music** using the web interface
3. **Share your deployment** with others
4. **Customize** the interface in `src/web/templates/`
5. **Contribute** improvements back to the project

## Support

- GitHub Issues: https://github.com/vishc0/MusicCreator/issues
- Documentation: See `/docs` folder
- Examples: Generate music and check `/viewer`
