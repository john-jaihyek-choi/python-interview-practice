import json
import logging
from typing import Dict, Any, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler("logs.log")],
)


def load_json_file(filename: str) -> Optional[Dict[str, Dict[str, Any]]]:
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            logging.debug(f"Data retrieved successfully from {filename} - {data}")
            return data
    except FileNotFoundError:
        logging.exception(f"File not found - {filename}")
    except Exception:
        logging.exception(f"Unknown error")


def update_json_data(
    data: Dict[str, Dict[str, Any]], user: str, info: Dict[str, Any]
) -> None:
    try:
        if user not in data:
            data[user] = info
        else:
            data[user].update(info)

        logging.info(f"user, {user}, updated successfully!")
    except Exception:
        logging.exception("Unexpected error occurred")


def save_json_data_to_file(filename: str, data: Dict[str, Any]) -> None:
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        logging.info(f"New data written to {filename}")
    except:
        logging.exception("Unexpected Error")


filename = "users.json"
json_data = load_json_file(filename)

update_json_data(json_data, "Chris", {"age": 10, "sex": "male"})
update_json_data(json_data, "Joey", {"age": 40, "sex": "male"})
update_json_data(json_data, "Isabel", {"age": 30, "sex": "female"})

save_json_data_to_file(filename, json_data)
