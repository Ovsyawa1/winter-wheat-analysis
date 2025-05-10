import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import probplot


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


def draw_mass_analys(shoots_values, roots_values, all_roots_values):
    plt.subplot(2, 2, 1)
    plt.hist(shoots_values, bins=15, color="green")
    plt.title('Распределение длин побегов')

    plt.subplot(2, 2, 2)
    plt.hist(roots_values, bins=15, color="orange")
    plt.title("Распределение средних длин корней")

    plt.subplot(2, 2, 3)
    plt.hist(all_roots_values, bins=15, color="skyblue")
    plt.title('Распределение длин корневых систем')
    plt.show()


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
