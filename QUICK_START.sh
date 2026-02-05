#!/bin/bash
# Burrp Quick Start Script

echo "Burrp - File Organizer with Local AI"
echo "===================================="
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is available
if ! command -v ollama &> /dev/null; then
    echo "Error: Ollama not found. Install with: brew install ollama"
    exit 1
fi

# Check if gemma3 model is available
if ! ollama list | grep -q "gemma3"; then
    echo "Pulling gemma3 model..."
    ollama pull gemma3
fi

echo "Burrp is ready!"
echo ""
echo "Usage:"
echo "  burrp <folder>                 - Organize folder"
echo "  burrp <folder> --dry-run      - Preview changes"
echo "  burrp <folder> --verbose       - Show details"
echo "  burrp <folder> --undo         - Undo last operation"
echo "  burrp <folder> --undo-all     - Undo all operations"
echo ""
echo "Example:"
echo "  burrp ~/Downloads"
echo ""
