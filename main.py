import argparse
import os
from reports.handlers import HandlersReport
from parser.log_parser import parse_log_file


def main():
    parser = argparse.ArgumentParser(description="Анализатор логов Django")
    parser.add_argument("log_files", nargs="+", help="Пути к файлам логов")
    parser.add_argument("--report", required=True, help="Имя генерируемого отчета")

    args = parser.parse_args()

    if args.report != "handlers":
        print(f"Неизвестный отчет: {args.report}")
        return

    missing_files = [file for file in args.log_files if not os.path.exists(file)]
    if missing_files:
        print("Недостающие файлы:", ", ".join(missing_files))
        return

    all_data = []
    for file_path in args.log_files:
        data = parse_log_file(file_path)
        all_data.append(data)

    report = HandlersReport()
    result = report.generate(all_data)
    print(result)


if __name__ == "__main__":
    main()
