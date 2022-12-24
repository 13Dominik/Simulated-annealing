from typing import List

import matplotlib.pyplot as plt

from data_structures import Solution


def plot_score(lst: List[float], iter_number: int) -> None:
    """
    Function to plot solution value trough iteration
    :param lst: Lst of particular solution value
    :param iter_number: Nuber of iteration
    :return:
    """
    plt.style.use('ggplot')
    plt.plot(range(iter_number), lst)
    plt.xlabel('Iteracja')
    plt.ylabel('Funkcja celu')
    plt.title('Wartość funkcji celu w poszczególnych iteracjach')
    plt.show()
    return None


def plot_random_stations(end_point: int, coord_list: List) -> None:
    """
    Plotting random generated stations
    :param end_point:
    :param coord_list:
    :return:
    """
    plt.style.use('ggplot')
    plt.scatter([el[0] for el in coord_list], [el[1] for el in coord_list], label='Stacje', c='m')
    plt.plot(range(0, end_point), range(0, end_point), label='Trasa')
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    plt.title('Losowo wygenerowane dane')
    plt.show()


def plot_solution(end_point: int, coord_list: List, solution: Solution) -> None:
    plt.style.use('ggplot')
    plt.scatter([el[0] for el in coord_list], [el[1] for el in coord_list], label='Stacje', c='g')
    #
    for i in range(len(coord_list)):
        plt.annotate(str(solution.get_station(i)), (coord_list[i][0], coord_list[i][1] + 0.2))

    plt.plot(range(0, end_point), range(0, end_point), label='Trasa')
    plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    plt.title('Wybrane stacje do tankowania wraz z ceną')
    plt.show()
