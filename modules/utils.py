import datetime
import json
import os
from typing import Union, Dict, List
import uuid

OUTPUT_DIR = "output"


def build_file_path(name: str):
    session_dir = f"{OUTPUT_DIR}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def build_file_name_session(name: str, session_id: str):
    session_dir = f"{OUTPUT_DIR}/{session_id}"
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{name}")


def to_json_file_pretty(name: str, content: Union[Dict, List]):
    def default_serializer(obj):
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        raise TypeError(
            f"Object of type {obj.__class__.__name__} is not JSON serializable"
        )

    with open(f"{name}.json", "w") as outfile:
        json.dump(content, outfile, indent=2, default=default_serializer)


def current_date_time_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def current_date_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d")


def dict_item_diff_by_set(
    previous_list: List[Dict], current_list: List[Dict], set_key: str
) -> List[str]:
    previous_set = {item[set_key] for item in previous_list}
    current_set = {item[set_key] for item in current_list}
    return list(current_set - previous_set)


def create_session_logger_id() -> str:
    return (
        datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
    )


import logging

def setup_logging(session_id: str):
    """Configure logging with session-specific log file"""
    log_file = build_file_name_session("session.log", session_id)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def parse_markdown_backticks(str) -> str:
    if "```" not in str:
        return str.strip()
    # Remove opening backticks and language identifier
    str = str.split("```", 1)[-1].split("\n", 1)[-1]
    # Remove closing backticks
    str = str.rsplit("```", 1)[0]
    # Remove any leading or trailing whitespace
    return str.strip()
