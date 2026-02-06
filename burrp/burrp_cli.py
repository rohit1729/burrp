#!/usr/bin/env python3
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
from ollama import Client
import logging


class Burrp:
    def __init__(self, target_folder, model=None, config_path=None, verbose=False):
        self.target_folder = Path(target_folder)
        self.config_dir = Path.home() / ".config" / "burrp"
        self.config_file = (
            Path(config_path) if config_path else self.config_dir / "config.json"
        )
        self.history_file = self.config_dir / "history.json"
        self.ai_log_file = self.config_dir / "ai_interactions.log"
        self.verbose = verbose

        # Set up AI interaction logging
        self._setup_ai_logger()

        self.defaults = {
            "model": "gemma3:4b",
            "categories": {
                "Images": [
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".bmp",
                    ".svg",
                    ".webp",
                    ".ico",
                ],
                "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"],
                "Spreadsheets": [".xls", ".xlsx", ".csv"],
                "Presentations": [".ppt", ".pptx"],
                "Audio": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"],
                "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
                "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
                "Code": [
                    ".py",
                    ".js",
                    ".html",
                    ".css",
                    ".java",
                    ".cpp",
                    ".cs",
                    ".rb",
                    ".go",
                    ".rs",
                ],
                "Executables": [".exe", ".dmg", ".app", ".sh", ".bat"],
                "Other": [],
            },
            "create_subfolders": True,
            "max_history": 5,
        }

        self.config = self._load_config()
        self.model = model or self.config.get("model", "gemma3:4b")
        self.categories = self.config.get("categories", self.defaults["categories"])

        self.client = Client(host="http://localhost:11434")
        self._ensure_config_exists()

    def _setup_ai_logger(self):
        """Set up logging for AI interactions to a separate file"""
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Create a separate logger for AI interactions
        self.ai_logger = logging.getLogger("burrp_ai")
        self.ai_logger.setLevel(logging.INFO)

        # Remove any existing handlers
        self.ai_logger.handlers = []

        # Create file handler
        fh = logging.FileHandler(self.ai_log_file)
        fh.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        fh.setFormatter(formatter)

        # Add handler to logger
        self.ai_logger.addHandler(fh)

        # Prevent propagation to root logger
        self.ai_logger.propagate = False

    def _ensure_config_exists(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self.config_file.write_text(json.dumps(self.defaults, indent=2))
            if self.verbose:
                print(f"Created config at {self.config_file}")

    def _load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self.defaults.copy()

    def _load_history(self):
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []

    def _save_history(self, history):
        config_dir = self.config_dir
        history_file = self.history_file

        config_dir.mkdir(parents=True, exist_ok=True)

        max_history = self.config.get("max_history", 5)
        history = history[-max_history:]

        history_file.write_text(json.dumps(history, indent=2))

    def _get_category(self, filename):
        # ext = Path(filename).suffix.lower()

        # for category, extensions in self.categories.items():
        #     if ext in extensions:
        #         return category

        try:
            prompt = f"""Categorize the file "{filename}" into one of these folders: {", ".join(self.categories.keys())}. Return only the folder name, nothing else."""

            # Log the prompt being sent to AI
            self.ai_logger.info(f"\n{'=' * 80}")
            self.ai_logger.info(f"FILE: {filename}")
            self.ai_logger.info(f"MODEL: {self.model}")
            self.ai_logger.info(f"PROMPT: {prompt}")

            response = self.client.chat(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )

            category = response["message"]["content"].strip()

            # Log the AI response
            self.ai_logger.info(f"RAW RESPONSE: {response['message']['content']}")
            self.ai_logger.info(f"CATEGORIZED AS: {category}")
            self.ai_logger.info(f"VALID: {category in self.categories}")

            if category in self.categories:
                return category
        except Exception as e:
            self.ai_logger.error(f"ERROR: {str(e)}")
            if self.verbose:
                print(f"Warning: Could not categorize {filename}: {e}")

        self.ai_logger.info(f"FINAL CATEGORY: Other (fallback)")
        return "Other"

    def organize(self, dry_run=False):
        if not self.target_folder.exists():
            print(f"Error: Folder '{self.target_folder}' does not exist")
            return False

        print(f"Organizing files in: {self.target_folder}")
        print(f"Model: {self.model}")
        print(f"Dry run: {'YES' if dry_run else 'NO'}")
        print(f"AI Log: {self.ai_log_file}")
        print("-" * 50)

        files_moved = 0
        files_skipped = 0
        operations = []

        for item in self.target_folder.iterdir():
            if item.is_file():
                category = self._get_category(item.name)
                category_folder = self.target_folder / category

                if not dry_run:
                    category_folder.mkdir(exist_ok=True)

                destination = category_folder / item.name

                counter = 1
                while destination.exists():
                    stem = item.stem
                    ext = item.suffix
                    destination = category_folder / f"{stem}_{counter}{ext}"
                    counter += 1

                source_path = str(item)
                dest_path = str(destination)

                if dry_run:
                    print(f"Would move: {item.name} -> {category}/")
                else:
                    shutil.move(source_path, dest_path)
                    print(f"Moved: {item.name} -> {category}/")
                    operations.append({"source": source_path, "dest": dest_path})

                files_moved += 1
            else:
                files_skipped += 1

        print("-" * 50)
        print(f"Organized {files_moved} files")
        print(f"Skipped {files_skipped} folders")

        if operations and not dry_run:
            history = self._load_history()
            history.append(
                {"timestamp": datetime.now().isoformat(), "operations": operations}
            )
            self._save_history(history)
            print(f"Operation saved to history")

        return True

    def undo(self, undo_all=False):
        history = self._load_history()

        if not history:
            print("No operations to undo")
            return False

        if undo_all:
            operations_to_undo = list(reversed(history))
            history.clear()
        else:
            operations_to_undo = [history.pop()]

        print(f"Reverting {'all' if undo_all else 'last'} operation(s)...")
        print("-" * 50)

        reverted = 0
        for entry in operations_to_undo:
            for op in reversed(entry["operations"]):
                source = Path(op["dest"])
                dest = Path(op["source"])

                if source.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(dest))
                    print(f"Reverted: {source.name} -> {dest.parent.name}/")
                    reverted += 1

        empty_folders = [
            p
            for p in self.target_folder.glob("*")
            if p.is_dir() and not any(p.iterdir())
        ]
        for folder in empty_folders:
            folder.rmdir()
            print(f"Removed empty folder: {folder.name}")

        self._save_history(history)

        print("-" * 50)
        print(f"Reverted {reverted} files")
        return True


def main():
    parser = ArgumentParser(description="Burrp - Organize your files with local AI")
    parser.add_argument("folder", help="Folder to organize")
    parser.add_argument("--model", help="Ollama model to use (default: gemma3:4b)")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without moving files"
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed logging")
    parser.add_argument("--undo", action="store_true", help="Revert last operation")
    parser.add_argument(
        "--undo-all", action="store_true", help="Revert all tracked operations"
    )
    parser.add_argument("--config", help="Path to config file")

    args = parser.parse_args()

    burrp = Burrp(
        args.folder, model=args.model, config_path=args.config, verbose=args.verbose
    )

    if args.undo or args.undo_all:
        burrp.undo(undo_all=args.undo_all)
    else:
        burrp.organize(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
