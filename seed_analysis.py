from pathlib import Path
import logging
import re
import numpy as np
import pandas as pd
from scipy.stats import (
    shapiro, tukey_hsd, f_oneway, levene
)

from draw_graphs import (
    draw_control_roots, draw_germination_rates, draw_qq_histograms
)
from read_txt_data import read_and_extract_txt_data


''' Объявление логгера для Контроля '''
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('conrol_statistics.log', mode='w')
    ],
)
logger = logging.getLogger('control_tests')


def count_germination_rate(filename):
    ''' Расчет всхожести '''
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
# all_values = np.array([])
# length_of_shoots = np.array([])
# mean_roots = []
text_extensions = {'.txt'}
roots_p_values = np.array([])
shoots_p_values = np.array([])
roots_sum_p_values = np.array([])
roots_mean_p_values = np.array([])
germination_rates = np.array([])


def normality_of_the_distribution_control(directory):
    ''' Не используется '''
    global all_values
    global length_of_shoots
    global germination_rates
    global mean_roots
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    df = read_and_extract_txt_data(item)
                    ''' Рассмотрение средних длин корней для теста Тьюки '''
                    numpy_values = df['Общая_длина_корневой_системы']
                    mean_roots.append(numpy_values)  # Сохраняем как список

                    ''' Рассмотрение общей длины корней '''
                    numpy_values = df["Общая_длина_корневой_системы"].to_numpy()
                    all_values = np.append(all_values, numpy_values)

                    ''' Рассмотрение длины побегов '''
                    numpy_values = df["Побег"].to_numpy()
                    length_of_shoots = np.append(
                        length_of_shoots,
                        numpy_values
                    )

                    ''' Рассмотрение всхожести '''
                    germination_rate = count_germination_rate(item)
                    germination_rates = np.append(
                        germination_rates,
                        germination_rate
                    )
            elif item.is_dir():
                normality_of_the_distribution_control(item)
    except Exception as e:
        print(f"Ошибка при чтении файла: {item}. Ошибка - {e}")
    finally:
        '''
        Тест ANOVA (Показывает различия в среднем значении)
        Если отличется хотя бы одна группа, то всё плохо
        '''
        f_statistic, f_p_value = f_oneway(*mean_roots)
        print(
            f"ANOVA statistic = {f_statistic}; "
            f"ANOVA p_value = {f_p_value}"
        )

        ''' Тест Левена (Показывает различия в дисперсии) '''
        f_statistic, f_p_value = levene(*mean_roots)
        print(
            f"Levene statistic = {f_statistic}; "
            f"Levene p_value = {f_p_value}"
        )

        ''' Тест Шапиро (Проверка на нормальное распределение) '''
        s_statistic, s_p_value = shapiro(all_values)
        print(
            f"shapiro statistic = {s_statistic}; "
            f"shapiro p_value = {s_p_value}"
        )

        '''
        Тест Тьюки
        Контролирует семейную ошибку (FWER), избегая ложных значимых
        результатов при множественных сравнениях
        '''
        t_statistic, t_p_value = tukey_hsd(*mean_roots)
        print(
            f"Tukey statistic = {t_statistic}; "
            f"Tukey p_value = {t_p_value}"
        )

        return all_values, length_of_shoots, germination_rates, mean_roots


def analyse_control_experiment(filename: Path):
    ''' Анализ одного файла контроля '''
    global roots_p_values
    global shoots_p_values
    global roots_sum_p_values
    global roots_mean_p_values
    global germination_rates
    try:
        df = read_and_extract_txt_data(filename)
        logger.info(f"Рассматриваем файл {filename}")

        ''' Рассмотрение индивидуальных корней '''
        roots_values = df.iloc[:, 1:len(df.columns)-2].to_numpy().flatten()
        # ~ - инвертирование
        roots_values = roots_values[~np.isnan(roots_values)]

        ''' Рассмотрение побегов '''
        shoots_values = df.loc[:, 'Побег'].to_numpy().flatten()
        shoots_values = shoots_values[~np.isnan(shoots_values)]

        ''' Рассмотрение корневой системы '''
        roots_sum_values = df.loc[:, 'Общая_длина_корневой_системы'].to_numpy().flatten()
        roots_sum_values = roots_sum_values[~np.isnan(roots_sum_values)]

        ''' Рассмотрение средней длины корней '''
        roots_mean_values = df.loc[:, 'Средняя_длина_корня'].to_numpy().flatten()
        roots_mean_values = roots_mean_values[~np.isnan(roots_mean_values)]

        ''' Тест Шапиро (Проверка на нормальное распределение) '''
        # Корни
        s_statistic, s_p_value = shapiro(roots_values)
        logger.info(f"Индивидуальные корни: p={s_p_value:.7f}")
        roots_p_values = np.append(roots_p_values, s_p_value)

        # Побеги
        s_statistic, s_p_value = shapiro(shoots_values)
        logger.info(f"Побеги: p={s_p_value:.7f}")
        shoots_p_values = np.append(shoots_p_values, s_p_value)

        # Корневая система
        s_statistic, s_p_value = shapiro(roots_sum_values)
        logger.info(f"Корневая система: p={s_p_value:.7f}")
        roots_sum_p_values = np.append(roots_sum_p_values, s_p_value)

        # Средняя длина корня
        s_statistic, s_p_value = shapiro(roots_mean_values)
        logger.info(f"Средняя длина корня: p={s_p_value:.7f}")
        roots_mean_p_values = np.append(roots_mean_p_values, s_p_value)

        # Всхожесть
        germination_rate = count_germination_rate(filename)
        logger.info(f"Всхожесть = {germination_rate:.7f}\n")
        germination_rates = np.append(germination_rates, germination_rate)

    except Exception as e:
        print(f"Ошибка - {e}; В файле {filename}")
        logger.error(f"Ошибка в файле {filename}! Ошибка - {e}\n")

    finally:
        # return roots_values, shoots_values, roots_sum_values, mass_string
        pass


def analyse_all_control_experiments(directory):
    ''' Анализ всех файлов контроля '''
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    analyse_control_experiment(item)
            elif item.is_dir():
                analyse_all_control_experiments(item)
    except Exception as e:
        print(f"Ошибка при чтении файла: {item}. Ошибка - {e}")
    finally:
        pass


if __name__ == "__main__":
    # all_values, length_of_shoots, germination_rates, mean_roots = (
    #     normality_of_the_distribution_control(
    #         # Сюда прописывать путь до папки
    #         Path("experiments", "control", "15-24")
    #     )
    # )

    # draw_qq_histograms(all_values, length_of_shoots)
    # draw_germination_rates(germination_rates)

    logger.info("Тесты Шапиро для контрольной группы")
    analyse_all_control_experiments(
        Path(
            'diploma',
            '2019.09.05_Winter Wheat 2018 Ozon 4gm3 on MASS',
        )
    )

    # Форматирование записи итоговых массивов
    formatter = {
        "float_kind": lambda x: f"{x:.7f}"
    }

    logger.info(
        "Итоговый массив из значений P для индивидуальных корней: "
        f"{np.array2string(roots_p_values, formatter=formatter)}"
    )
    logger.info(
        "Итоговый массив из значений P для побегов: "
        f"{np.array2string(shoots_p_values, formatter=formatter)}"
    )
    logger.info(
        "Итоговый массив из значений P для корневой системы: "
        f"{np.array2string(roots_sum_p_values, formatter=formatter)}"
    )
    logger.info(
        "Итоговый массив из значений P для средней длины корня: "
        f"{np.array2string(roots_mean_p_values, formatter=formatter)}"
    )
    logger.info(
        "Итоговый массив из значений всхожести: "
        f"{np.array2string(germination_rates, precision=5)}"
    )

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
