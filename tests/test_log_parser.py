import tempfile
import pytest
from parser.log_parser import parse_log_file


def parse_from_log_content(content: str):
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    return parse_log_file(tmp_path)


@pytest.mark.parametrize("log_line, expected_path, expected_level", [
    ("2025-03-28 12:00:00,000 INFO django.request: GET /info/ 200 OK", "/info/", "INFO"),
    ("2025-03-28 12:01:00,000 DEBUG django.request: Debug: /debug/", "/debug/", "DEBUG"),
    ("2025-03-28 12:02:00,000 WARNING django.request: Warning: /warn/", "/warn/", "WARNING"),
    ("2025-03-28 12:03:00,000 ERROR django.request: Error: /error/", "/error/", "ERROR"),
    ("2025-03-28 12:04:00,000 CRITICAL django.request: Crash: /critical/", "/critical/", "CRITICAL"),
])
def test_parse_log_file_extracts_levels_correctly(log_line, expected_path, expected_level):
    result = parse_from_log_content(log_line)
    assert result[expected_path][expected_level] == 1


@pytest.mark.parametrize("log_line, expected_path, expected_level", [
    ("2025-03-28 12:00:00,000 INFO django.request: GET /login 200 OK", "/login", "INFO"),
    ("2025-03-28 12:01:00,000 INFO django.request: GET /login/ 200 OK", "/login/", "INFO"),
])
def test_log_parser_treats_paths_with_and_without_trailing_slash_differently(log_line, expected_path, expected_level):

    result = parse_from_log_content(log_line)

    assert result[expected_path][expected_level] == 1


@pytest.mark.parametrize("log_line", [
    "2025-03-28 12:00:00,000 INFO django.security: Something unrelated",
    "2025-03-28 12:01:00,000 DEBUG django.db.backends: Querying",
    "2025-03-28 12:02:00,000 WARNING some.other.module: Noise",
])
def test_parse_log_file_ignores_non_request_lines(log_line):
    result = parse_from_log_content(log_line)
    assert result == {}


@pytest.mark.parametrize("log_line", [
    "",
    "garbage line with no structure",
    "2025-03-28 12:00:00,000 INFO NotMatching django.request",
])
def test_log_parser_handles_invalid_lines_gracefully(log_line):
    result = parse_from_log_content(log_line)
    assert result == {}
