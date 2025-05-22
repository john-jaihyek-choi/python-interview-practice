import logging
import argparse
import json
from typing import Dict
from text_file_directory import TextFileDirectory

logging.basicConfig(
    level=logging.INFO,
    format="[%(filename)s::%(funcName)s::%(lineno)d] | %(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


# Parse CLI arguments
def parse_args() -> None:
    """
    Parses arguments for script to run on CLI.

    Args:
        None

    Return:
        Parser
    """
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
                f"-> Found in: {files}",
            )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                json.dump(duplicates, file, indent=4)

            print(f"Duplicates written to {args.output}")

    except Exception as e:
        logging.exception(f"Unexpected error detecting duplicate paragraphs: {e}")
