import sys
import tempfile
import pytest
from main import main


def create_temp_log(content: str) -> str:
    with tempfile.NamedTemporaryFile("w+", delete=False) as tmp:
        tmp.write(content)
        return tmp.name


@pytest.mark.parametrize("log_lines1, log_lines2, total_expected", [
    (
        ["2025-03-28 12:00:00,000 INFO django.request: GET /a/ 200 OK\n"],
        ["2025-03-28 12:01:00,000 ERROR django.request: Internal Server Error: /a/\n"],
        2
    ),
    (
        ["2025-03-28 12:00:00,000 INFO django.request: GET /multi/ 200 OK\n"],
        ["2025-03-28 12:01:00,000 INFO django.request: GET /multi/ 200 OK\n"],
        2
    ),
])
def test_cli_total_requests(monkeypatch, capsys, log_lines1, log_lines2, total_expected):
    log1 = create_temp_log("".join(log_lines1))
    log2 = create_temp_log("".join(log_lines2))
    monkeypatch.setattr(sys, 'argv', ['main.py', log1, log2, '--report', 'handlers'])
    main()
    output = capsys.readouterr().out
    assert f"Total requests: {total_expected}" in output


@pytest.mark.parametrize("log_lines1, log_lines2, expected_handler", [
    (
        ["2025-03-28 12:00:00,000 INFO django.request: GET /a/ 200 OK\n"],
        ["2025-03-28 12:01:00,000 ERROR django.request: Internal Server Error: /a/\n"],
        "/a/"
    ),
    (
        ["2025-03-28 12:00:00,000 DEBUG django.request: Debug at /b/\n"],
        ["2025-03-28 12:01:00,000 WARNING django.request: Warning at /b/\n"],
        "/b/"
    ),
])
def test_cli_output_contains_handler(monkeypatch, capsys, log_lines1, log_lines2, expected_handler):
    log1 = create_temp_log("".join(log_lines1))
    log2 = create_temp_log("".join(log_lines2))
    monkeypatch.setattr(sys, 'argv', ['main.py', log1, log2, '--report', 'handlers'])
    main()
    output = capsys.readouterr().out
    assert expected_handler in output


@pytest.mark.parametrize("log_lines1, log_lines2, expected_handler", [
    (
        ["2025-03-28 12:00:00,000 INFO django.request: GET /a/ 200 OK\n"],
        ["2025-03-28 12:01:00,000 ERROR django.request: Internal Server Error: /a/\n"],
        "/a/"
    ),
    (
        ["2025-03-28 12:00:00,000 DEBUG django.request: Debug at /b/\n"],
        ["2025-03-28 12:01:00,000 WARNING django.request: Warning at /b/\n"],
        "/b/"
    ),
])
def test_cli_output_contains_handler(monkeypatch, capsys, log_lines1, log_lines2, expected_handler):
    log1 = create_temp_log("".join(log_lines1))
    log2 = create_temp_log("".join(log_lines2))
    monkeypatch.setattr(sys, 'argv', ['main.py', log1, log2, '--report', 'handlers'])
    main()
    output = capsys.readouterr().out
    assert expected_handler in output


@pytest.mark.parametrize("args, expected_exit, expected_output", [
    (['main.py'], True, ""),  # нет аргументов
    (['main.py', '--report', 'handlers'], True, ""),  # нет логов
    (['main.py', 'nonexistent.log', '--report', 'handlers'], False, "Недостающие файлы:"),
    (['main.py', 'fake.log', '--report', 'invalid'], False, "Неизвестный отчет:"),
])
def test_cli_argument_validation(monkeypatch, capsys, args, expected_exit, expected_output):
    monkeypatch.setattr(sys, 'argv', args)

    if expected_exit:
        with pytest.raises(SystemExit):
            main()
    else:
        main()
        output = capsys.readouterr().out
        assert expected_output in output
