# Contributing to MusicCreator

Thank you for your interest in contributing to MusicCreator! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/MusicCreator.git
   cd MusicCreator
   ```
3. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Set up pre-commit hooks**:
   ```bash
   pre-commit install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```

## Making Changes

### Code Style

We follow PEP 8 for Python code. Use these tools:

```bash
# Format code
black src/ tests/

# Check style
flake8 src/ tests/

# Type checking
mypy src/
```

### Testing

Always add tests for new features:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_research.py
```

### Documentation

Update documentation when you:
- Add new features
- Change APIs or configurations
- Fix bugs that affect user behavior

## Pull Request Process

1. **Update your branch**:
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Run tests and linting**:
   ```bash
   pytest
   black src/ tests/
   flake8 src/ tests/
   ```

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add composer style caching"
   ```
   
   Use conventional commits:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation only
   - `style:` formatting, missing semicolons, etc.
   - `refactor:` code restructuring
   - `test:` adding tests
   - `chore:` maintenance tasks

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Link any related issues

### PR Checklist

Before submitting, ensure:

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black`)
- [ ] Linting passes (`flake8`)
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main
- [ ] PR description is clear and complete

## Project Structure

```
MusicCreator/
├── src/
│   ├── research/          # Composer research
│   │   ├── __init__.py
│   │   ├── scraper.py     # Web scraping
│   │   └── api.py         # API integrations
│   ├── analysis/          # Style analysis
│   │   ├── __init__.py
│   │   ├── analyzer.py    # LLM-based analysis
│   │   └── patterns.py    # Pattern detection
│   ├── generation/        # Music generation
│   │   ├── __init__.py
│   │   ├── generator.py   # Main generator
│   │   └── models.py      # AI models
│   ├── sheet_music/       # Sheet music creation
│   │   ├── __init__.py
│   │   ├── musicxml.py    # MusicXML export
│   │   └── lilypond.py    # LilyPond export
│   ├── audio/             # Audio generation
│   │   ├── __init__.py
│   │   ├── midi.py        # MIDI creation
│   │   └── synthesis.py   # Audio synthesis
│   ├── web/               # Web interface
│   │   ├── __init__.py
│   │   ├── app.py         # Flask app
│   │   └── templates/     # HTML templates
│   └── main.py            # CLI entry point
├── tests/                 # Test suite
├── docs/                  # Documentation
├── config/                # Configuration files
└── examples/              # Example outputs
```

## Feature Development Workflow

1. **Research Phase**:
   - Investigate existing solutions
   - Design the approach
   - Document in issue or PR

2. **Implementation Phase**:
   - Write minimal working code
   - Add comprehensive tests
   - Update documentation

3. **Review Phase**:
   - Self-review your code
   - Run full test suite
   - Check CI/CD passes

4. **Iteration Phase**:
   - Address review feedback
   - Update based on testing
   - Improve documentation

## Areas for Contribution

### High Priority
- Improve music generation quality
- Add more composer styles
- Enhance web interface
- Performance optimizations

### Medium Priority
- Additional audio formats
- Better error handling
- More comprehensive tests
- Documentation improvements

### Low Priority
- Code refactoring
- UI/UX enhancements
- Additional examples
- Internationalization

## Reporting Issues

### Bug Reports

Include:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python version, etc.)
- Relevant logs or error messages

### Feature Requests

Include:
- Use case and motivation
- Proposed solution
- Alternative approaches considered
- Impact on existing features

## Getting Help

- **Questions**: Open a discussion
- **Bugs**: Open an issue
- **Security**: Email maintainers privately
- **Chat**: Join our community (if available)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to MusicCreator! 🎵
