# Burrp Command Reference

## Setup Commands

```bash
# One-time setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

```bash
# Preview organization (recommended first)
burrp ~/Downloads --dry-run

# Organize folder
burrp ~/Downloads

# Undo last operation
burrp ~/Downloads --undo
```

## All Flags

| Flag | Description |
|------|-------------|
| `--model <name>` | Use different Ollama model (default: gemma3) |
| `--dry-run` | Preview changes without moving files |
| `--verbose` | Show detailed logging |
| `--undo` | Revert last operation |
| `--undo-all` | Revert all tracked operations |
| `--config <path>` | Use custom config file path |

## Examples

```bash
# Preview and organize Downloads
burrp ~/Downloads --dry-run
burrp ~/Downloads

# Organize with verbose output
burrp ~/Desktop/myfiles --verbose

# Use different model
burrp ~/Downloads --model mistral

# Undo all recent operations
burrp ~/Downloads --undo-all
```

## Testing

```bash
# Run unit tests
source venv/bin/activate
python -m burrp.tests.test_burrp
```

## Ollama Models Available

Run `ollama list` to see installed models:
- gemma3:4b (default, fast)
- deepseek-r1:14b (larger, more capable)
- llama2:latest (classic)

Pull new models:
```bash
ollama pull <model-name>
```

## Config File

Auto-created at: `~/.config/burrp/config.json`

You can customize:
- Default Ollama model
- File category mappings
- History size (max 5 by default)
