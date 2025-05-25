import unittest
import tempfile
import shutil
import logging
from pathlib import Path
from text_file_directory import TextFileDirectory


class TestTextFileDirectory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.data_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.data_dir)

    def test_find_duplicates_exact_match(self):
        (Path(self.data_dir) / "file1.txt").write_text(
            "This paragraph should match with file2\n\nTHIS PARAGRAPH SHOULD NOT"
        )
        (Path(self.data_dir) / "file2.txt").write_text(
            "THIS IS A UNIQUE PARAGRAPH\n\nThis paragraph should match with file2"
        )
        self.text_file_directory = TextFileDirectory(self.data_dir)

        test = self.text_file_directory.find_duplicates(match_type="exact")
        expected = {
            "This paragraph should match with file2": ["file1.txt", "file2.txt"]
        }

        self.assertEqual(test, expected)

    def test_find_duplicates_no_contents(self):
        self.text_file_directory = TextFileDirectory(self.data_dir)

        test = self.text_file_directory.find_duplicates()
        expected = {}

        self.assertEqual(test, expected)

    def test_find_duplicates_soft_match(self):
        (Path(self.data_dir) / "file1.txt").write_text(
            " This paragraph  has  many redundant spaces..."
        )
        (Path(self.data_dir) / "file2.txt").write_text(
            "   This paragraph has many redundant spaces..."
        )
        self.text_file_directory = TextFileDirectory(self.data_dir)

        test = self.text_file_directory.find_duplicates()
        expected = {
            "this paragraph has many redundant spaces...": ["file1.txt", "file2.txt"]
        }

        self.assertEqual(test, expected)


if __name__ == "__main__":
    unittest.main()
