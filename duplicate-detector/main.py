import logging
import os
import re
import argparse
import json
from pathlib import Path
from typing import List, Dict
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


# 1. Locate .txt files from the data directory
def get_text_files(path: str) -> List[str]:
    """
    Recursively get txt files from a given directory.

    Args:
        path (str): Path to the txt files directory.

    Returns:
        List[str]: List of txt files in the given path.
    """
    try:
        files = [str(file) for file in Path(path).rglob("*.txt")]
        return files
    except FileNotFoundError:
        logging.exception(f"Directory {path} does not exist!")
        return []
    except Exception as e:
        logging.exception(f"Unexpected failure getting text files from {path}: {e}")
        return []


# 2. Extract pragraphs from the file
def extract_paragraphs(file_path: str) -> List[str]:
    """
    Extracts all normalized paragraphs from a file.

    Args:
        file_path (str): Path to the txt files.

    Returns:
        List[str]: List of normalized paragraphs strings.
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()

        return [
            normalize_string(paragraph)
            for paragraph in re.split(r"\n\s*\n", content.strip())
        ]
    except Exception as e:
        logging.exception(
            f"Unexpected failure extracting paragraphs from {file_path}: {e}"
        )
        return []


def normalize_string(string: str) -> str:
    """
    Normalizes a given string: lowercase conversion and redundant spacing removal.

    Args:
        string (str): Paragraph string to normalize.

    Returns:
        str: Normalized paragraph.
    """
    return re.sub(r"\s+", " ", string.lower())


# 3. Collect extracted paragraphs
def group_paragraphs(data_dir_path: str) -> Dict[str, set]:
    """
    Groups every paragraph from files in to a dictionary.

    Args:
        data_dir_path (str): Path of the directory that contains text files.

    Returns:
        Dict[str,set]: Dictionary of paragraph-files pair.
    """

    files = get_text_files(data_dir_path)

    if not files:
        logging.warning(f"No files found in {data_dir_path}")
        return {}

    detected = defaultdict(set)

    for file in files:
        for paragraph in extract_paragraphs(file):
            detected[paragraph].add(Path(file).name)

    return detected


# 4. Report duplicates
def output_duplicates(
    paragraph_collection: Dict[str, set],
    files_found_in_count: int,
    output_dst: str = None,
) -> None:
    """
    Print duplicates to stdout OR write the results to a defined output destination.

    Args:
        paragraph_collection (Dict[str, set]): Dictionary of paragraph-files pair.
        files_found_in_count (int): Threshold for duplicates.
        output_dst (str): Path to a file an output would be written to.

    Returns:
        None
    """

    duplicates = {
        paragraph: sorted(files)
        for paragraph, files in paragraph_collection.items()
        if len(files) >= files_found_in_count
    }

    if not duplicates:
        print(f"No duplicates found!")

    if output_dst:
        try:
            with open(output_dst, "w", encoding="utf-8") as file:
                json.dump(duplicates, file, indent=4)
            print(f"Duplicates written to {output_dst}")
        except Exception:
            logging.exception(f"Failed to write output to {output_dst}")
    else:
        for paragraph, files in duplicates.items():
            if len(files) >= files_found_in_count:
                print(
                    f"Duplicate Paragraph: {paragraph}\n", f"-> Found in: {list(files)}"
                )


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
        "-th",
        "--threshold",
        default=1,
        type=int,
        help="Number of files that contain duplicates to be detected as duplicate",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Optional path to save results as JSON"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    paragraphs = group_paragraphs(args.dir)

    output_duplicates(paragraphs, args.threshold, args.output)
