from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import levene
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.formula.api import ols
import statsmodels.api as sm
import logging

from read_txt_data import read_and_extract_txt_data


''' Объявление логгера для теста Тьюки '''
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler('tukey_result.log', mode='w')
    ],
)
logger = logging.getLogger('tukey_result')

text_extensions = {'.txt'}
folders = [
    Path('diploma', '2019.09.05_Winter Wheat 2018 Ozon 4gm3 on MASS'),
    Path('diploma', '2019.09.12 Winter Wheat 2018 ozon 1gm3 on MASS'),
    Path('diploma', '2019.10.03 Winter Wheat 2018 ozon 4gm3 45min on MASS', 
         'IPP RAS'),
    Path('diploma', '2019.10.03 Winter Wheat 2018 ozon 4gm3 45min on MASS', 
         'MPEI'),
    Path('diploma', '2019.10.24 WW 2018 Ozon 3gm3 45 min on MASS'),
    Path('diploma', '2019.11.08 WW 2018  Ozon on MASS'),
    Path('diploma', '2019.12.26 Winter Wheat 2018 on MASS ozon'),
    Path('diploma', '2019.12.27 Winter Wheat 2018 on MASS ozon'),
    Path('diploma', '2020.01.16 Winter Wheat 2018 ozone on Mass'),
    Path('diploma', '2020.01.17 WW  2018 ozone on Mass')
]

# Собираем данные в один DataFrame
all_data_list = []
for i, folder in enumerate(folders, 1):
    for item in folder.iterdir():
        if item.is_file():
            if item.suffix.lower() in text_extensions:
                df = read_and_extract_txt_data(item)
                df['Группа'] = f"Группа_{i}"
                all_data_list.append(df)

full_data = pd.concat(all_data_list, ignore_index=True)

'''
# Проверка для побегов
levene_test_shoots = levene(
    *[group['Побег'].values for name, group in full_data.groupby('Группа')]
)
print(f"Levene test (shoots): p-value = {levene_test_shoots.pvalue}")

# Проверка для корневой системы
levene_test_roots = levene(
    *[group['Общая_длина_корневой_системы'].values for name, group in full_data.groupby('Группа')]
)
print(f"Levene test (roots): p-value = {levene_test_roots.pvalue}")

# Проверка на среднюю длину корня
levene_test_roots = levene(
    *[group['Средняя_длина_корня'].values for name, group in full_data.groupby('Группа')]
)
print(f"Levene test (roots): p-value = {levene_test_roots.pvalue}")

# ANOVA для побегов
model_shoots = ols('Побег ~ Группа', data=full_data).fit()
anova_shoots = sm.stats.anova_lm(model_shoots, typ=2)
print("ANOVA (shoots):\n", anova_shoots)

# ANOVA для корней
model_roots = ols('Общая_длина_корневой_системы ~ Группа', data=full_data).fit()
anova_roots = sm.stats.anova_lm(model_roots, typ=2)
print("ANOVA (roots):\n", anova_roots)
'''

tukey_shoots = pairwise_tukeyhsd(
    endog=full_data['Побег'],
    groups=full_data['Группа'],
    alpha=0.05
)
logger.info("Тест Тьюки для побегов")
logger.info(f"{tukey_shoots}")

shoots_rejections = tukey_shoots.reject
unique, counts = np.unique(shoots_rejections, return_counts=True)
logger.info("Число отказов в анализе побегов")
logger.info(f"{dict(zip(unique, counts))}\n")

# Тест Тьюки для корней
tukey_roots = pairwise_tukeyhsd(
    endog=full_data['Средняя_длина_корня'],
    groups=full_data['Группа'],
    alpha=0.05
)
logger.info("\nTukey HSD (roots):")
logger.info(tukey_roots)

roots_rejections = tukey_roots.reject
unique, counts = np.unique(roots_rejections, return_counts=True)
logger.info("Число отказов в анализе корней")
logger.info(dict(zip(unique, counts)))

# Дата фрейм для красивого отображения
results_df = tukey_roots.summary().as_text()
print(results_df)