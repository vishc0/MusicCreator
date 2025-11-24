# Configuration Guide

This guide explains how to configure MusicCreator for your environment.

## Required Secrets

MusicCreator uses external APIs that require authentication. These should be configured as GitHub Secrets (never commit them to the repository).

### GitHub Secrets Setup

1. Go to your repository settings: `Settings → Secrets and variables → Actions`
2. Click "New repository secret"
3. Add the following secrets:

#### Required Secrets

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `HUGGINGFACE_API_KEY` | Hugging Face API token for LLM access | Sign up at https://huggingface.co and create an API token under Settings → Access Tokens |

#### Optional Secrets

| Secret Name | Description | How to Obtain |
|-------------|-------------|---------------|
| `OPENAI_API_KEY` | OpenAI API key (if using GPT models) | Sign up at https://platform.openai.com |
| `ANTHROPIC_API_KEY` | Anthropic API key (if using Claude) | Sign up at https://www.anthropic.com |
| `PUBLISH_TOKEN` | Token for publishing outputs | GitHub Personal Access Token with repo permissions |

## Local Configuration

### Environment Variables

For local development, create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env
```

Example `.env` file:
```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
ENABLE_PUBLISH=false
```

### Configuration File

Edit `config/config.yaml` to customize behavior:

```yaml
# Composer research settings
research:
  sources:
    - wikipedia
    - imslp
    - classical_archives
  max_results: 10

# Style analysis settings
analysis:
  model: "mistralai/Mistral-7B-Instruct-v0.2"
  temperature: 0.7
  max_tokens: 2000

# Music generation settings
generation:
  num_compositions: 5
  length_measures: 32
  time_signature: "4/4"
  key: "auto"  # auto-detect from composer style

# Sheet music settings
sheet_music:
  format: "musicxml"  # musicxml, lilypond, or pdf
  include_annotations: true
  paper_size: "letter"

# Audio settings
audio:
  format: "mp3"  # mp3, wav, or midi
  sample_rate: 44100
  soundfont: "default"  # path to .sf2 file or "default"

# Publishing settings
publishing:
  enabled: false  # Set to true to enable auto-publishing
  targets:
    - github_pages
  output_dir: "examples"
```

## Free-Tier API Setup

### Hugging Face (Required)

1. **Sign up**: Visit https://huggingface.co/join
2. **Create API token**:
   - Go to Settings → Access Tokens
   - Click "New token"
   - Name it "MusicCreator"
   - Select "Read" permissions
   - Copy the token (starts with `hf_`)
3. **Add to GitHub Secrets** as `HUGGINGFACE_API_KEY`

**Free tier includes:**
- API rate limits sufficient for this project
- Access to open-source models
- No credit card required

### Alternative LLM Options

#### Groq (Optional, faster inference)

1. Sign up at https://groq.com
2. Get API key from console
3. Add as `GROQ_API_KEY`
4. Update `config.yaml` to use Groq models

#### Together AI (Optional)

1. Sign up at https://together.ai
2. Get $25 free credits
3. Add as `TOGETHER_API_KEY`

## Publishing Setup

### GitHub Pages

To enable publishing to GitHub Pages:

1. **Enable GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages` (will be created automatically)

2. **Set the publish token**:
   - Create a Personal Access Token with `repo` scope
   - Add as `PUBLISH_TOKEN` secret

3. **Enable publishing**:
   - Set `ENABLE_PUBLISH=true` in your environment
   - Or set `publishing.enabled: true` in `config/config.yaml`

## Testing Configuration

Verify your configuration:

```bash
# Test API connections
python tests/test_config.py

# Test with a simple composer
python src/main.py --composer "Mozart" --dry-run
```

## Troubleshooting

### API Rate Limits

If you hit rate limits:
- Use larger intervals in scheduled workflows
- Implement caching (enabled by default)
- Consider upgrading to paid tiers if needed

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission Errors

Ensure GitHub Actions has proper permissions:
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

## Cost Management

All default configurations use **zero-cost** options:
- Free-tier APIs (Hugging Face)
- GitHub-hosted runners
- GitHub Pages hosting (free for public repos)
- Open-source tools and libraries

Monitor usage at:
- Hugging Face: https://huggingface.co/settings/billing
- GitHub Actions: Settings → Billing

## Security Best Practices

- ✅ Never commit API keys or secrets
- ✅ Use GitHub Secrets for sensitive data
- ✅ Add `.env` to `.gitignore`
- ✅ Regularly rotate API tokens
- ✅ Use minimal required permissions
- ✅ Review third-party dependencies regularly
