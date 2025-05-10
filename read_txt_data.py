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
        filename,
        sep="\t",
        header=None,
        names=columns,
        skipfooter=1,
        engine="python",
    )
    df['Средняя_длина_корня'] = df.iloc[:, 1:].mean(axis=1)
    df['Общая_длина_корневой_системы'] = df.iloc[:, 1:].sum(axis=1)
    return df
