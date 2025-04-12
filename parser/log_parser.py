import re
from typing import Dict
from collections import defaultdict

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LEVEL_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} (?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL) django\.request: .*"
)

PATH_PATTERN = re.compile(r"(/[\w\-/]+)")


def parse_log_file(path: str) -> Dict[str, Dict[str, int]]:
    result = defaultdict(lambda: defaultdict(int))

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            level_match = LEVEL_PATTERN.search(line)
            if level_match:
                level = level_match.group("level")
                path_match = PATH_PATTERN.search(line)
                if path_match:
                    handler = path_match.group(1)
                    result[handler][level] += 1

    return result
