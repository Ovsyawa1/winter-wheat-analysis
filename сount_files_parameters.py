from pathlib import Path


def count_text_files(directory):
    """
    Рекурсивно подсчитывает количество текстовых файлов в указанной директории
    и всех её подпапках.

    Args:
        directory (str): Путь к директории для поиска.

    Returns:
        int: Количество найденных текстовых файлов
    """
    text_extensions = {'.txt'}
    count = 0

    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    count += 1
            elif item.is_dir():
                count += count_text_files(item)
        return count
    except FileNotFoundError:
        print(f"Директория {directory} не найдена")
        return 0


def count_lines_in_text_files(directory):
    """
    Рекурсивно подсчитывает общее количество строк во всех текстовых файлах
    в указанной директории и её подпапках.

    Args:
        directory (str): Путь к директории для поиска.

    Returns:
        int: Общее количество строк во всех текстовых файлах
    """
    text_extensions = {'.txt'}
    total_lines = 0

    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    try:
                        with open(item, 'r', encoding='utf-8') as file:
                            total_lines += sum(1 for _ in file)
                    except UnicodeDecodeError:
                        print(
                            f"Ошибка чтения файла {item}: "
                            f"неверная кодировка"
                        )
                    except Exception as e:
                        print(f"Ошибка при чтении файла {item}: {str(e)}")
            elif item.is_dir():
                total_lines += count_lines_in_text_files(item)
        return total_lines
    except FileNotFoundError:
        print(f"Директория {directory} не найдена")
        return 0


def count_experiments(directory):
    """
    Рекурсивно подсчитывает общее количество экспериментов во всех текстовых
    файлах в указанной директории и её подпапках.

    Args:
        directory (str): Путь к директории для поиска.

    Returns:
        int: Общее количество экспериментов
    """
    text_extensions = {'.txt'}
    total_experiments = 0
    total_lines = 0

    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    try:
                        with open(item, 'r', encoding='utf-8') as file:
                            lines = [line.strip() for line in file.readlines()]
                            # Удаляем потенциально пустые строки
                            lines = [line for line in lines if line]

                            if lines:
                                total_lines += len(lines)
                                # Подсчет строк, кроме последней
                                file_experiments = len(lines) - 1

                                # Обработка последней строки
                                last_line = lines[-1]
                                if last_line.endswith('=0'):
                                    try:
                                        x_value = int(last_line.split('=')[0])
                                        file_experiments += x_value
                                    except (ValueError, IndexError):
                                        print(
                                            f"Ошибка в формате последней "
                                            f"строки файла {item}: {last_line}"
                                        )

                                total_experiments += file_experiments

                    except UnicodeDecodeError:
                        print(
                            f"Ошибка чтения файла {item}: "
                            f"неверная кодировка"
                        )
                    except FileNotFoundError:
                        print("Файл не найден")
                    except Exception as e:
                        print(f"Ошибка при чтении файла {item}: {str(e)}")

            elif item.is_dir():
                sub_experiments = count_experiments(item)
                # Проверяем, что результат не None
                if sub_experiments is not None:
                    total_experiments += sub_experiments
        return total_experiments
    except FileNotFoundError:
        print(f"Директория {directory} не найдена")
        return 0


if __name__ == "__main__":
    dir_name = "diploma"
    files_count = count_text_files(dir_name)
    lines_count = count_lines_in_text_files(dir_name)
    experiments_count = count_experiments(dir_name)
    print(f"Количество текстовых файлов в папке diploma {files_count}")
    print(f"Общее количество строк во всех текстовых файлах: {lines_count}")
    print(f"Общее количество экспериментов: {experiments_count}")
