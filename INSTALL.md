# Burrp - Installation & Setup Guide

## Project Status: 🟢 Complete

All core files have been created and configured. Ready for use.

## Project Structure

```
burrp/
├── burrp.py              # Main CLI tool (executable)
├── requirements.txt      # Python dependencies
├── setup.py              # Package installation setup
├── README.md            # Full documentation
├── PLAN.md              # Project plan
├── INSTALL.md           # This file
├── .gitignore          # Git ignore rules
└── tests/
    ├── __init__.py
    └── test_burrp.py    # Unit tests
```

## Installation Steps

### 1. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Burrp

```bash
pip install -e .
```

This installs burrp as a command-line tool:
```bash
burrp <folder> [options]
```

### 4. Install Ollama

**On macOS:**
```bash
brew install ollama
ollama serve &
ollama pull gemma3
```

**On Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull gemma3
```

**On Windows:**
Download from https://ollama.com/download

### 5. Verify Setup

```bash
ollama list  # Should show gemma3
burrp --help
```

## Quick Start

### Organize a folder (dry run first):
```bash
burrp ~/Downloads --dry-run
```

### Organize for real:
```bash
burrp ~/Downloads
```

### Undo if needed:
```bash
burrp ~/Downloads --undo
```

## Features Implemented

✅ Local AI processing with gemma3
✅ Extension-based categorization
✅ Dry-run mode
✅ Undo support (last 5 operations)
✅ Configuration file support (∼/.config/burrp/config.json)
✅ Error handling
✅ Verbose logging
✅ Auto-creation of config
✅ Handle filename collisions
✅ Skip existing folders

## Key Files

- **burrp.py**: Complete CLI implementation (∼270 lines)
- **requirements.txt**: ollama>=0.1.0
- **setup.py**: Proper package setup for pip install
- **README.md**: Comprehensive documentation
- **tests/test_burrp.py**: Unit tests for validation

## Configuration

Config auto-creates at: `~/.config/burrp/config.json`

Default config:
```json
{
  "model": "gemma3",
  "categories": {
    "Images": [...],
    "Documents": [...],
    ...
  },
  "create_subfolders": true,
  "max_history": 5
}
```

## Testing

Run unit tests:
```bash
python -m pytest tests/test_burrp.py
```

Or with unittest:
```bash
python tests/test_burrp.py
```

## Security Notes

- All processing is local
- Only filenames sent to Ollama, never file contents
- Config stored in ∼/.config/burrp/
- History stored in ∼/.config/burrp/history.json

## Example Workflow

```bash
# 1. Preview what will happen
burrp ~/messy_folder --dry-run

# 2. Feel confident? Organize it
burrp ~/messy_folder

# 3. Oops? Undo it
burrp ~/messy_folder --undo

# 4. Want different model?
burrp ~/messy_folder --model mistral

# 5. Need details?
burrp ~/messy_folder --verbose
```

## Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'ollama'`
**Fix**: Activate venv and run `pip install ollama`

**Issue**: Ollama connection error
**Fix**: Make sure `ollama serve` is running in background

**Issue**: Permission denied
**Fix**: Ensure write access to target folder