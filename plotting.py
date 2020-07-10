import numpy as np
import matplotlib.pyplot as plt


def arrow_coords(center1, center2, rad1, rad2):
    '''Вычисление коородинат стрелок для отрисовки диагональных перекосов'''
    cos = np.sqrt(2) / 2
    center1, center2 = np.array(center1), np.array(center2)
    sign = np.sign(center2 - center1)
    arr_base = np.array(center1) + sign * (rad1 * cos)
    center_diff = center2 - center1
    dx, dy = center_diff - (center_diff / np.linalg.norm(center_diff)) * (rad1 + rad2)
    return list(arr_base), dx, dy


def plot_fields(axis, weigths, scale_coef=0.2):
    '''
    В этой функции почему-то ошибка (см. dataframe и текущий график), буду чинить этот момент,
    когда на figure будет полная картина (таблица со значениями и ОГ вместе с ЗГ)
    upd есть таблица со значениями, сейчас буду чинить...
    ЭКСПЕРИМЕНТАЛЬНАЯ ВЕРСИЯ
    '''
    # ЛП, ЛН, ПП, ПН
    centers_grid = np.meshgrid([0.25, 0.75], [0.25, 0.75])
    quadrant_table = {'1': (centers_grid[0][0,1], centers_grid[1][1,0]),
                      '2': (centers_grid[0][0,0], centers_grid[1][1,1]),
                      '3': (centers_grid[0][1,0], centers_grid[1][0,1]),
                      '4': (centers_grid[0][1,1], centers_grid[1][0,0])}

    weigths = np.array([weigths[field] for field in ['Левая Пятка', 'Правая Пятка', 'Левый Носок', 'Правый Носок']])
    weigths = weigths * scale_coef / weigths.max()
    percentages = (weigths / weigths.sum()).reshape((4,))
    quadrant_weigths = {'1': weigths[0], '2': weigths[1], '3': weigths[2], '4': weigths[3]}
    quadrant_weigths = {'1': weigths[3], '2': weigths[2], '3': weigths[0], '4': weigths[1]}

    # getting coordinates for arrows
    for start, end in [('1', '3'), ('2', '4')]:
        start_end = [quadrant_weigths[start], quadrant_weigths[end]]
        start_end = {key: quadrant_weigths[key] for key in [start, end]}
        k, v = list(start_end.keys()), list(start_end.values())
        max_key = k[v.index(max(v))]
        min_key = k[v.index(min(v))]
        diag = arrow_coords(quadrant_table[min_key],
                            quadrant_table[max_key],
                            quadrant_weigths[min_key],
                            quadrant_weigths[max_key])

        axis.arrow(*diag[0], diag[1], diag[2], length_includes_head=True, head_width=0.03, head_length=0.08)

    # здесь про отрисовку "нормы"
    norm_percentages = np.array([32, 32, 18, 18]) / 100.
    percent_len = weigths.max() / percentages.max()
    norm_weigths = percent_len * norm_percentages

    xx, yy = np.meshgrid([0.25, 0.75], [0.25, 0.75])  # right to left, bottom to up

    for x, y, w, perc, n_w, n_perc in zip(xx.ravel(), yy.ravel(), weigths, percentages, norm_weigths, norm_percentages):
        alpha = w / scale_coef
        lw = w * 2 / scale_coef
        cir = plt.Circle((x, y), radius=w, alpha=alpha, edgecolor='black', facecolor='white', linewidth=lw)
        axis.add_patch(cir)
        norm_cir = plt.Circle((x, y), radius=n_w, alpha=0.5, fill=False, linestyle='--')
        axis.add_patch(norm_cir)
        axis.text(x, y, s=str(round(100 * perc, 1)) + ' %' + 2*'\n' + str(round(100 * (perc - n_perc), 1)) + '%')


def plot_patient(pat_df):
    '''
    Эта функция по видимости принимает на вход dataframe (какой, сколько пациентов?)
    для того, чтобы разбить эти данные на ОГ и ЗГ, создать figure и subplots, затем
    на этой матрице графиков вызвать plot_fields
    '''
    opeyes_weigths = pat_df['ОГ']  # ЛП, ЛН, ПП, ПН
    cleyes_weigths = pat_df['ЗГ']

    fig = plt.figure(figsize=(13, 6))
    axes = fig.subplots(1, 2)

    # circles
    ax_opeye = axes[0]
    ax_cleye = axes[1]

    plot_fields(ax_opeye, opeyes_weigths)
    plot_fields(ax_cleye, cleyes_weigths)

    ax_opeye.set_axis_off()
    ax_cleye.set_axis_off()
