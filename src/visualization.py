from typing import List

import matplotlib.pyplot as plt

from src.data_structures import Solution


def plot_score(lst: List[float], iter_number: int) -> None:
    """
    Function to plot solution value trough iteration
    :param lst: Lst of particular solution value
    :param iter_number: Nuber of iteration
    :return:
    """
    plt.style.use('ggplot')
    plt.plot(range(iter_number + 1), lst)
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


def plot_solution(solution: Solution) -> None:
    plt.style.use('ggplot')
    y = [elem[0].extra_route for elem in solution.get_solution()]
    x = [elem[0].road_position for elem in solution.get_solution()]

    #for i in range(len(solution)):
        #string = f"Km trasy: {solution.get_station(i).road_position}\n"
        #string += f"Ex km: {solution.get_station(i).extra_route}\n"
        #string += f"il: {solution.solution[i][1]}"
        #plt.annotate(
        #    string, (x[i], y[i] + 0.2))

    plt.xlabel("Kilometr trasy")
    plt.title("Stacje na które musimy zjechać")
    plt.ylabel("Dodatkowe km do trasy")
    plt.stem(x, y)
    plt.show()
