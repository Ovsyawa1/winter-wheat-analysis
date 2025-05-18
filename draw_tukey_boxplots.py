import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from read_txt_data import read_and_extract_txt_data


# Настройка стиля графиков
plt.style.use('default')
sns.set_theme()

# Пути к папкам с данными
folders = [
    Path('diploma', '2019.09.05_Winter Wheat 2018 Ozon 4gm3 on MASS'),
    Path('diploma', '2019.09.12 Winter Wheat 2018 ozon 1gm3 on MASS'),
    Path('diploma', '2019.10.03 Winter Wheat 2018 ozon 4gm3 45min on MASS', 'IPP RAS'),
    Path('diploma', '2019.10.03 Winter Wheat 2018 ozon 4gm3 45min on MASS', 'MPEI'),
    Path('diploma', '2019.10.24 WW 2018 Ozon 3gm3 45 min on MASS'),
    Path('diploma', '2019.11.08 WW 2018  Ozon on MASS'),
    Path('diploma', '2019.12.26 Winter Wheat 2018 on MASS ozon'),
    Path('diploma', '2019.12.27 Winter Wheat 2018 on MASS ozon'),
    Path('diploma', '2020.01.16 Winter Wheat 2018 ozone on Mass'),
    Path('diploma', '2020.01.17 WW  2018 ozone on Mass')
]

# Собираем данные
all_data_list = []
for i, folder in enumerate(folders, 1):
    for item in folder.iterdir():
        if item.is_file() and item.suffix.lower() == '.txt':
            df = read_and_extract_txt_data(item)
            df['Группа'] = f"Группа_{i}"
            all_data_list.append(df)

full_data = pd.concat(all_data_list, ignore_index=True)

# Создаем фигуру с двумя подграфиками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Настройка шрифта для всех текстовых элементов
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18  # Размер шрифта по умолчанию

# Boxplot для побегов
sns.boxplot(x='Группа', y='Побег', data=full_data, ax=ax1)
ax1.set_title('Распределение длины побегов по группам', fontsize=18)
ax1.set_xlabel('Группа', fontsize=18)
ax1.set_ylabel('Длина побега (мм)', fontsize=18)
ax1.tick_params(axis='x', rotation=45)

# Boxplot для корней
sns.boxplot(x='Группа', y='Средняя_длина_корня', data=full_data, ax=ax2)
ax2.set_title('Распределение средней длины корня по группам', fontsize=18)
ax2.set_xlabel('Группа', fontsize=18)
ax2.set_ylabel('Средняя длина корня (мм)', fontsize=18)
ax2.tick_params(axis='x', rotation=45)

# Настройка общего вида
plt.tight_layout()
plt.savefig('tukey_boxplots.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
