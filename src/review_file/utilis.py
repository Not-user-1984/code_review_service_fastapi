import pycodestyle


def run_code_review(file_content: str) -> str:
    # Создаем объект Pycodestyle
    style_checker = pycodestyle.StyleGuide()
    # Выполняем проверку стиля для переданного содержимого файла
    report = style_checker.check_data(file_content)
    # Создаем строку с результатами проверки
    result = f"Total errors: {report.total_errors}\n"
    for code, message, line_number, _ in report.get_statistics():
        result += f"Line {line_number}: [{code}] {message}\n"
    return result