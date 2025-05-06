from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import shapiro, probplot
import matplotlib.pyplot as plt


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
        filename,
        sep="\t",
        header=None,
        names=columns,
        skipfooter=1,
        engine="python"
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

    except Exception as e:
        print(f"Ошибка при чтении файла {filename} " + e)

    finally:
        return germination_rate


# Доказательство нормальности распределения контрольных экспериментов
all_values = np.array([])
length_of_shoots = np.array([])


def normality_of_the_distribution_control(directory):
    global all_values
    global length_of_shoots
    text_extensions = {'.txt'}
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    df = read_and_extract_txt_data(item)
                    ''' Рассмотрение средних длин корней '''
                    # sample = df['Средняя_длина_корня'].mean()
                    
                    ''' Рассмотрение индивидуальных корней '''
                    # df = df.drop('Средняя_длина_корня', axis=1)
                    # df = df.drop('Общая_длина_корневой_системы', axis=1)
                    # numpy_values = df.to_numpy().flatten()
                    # numpy_values = numpy_values[~np.isnan(numpy_values)]
                    # all_values = np.append(all_values, numpy_values)

                    ''' Рассмотрение общей длины корней '''
                    numpy_values = df["Общая_длина_корневой_системы"].to_numpy()
                    all_values = np.append(all_values, numpy_values)

                    ''' Рассмотрение длины побегов '''
                    numpy_values = df["Побег"].to_numpy()
                    length_of_shoots = np.append(length_of_shoots, numpy_values)

                    # means_fic.append(sample)
            elif item.is_dir():
                normality_of_the_distribution_control(item)
    except Exception as e:
        print(f"Ошибка при чтении файла: {item}. Ошибка - {e}")
    finally:
        return all_values, length_of_shoots


if __name__ == "__main__":
    all_values, length_of_shoots = normality_of_the_distribution_control(
        # Сюда прописывать путь до папки
        Path("experiments", "control", "45+")
    )

    statistic, p_value = shapiro(all_values)
    print(f"statistic = {statistic}, p_value = {p_value}")

    plt.subplot(2, 2, 1)
    probplot(all_values, dist="norm", plot=plt)
    plt.title('Q-Q Корни')
    
    plt.subplot(2, 2, 2)
    plt.hist(all_values, bins=30, color="orange")
    plt.title("Гистограмма Корни")
    
    plt.subplot(2, 2, 3)
    probplot(length_of_shoots, dist="norm", plot=plt)
    plt.title('Q-Q Побеги')
    
    plt.subplot(2, 2, 4)
    plt.hist(length_of_shoots, bins=30, color="green")
    plt.title('Гистограмма Побеги')
    plt.show()

    # df = read_and_extract_txt_data("test.txt")
    # germination_rates = count_germination_rate("test.txt")
    # mass_transfer = (df['Побег'].mean() / df['Средняя_длина_корня'].mean())
    # print(f"Индекс прорастания: {germination_rates}")
    # print(f"Переток массы от надземной части в подземную: {mass_transfer}")
    # print(df['Общая_длина_корневой_системы'].describe())
    # print(df)
    # print(df.head(10))
    # print(df['Общая длина корневой системы'])
    # print(df['Средняя длина корня'].mean())
