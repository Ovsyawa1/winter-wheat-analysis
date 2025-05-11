import logging
from pathlib import Path
import numpy as np

from get_germination_rate import count_germination_rate
from normality_analysis import text_extensions
from draw_graphs import draw_mass_analys
from read_txt_data import read_and_extract_txt_data


mean_shoots_values = np.array([])
mean_roots_values = np.array([])
mean_all_roots_values = np.array([])
shoots_values = np.array([])
roots_values = np.array([])
all_roots_values = np.array([])
germination_rates = np.array([])

''' Объявление логгера для Контроля '''
logger = logging.getLogger('seed_characteristics')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('seed_characteristics.log', mode='a')
handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(handler)


def data_organization(filename):
    global mean_shoots_values
    global mean_roots_values
    global mean_all_roots_values
    global shoots_values
    global roots_values
    global all_roots_values
    global germination_rates

    df = read_and_extract_txt_data(filename)
    # Проверка на аномалии
    print(filename)
    print(df[df["Средняя_длина_корня"] == df["Средняя_длина_корня"].max()])
    logger.info(f"Файл - {filename}")
    logger.info(
        "Средняя длина побега: "
        f"{df["Побег"].mean():.5f}\n"
        "Отклонение: "
        f"{df["Побег"].std():.5f}"
    )
    mean_shoots_values = np.append(mean_shoots_values, df["Побег"].mean())
    shoots_values = np.append(shoots_values, df["Побег"].to_numpy().flatten())

    logger.info(
        "Средняя длина корня: "
        f"{df['Средняя_длина_корня'].mean():.5f}\n"
        "Отклонение: "
        f"{df['Средняя_длина_корня'].std():.5f}"
    )
    mean_roots_values = np.append(
        mean_roots_values,
        df['Средняя_длина_корня'].mean()
    )
    roots_values = np.append(
        roots_values,
        df["Средняя_длина_корня"].to_numpy().flatten()
    )

    logger.info(
        "Средняя общая длина корневой системы: "
        f"{df['Общая_длина_корневой_системы'].mean():.5f}\n"
        "Отклонение: "
        f"{df['Общая_длина_корневой_системы'].std():.5f}"
    )
    mean_all_roots_values = np.append(
        mean_all_roots_values, 
        df['Общая_длина_корневой_системы'].mean()
    )
    all_roots_values = np.append(
        all_roots_values,
        df['Общая_длина_корневой_системы'].to_numpy().flatten()
    )
    
    germination_rate = count_germination_rate(filename)
    logger.info(
        "Всхожесть: "
        f"{germination_rate:.5f}\n"
    )
    germination_rates = np.append(germination_rates, germination_rate)


def weight_characteristics(directory):
    ''' Анализ всех файлов '''
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    data_organization(item)
            elif item.is_dir():
                weight_characteristics(item)
    except Exception as e:
        logger.error(f"Ошибка в папке {directory}! Ошибка - {e}\n")
        print(f"Ошибка при чтении файла: {item}. Ошибка - {e}")


if __name__ == "__main__":
    logger.info("Начало анализа данных по массе\n")
    weight_characteristics(
        Path(
            'experiments',
            '8gm3_45',
        )
    )
    logger.info(
        "Итого\n"
        "Для рассматриваемого массового диапозона семян\n"
        f"Средняя длина побега: {shoots_values.mean():.5f}\n"
        f"Средняя длина корня: {roots_values.mean():.5f}\n"
        f"Средняя длина корневой системы: {all_roots_values.mean():.5f}\n"
        f"Средний показатель всхожести: {germination_rates.mean():.5f}\n\n"
    )
    draw_mass_analys(
        shoots_values,
        roots_values,
        all_roots_values,
        germination_rates
    )
