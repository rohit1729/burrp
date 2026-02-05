import unittest
import tempfile
import shutil
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from burrp import Burrp


class TestBurrp(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

        self.config_dir = Path.home() / ".config" / "burrp"
        self.original_config = None
        if self.config_dir.exists():
            config_file = self.config_dir / "config.json"
            if config_file.exists():
                with open(config_file) as f:
                    self.original_config = f.read()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

        if self.original_config is not None:
            config_file = self.config_dir / "config.json"
            with open(config_file, "w") as f:
                f.write(self.original_config)

    def test_init_creates_config(self):
        burrp = Burrp(self.temp_dir, verbose=False)
        config_dir = Path.home() / ".config" / "burrp"
        config_file = config_dir / "config.json"

        self.assertTrue(config_file.exists())

        with open(config_file) as f:
            config = json.load(f)

        self.assertIn("model", config)
        self.assertIn("categories", config)

    def test_empty_folder(self):
        burrp = Burrp(self.temp_dir, verbose=False)
        result = burrp.organize(dry_run=True)

        self.assertTrue(result)

    def test_no_target_folder(self):
        non_existent = Path(self.temp_dir) / "non_existent"
        burrp = Burrp(str(non_existent), verbose=False)
        result = burrp.organize(dry_run=True)

        self.assertFalse(result)

    def test_dry_run_creates_no_folders(self):
        test_file = self.temp_path / "test.txt"
        test_file.write_text("test")

        burrp = Burrp(self.temp_dir, verbose=False)
        burrp.organize(dry_run=True)

        documents_folder = self.temp_path / "Documents"
        self.assertFalse(documents_folder.exists())
        self.assertTrue(test_file.exists())


if __name__ == "__main__":
    unittest.main()
