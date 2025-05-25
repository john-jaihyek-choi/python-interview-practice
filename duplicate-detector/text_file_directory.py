import logging
import re
from pathlib import Path
from typing import List, Dict, Literal, Optional, Callable
from collections import defaultdict

logger = logging.getLogger(__name__)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="[%(filename)s::%(funcName)s::%(lineno)d] | %(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

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
    4. Print the results to the stdout
"""

MatchType = Literal["exact", "soft", "fuzzy"]


class TextFileDirectory:
    def __init__(self, directory: str):
        self.dir_path = directory

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
        transformer_func = self.__normalize if match_type != "exact" else None
        paragraphs = self.__group_paragraphs_by_file(transformer_func)
        duplicates = self.__filter_duplicates(paragraphs)

        if not duplicates:
            logger.info(f"No duplicates found!")
            return {}

        return duplicates

    def __list_text_files(self) -> List[str]:
        """
        Recursively get txt files from self.dir_path.

        Args:
            None

        Returns:
            List[str]: List of txt files in the given path.
        """

        return [str(file) for file in Path(self.dir_path).rglob("*.txt")]

    # Normalize (redundant spaces removal) string
    def __normalize(self, string: str) -> str:
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

    # Extract paragraphs from a single file
    def __extract_paragraphs(self, file_path: str) -> List[str]:
        """
        Extracts all normalized paragraphs from a file.

        Args:
            file_path (str): Path to the txt files.

        Returns:
            List[str]: List of normalized paragraphs strings.
        """

        if file_path is None:
            raise TypeError("file_path should be non-None and string argument")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = re.split(
            r"\n\s*\n", content.strip()
        )  # split paragraphs - delimiter == \n

        return [paragraph for paragraph in content]

    def __filter_duplicates(self, paragraphs: Dict[str, set]) -> Dict[str, List[str]]:
        """
        Filters duplicating paragraphs

        Args:
            paragraphs (Dict[str, set]): Paragraph-file mapping

        Returns:
            Dict[str, set]: Paragraphs that are duplicates across files
        """
        return {
            paragraph: sorted(files)
            for paragraph, files in paragraphs.items()
            if len(files) > 1
        }

    def __group_paragraphs_by_file(
        self, transform: Optional[Callable[[str], str]] = None
    ) -> Dict[str, set]:
        """
        Group all unique paragraphs by file

        Args:
            transform (Callable[[str], str]): Desired transformation function. None by default

        Returns:
            Dict[str,set]: Dictionary of paragraph-files pair.
        """

        files = self.__list_text_files()

        if not files:
            logger.warning(f"No files found in {self.dir_path}")
            return {}

        paragraphs: Dict[str, set] = defaultdict(set)

        for file in files:
            for paragraph in self.__extract_paragraphs(file_path=file):
                p = transform(paragraph) if transform else paragraph
                paragraphs[p].add(Path(file).name)

        return paragraphs
