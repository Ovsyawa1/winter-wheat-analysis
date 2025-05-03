import pandas as pd


def read_and_extract_txt_data(filename):
    # Шаг 1: Определить максимальное число столбцов в текстовом файле
    max_cols = 0
    with open(filename, 'r') as f:
        for line in f:
            cols = line.strip().split("\t")
            if len(cols) > max_cols:
                max_cols = len(cols)
    columns = ['Побег'] + [f'Корень_{i}' for i in range(1, max_cols)]

    # Шаг 2: Создание датафрейма
    df = pd.read_csv(
        filename, sep="\t",
        header=None,
        names=columns,
        skipfooter=1,
    )
    df['Средняя_длина_корня'] = df.iloc[:, 1:].mean(axis=1)
    df['Общая_длина_корневой_системы'] = df.iloc[:, 1:].sum(axis=1)
    return df


def count_germination_rate(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
            # Удаляем потенциальные пустые строки
            lines = [line for line in lines if line]

            if lines:
                germinated_seeds = len(lines) - 1

                # Обработка последней строки
                last_line = lines[-1]
                if last_line.endswith('=0'):
                    try:
                        ungerminated_seeds = int(last_line.split('=')[0])
                    except Exception as e:
                        print(
                            f"Ошибка {e} в формате последней  "
                            f"строки файла {filename}: {last_line}"
                        )
                germination_rate = (
                    germinated_seeds/(ungerminated_seeds + germinated_seeds)
                )

    except UnicodeDecodeError:
        print(
            f"Ошибка чтения файла {filename}: "
            f"неверная кодировка"
        )
    except FileNotFoundError:
        print("Файл не найден")
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {str(e)}")
    
    finally:
        return germination_rate


if __name__ == "__main__":
    df = read_and_extract_txt_data("test.txt")
    germination_rates = count_germination_rate("test.txt")
    mass_transfer = (df['Побег'].mean() / df['Средняя_длина_корня'].mean())
    print(f"Индекс прорастания: {germination_rates}")
    print(f"Переток массы от надземной части в подземную: {mass_transfer}")
    print(df['Общая_длина_корневой_системы'].describe())
    print(df)
    # print(df.head(10))
    # print(df['Общая длина корневой системы'])
    # print(df['Средняя длина корня'].mean())
