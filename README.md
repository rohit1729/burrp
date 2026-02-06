# Burrp

Privacy-focused file organizer using local Ollama models. Burrp scans a folder, categorizes files intelligently, and organizes them into neat folders - all without sending your data to the cloud.

## Features

- **Local AI Processing**: Uses Ollama's gemma3:4b model by default (completely offline)
- **Smart Categorization**: Automatic file type detection with AI fallback for unknown files
- **Privacy First**: No cloud services, no data leaves your machine
- **Dry Run Mode**: Preview changes before organizing
- **Undo Support**: Revert the last 5 operations
- **Configurable**: Custom categories and settings via config file
- **Collision Handling**: Automatically renames duplicate files

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
```bash
# On macOS
brew install ollama
ollama serve &

# Pull the gemma3:4b model
ollama pull gemma3:4b
```

3. Install Burrp:
```bash
pip install -e .
```

## Usage

### Basic Usage

Organize a folder:
```bash
burrp ~/Downloads
```

### Preview Before Organizing

See what will happen without making changes:
```bash
burrp ~/Downloads --dry-run
```

### Undo Last Operation

Revert the last organize operation:
```bash
burrp ~/Downloads --undo
```

Revert all tracked operations:
```bash
burrp ~/Downloads --undo-all
```

### Advanced Options

Use a different Ollama model:
```bash
burrp ~/Downloads --model mistral
```

Use a custom config file:
```bash
burrp ~/Downloads --config /path/to/config.json
```

Verbose logging:
```bash
burrp ~/Downloads --verbose
```

## Configuration

Burrp auto-creates a config file at `~/.config/burrp/config.json` on first run:

```json
{
  "model": "gemma3:4b",
  "categories": {
    "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".cs", ".rb", ".go", ".rs"],
    "Executables": [".exe", ".dmg", ".app", ".sh", ".bat"],
    "Other": []
  },
  "create_subfolders": true,
  "max_history": 5
}
```

You can customize:
- `model`: Your preferred Ollama model
- `categories`: Add or modify file type mappings
- `max_history`: Number of operations to track (for undo)

## How It Works

1. **Scan**: Burrp scans the target folder for files
2. **Categorize**: Files are categorized by extension (fast) or AI (slow)
3. **Organize**: Files are moved into category folders
4. **Track**: Operations are logged for potential undo

## How AI Categorization Works

- Files with known extensions use fast pattern matching
- Unknown files are sent to your local Ollama instance
- Only the filename (not content) is sent to the AI
- The AI categorizes into one of your configured folders

## Privacy

- All processing happens locally on your machine
- Ollama runs locally with `http://localhost:11434`
- Only filenames are sent to the AI (never file contents)
- No external cloud services or APIs
- Config and history stored in `~/.config/burrp/`

## Requirements

- Python 3.7+
- Ollama installed and running
- At least one Ollama model (gemma3 recommended)

## Troubleshooting

**Ollama connection error:**
```bash
# Make sure Ollama is running
ollama serve

# Verify model is available
ollama list
```

**Permission denied:**
```bash
# Make sure you have write permissions
chmod +w /path/to/folder
```

## License

MIT