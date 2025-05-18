import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import probplot
import seaborn as sns


def draw_qq_histograms(roots_values, shoots_values):
    plt.subplot(2, 2, 1)
    probplot(roots_values, dist="norm", plot=plt)
    plt.title('Q-Q Корневая система')

    plt.subplot(2, 2, 2)
    plt.hist(roots_values, bins=15, color="orange")
    plt.title("Гистограмма Корневая система")

    plt.subplot(2, 2, 3)
    probplot(shoots_values, dist="norm", plot=plt)
    plt.title('Q-Q Побеги')

    plt.subplot(2, 2, 4)
    plt.hist(shoots_values, bins=15, color="green")
    plt.title('Гистограмма Побеги')
    plt.show()


def draw_germination_rates(germination_rates):
    x_axis = [x for x in range(1, len(germination_rates) + 1)]
    y_axis = germination_rates
    plt.bar(x_axis, y_axis, color="skyblue")
    plt.ylim(np.min(y_axis) - 0.2, 1)
    plt.title('График всхожесть')
    plt.show()


def draw_mass_histograms(
    shoots_values,
    roots_values,
    all_roots_values,
    germination_rates
):
    plt.subplot(2, 2, 1)
    plt.hist(shoots_values, bins=15, color="green", edgecolor="black")
    plt.title('Распределение длин побегов')

    plt.subplot(2, 2, 2)
    plt.hist(roots_values, bins=15, color="orange", edgecolor="black")
    plt.title("Распределение средних длин корней")

    plt.subplot(2, 2, 3)
    plt.hist(all_roots_values, bins=15, color="skyblue", edgecolor="black")
    plt.title('Распределение длин корневых систем')
    
    plt.subplot(2, 2, 4)
    x_axis = [x for x in range(1, len(germination_rates) + 1)]
    y_axis = germination_rates
    plt.bar(x_axis, y_axis, color="#ff5cff", edgecolor="black")
    plt.ylim(np.min(y_axis) - 0.2, 1)
    plt.title('График всхожесть')
    plt.show()


def draw_mass_boxplots():
    # Создаем фигуру с двумя подграфиками
    fig, axs = plt.subplots(2, 2, figsize=(15, 6))

    # Boxplot для побегов
    sns.boxplot(x='Группа', y='Побег', data=full_data, ax=axs[0, 0])
    ax1.set_title('Распределение длины побегов по группам')
    ax1.set_xlabel('Группа')
    ax1.set_ylabel('Длина побега (мм)')
    ax1.tick_params(axis='x', rotation=45)

    # Boxplot для корней
    sns.boxplot(x='Группа', y='Средняя_длина_корня', data=full_data, ax=ax2)
    ax2.set_title('Распределение средней длины корня по группам')
    ax2.set_xlabel('Группа')
    ax2.set_ylabel('Средняя длина корня (мм)')
    ax2.tick_params(axis='x', rotation=45)

    # Настройка общего вида
    plt.tight_layout()
    plt.savefig('tukey_boxplots.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()


def draw_control_roots(
    roots_values, shoots_values, shoots_sum_values, mass_string
):
    plt.subplot(2, 2, 1)
    probplot(roots_values, dist="norm", plot=plt)
    plt.title(f'Q-Q Индивидуальные корни {mass_string} мг')

    plt.subplot(2, 2, 2)
    plt.hist(roots_values, bins=15, color="orange")
    plt.title(f"Гистограмма Индивидуальные корни {mass_string} мг")

    plt.subplot(2, 2, 3)
    probplot(shoots_values, dist="norm", plot=plt)
    plt.title(f'Q-Q Побеги {mass_string} мг')

    plt.subplot(2, 2, 4)
    plt.hist(shoots_values, bins=12, color="lightgreen")
    plt.title(f"Гистограмма Побеги {mass_string} мг")
    plt.show()

    plt.subplot(1, 2, 1)
    probplot(shoots_sum_values, dist="norm", plot=plt)
    plt.title(f'Q-Q Корневая система {mass_string} мг')

    plt.subplot(1, 2, 2)
    plt.hist(shoots_sum_values, bins=12, color="orange")
    plt.title(f"Гистограмма Корневая система {mass_string} мг")
    plt.show()
