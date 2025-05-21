import logging
import os
import re
import argparse
import json
from pathlib import Path
from typing import List, Dict, Literal, Optional, Callable
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

"""
Problem Statement:
    You're given a directory of .txt files. Each file contains plain-text paragraphs, separated by blank lines.

    Goal: Write a program that detects all paragraphs that appear in two or more files and report which files they appear in.

    Paragraphs should be treated as the same if their content is the same, ignoring:
        - leading/trailing whitespace
        - case differences
        - redundant spaces within a paragraph

    Feel free to structure your code however you prefer. You're welcome to write helper methods, classes, or test cases.
"""

"""
Note:
    - directory of .txt files
    - file contains plain-text paragraphs
        - separated by blank lines
    - Duplicates:
        - ignore leading/trailing whitespaces
        - case insensitive
        - ignore redundant spaces
    - Goal:
        - Program to detect all paragraphs that appear in two or more files
            - Then report which files they appear in
        - example output:
            - "Paragraph1": [file1.txt, file2.txt, ...]
            - "Paragraph2": [file2.txt, file3.txt, ...]

Problem Breakdown:
    1. Locate all .txt files from the "data/" directory
        - Q: could there be nested sub-directories containing txt files?
    2. Extract paragraphs from each file, delimited by blank line (\n)
        - Normalize paragraphs when extracting
    3. Store extracted paragraph to a dictionary
        - Note:
            - store extracted paragraph as a KEY, file being extracted from as a value
    4. Report the result
        - iterate on the stored paragraph-file relation and 
"""

MatchType = Literal["exact", "soft", "fuzzy"]


class TextFileDirectory:
    def __init__(self, directory: str):
        self.dir_path = directory

    # 1. Locate .txt files from the data directory
    def _list_text_files(self) -> List[str]:
        """
        Recursively get txt files from self.dir_path.

        Args:
            None

        Returns:
            List[str]: List of txt files in the given path.
        """

        return [str(file) for file in Path(self.dir_path).rglob("*.txt")]

    # 2. Extracts all paragraphs from a single file
    def _extract_paragraphs(self, file_path: str) -> List[str]:
        """
        Extracts all normalized paragraphs from a file.

        Args:
            file_path (str): Path to the txt files.

        Returns:
            List[str]: List of normalized paragraphs strings.
        """

        if file_path is None:
            raise TypeError("file_path should be non-None and string argument")

        with open(file_path, "r") as file:
            content = file.read()

        content = re.split(
            r"\n\s*\n", content.strip()
        )  # split paragraphs - delimiter == \n

        return [paragraph for paragraph in content]

    def _normalize(self, string: str) -> str:
        """
        Normalizes a given string: lowercase conversion and redundant spacing removal.

        Args:
            string (str): Paragraph string to normalize.

        Returns:
            str: Normalized paragraph.
        """
        if string is None:
            raise TypeError("Expected a non-None string as argument")

        if not isinstance(string, str):
            string = str(string)

        return re.sub(
            r"\s+", " ", string.lower().strip()
        )  # remove redundant spaces from a string

    # 3. Identifies duplicate paragraphs
    def group_paragraphs_by_file(
        self, transform: Optional[Callable[[str], str]]
    ) -> Dict[str, set]:
        """
        Group all unique paragraphs by file

        Args:
            transform (Callable[[str], str]): Boolean value for paragraph normalization

        Returns:
            Dict[str,set]: Dictionary of paragraph-files pair.
        """

        files = self._list_text_files()

        if not files:
            logging.warning(f"No files found in {self.dir_path}")
            return {}

        paragraphs: Dict[str, set] = defaultdict(set)

        for file in files:
            for paragraph in self._extract_paragraphs(file_path=file):
                p = transform(paragraph) if transform else paragraph
                paragraphs[p].add(Path(file).name)

        return paragraphs

    def _filter_duplicates(self, paragraphs: Dict[str, set]) -> Dict[str, set]:

        return {
            paragraph: sorted(files)
            for paragraph, files in paragraphs.items()
            if len(files) > 1
        }

    # 4. Report duplicates
    def find_duplicates(self, match_type: MatchType = "soft") -> Dict[str, set]:
        """
        Finds and returns duplicating paragraph-file key-val pair.

        Args:
            match_type ("soft"|"exact"|"fuzzy"): match type to detect duplicates

        Returns:
            Dict[str,set]: Dictionary containing paragraphs and the file locations
        """

        if match_type == "fuzzy":
            raise NotImplementedError("Fuzzy filter not implemented yet...")

        # use internal normalizer if "soft" or "fuzzy"
        transformer_func = self._normalize if match_type != "exact" else None
        paragraphs = self.group_paragraphs_by_file(transformer_func)
        duplicates = self._filter_duplicates(paragraphs)

        if not duplicates:
            logging.info(f"No duplicates found!")
            return {}

        return duplicates


# Parse CLI arguments
def parse_args() -> None:
    parser = argparse.ArgumentParser(
        description="Detect duplicate paragraphs across .txt files"
    )
    parser.add_argument(
        "-d",
        "--dir",
        default="data/",
        type=str,
        help="Path to the directory that contains the .txt files",
    )
    parser.add_argument(
        "-m",
        "--match",
        default="soft",
        type=str,
        help="Match type to detect duplicates",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Optional path to save results as JSON"
    )
    return parser.parse_args()


if __name__ == "__main__":
    try:
        args = parse_args()
        text_file_directory = TextFileDirectory(args.dir)
        duplicates: Dict[str, set] = text_file_directory.find_duplicates(
            match_type=args.match
        )

        for paragraph, files in duplicates.items():
            print(
                f"Duplicate Paragraph: {paragraph}\n",
                f"-> Found in: {list(files)}",
            )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                json.dump(duplicates, file, indent=4)
            print(f"Duplicates written to {args.output}")

    except Exception as e:
        logging.exception(f"Unexpected error detecting duplicate paragraphs: {e}")
