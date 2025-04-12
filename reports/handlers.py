from typing import Dict, List
from collections import defaultdict

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class HandlersReport:
    def generate(self, data_list: List[Dict[str, Dict[str, int]]]) -> str:
        combined = defaultdict(lambda: defaultdict(int))
        total_requests = 0

        for data in data_list:
            for handler, level_counts in data.items():
                for level in LOG_LEVELS:
                    combined[handler][level] += level_counts.get(level, 0)
                    total_requests += level_counts.get(level, 0)

        output = [f"\nTotal requests: {total_requests}\n"]
        header = f"{'HANDLER':<24}" + "".join(f"{lvl:<8}" for lvl in LOG_LEVELS)
        output.append(header)

        for handler in sorted(combined.keys()):
            row = f"{handler:<24}"
            for level in LOG_LEVELS:
                row += f"{combined[handler][level]:<8}"
            output.append(row)

        footer = " " * 24
        for level in LOG_LEVELS:
            level_sum = sum(combined[handler][level] for handler in combined)
            footer += f"{level_sum:<8}"
        output.append(footer)

        return "\n".join(output)
