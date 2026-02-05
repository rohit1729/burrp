# Burrp Project Plan

## Overview
Burrp is a local Python CLI tool that organizes files in a folder using local Ollama models for intelligent categorization. Privacy-focused - all processing done locally.

## Core Features

### 1. File Organization
- Scan target folder for files
- Categorize files by extension (fast path)
- Use local gemma3 model for unknown files
- Move files to appropriate folders
- Handle filename collisions with counter suffix

### 2. CLI Arguments
```bash
burrp <folder> [options]

Options:
  --model <name>       Ollama model (default: gemma3)
  --dry-run           Preview changes without moving files
  --verbose           Show detailed log
  --undo              Revert last operation
  --undo-all          Revert all tracked operations
  --config <path>     Custom config file path
```

### 3. Configuration (.burrprc)
- Auto-created in: `~/.config/burrp/config.json`
- Contains model preference, category mappings, settings

```json
{
  "model": "gemma3",
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

### 4. Undo Functionality
- History stored in: `~/.config/burrp/history.json`
- Tracks last 5 operations
- Each operation includes: timestamp, list of moves
- `--undo` reverses last operation
- `--undo-all` reverses all tracked operations
- Cleans up empty folders after undo

## Project Structure
```
burrp/
├── burrp.py              # Main CLI tool
├── requirements.txt      # Dependencies
├── README.md            # Documentation
├── setup.py             # Package setup
└── tests/
    └── test_burrp.py    # Unit tests
```

## Implementation Details

### Priority Order
1. CLI arguments
2. Config file
3. Built-in defaults

### Undo History Format
```json
[
  {
    "timestamp": "2026-02-05T14:30:00",
    "operations": [
      {"source": "/path/file.txt", "dest": "/path/Documents/file.txt"}
    ]
  }
]
```

### Dry-run Output Example
```
Would move: image1.png -> Images/
Would move: notes.pdf -> Documents/
Would skip: existing_folder/
```

### Error Handling
- Check folder existence
- Handle permission errors
- Graceful fallback if Ollama unavailable
- Log issues without stopping

### Safety Features
- Validate Ollama connection before use
- Auto-create config if missing
- Track maximum 5 operations (FIFO)