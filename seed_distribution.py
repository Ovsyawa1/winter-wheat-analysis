from pathlib import Path
import re
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


seed_masses = np.array([])


def mass_distribution(directory: str):
    """
    Функция для определения всех масс из файлов

    Args:
        directory (str): Путь к директории для поиска.

    Returns:
        seed_distribution(np.array): Массив из масс семян в каждом опыте
    """

    global seed_masses  # обращение к глобальной переменной
    text_extensions = {'.txt'}  # искать только .txt файлы
    # Создание регулярного выражения для поиска массы
    pattern = re.compile(r'\d+-\d+')  # (число)-(число)
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            # Переменная для использования в расчетах средних значений
            sum = 0
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    # Получаем "части" от названия текстового файла
                    parts = re.split(r'[ _]', item.stem)
                    # Поиск совпадений в частях от названия
                    matches = list(filter(pattern.match, parts))
                    # Файлы могут записаны через "-"",
                    # а могут просто указывать, что масса больше 45
                    if matches:  # случай когда нашлись совпадения
                        mass_string = matches[0]
                        values = mass_string.split('-')
                        for value in values:
                            sum += int(value)
                        seed_masses = np.append(seed_masses, sum/2)
                    else:  # случай, когда указано "45 и больше"
                        seed_masses = np.append(seed_masses, 45)
            # Вход в рекурсию для "поиска в глубину"
            elif item.is_dir():
                mass_distribution(item)
    except UnicodeDecodeError:
        raise (
            f"Ошибка чтения файла {item}: "
            f"неверная кодировка"
        )
    except FileNotFoundError as e:
        raise f"Не найден файл. Ошибка {e}"
    except Exception as e:
        raise f"Ошибка при чтении файла {item}: {str(e)}"
    finally:
        return seed_masses


if __name__ == "__main__":
    seed_distribution = mass_distribution("diploma")
    # unique_masses = np.unique(seed_distribution)
    # count_masses = np.array([])
    # for unique_mass in unique_masses:
    #     mass_repeats = np.count_nonzero(seed_distribution == unique_mass)
    #     count_masses = np.append(count_masses, mass_repeats)

    # print(seed_distribution)
    # print(unique_masses)
    # print(count_masses)

    '''
    Создание графического представления о распределении масс в опытах
    '''
    # order = np.argsort(unique_masses)
    # mass_x = np.array(unique_masses)[order]
    # mass_y = np.array(count_masses)[order]

    '''График в виде KDE (kernel density estimation)'''
    sns.set_style('whitegrid')
    sns.kdeplot(seed_distribution) 

    plt.style.use('fivethirtyeight')
    # bins = [15, 24, 28, 32, 36, 40, 44, 50]

    '''График в виде гистограммы'''
    # plt.hist(
    #     seed_distribution,
    #     bins=bins,
    #     edgecolor='black',
    #     color="orange",
    #     )
    
    plt.title('Распределение семян по массе')
    plt.xlabel('Масса, мгм')
    plt.ylabel('Число семян')

    plt.show()
