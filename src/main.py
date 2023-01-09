from sa_algorithm import simulated_annealing, init_solution, new_solution
from read_data import validate_txt_data, read_txt

print("Wpisz exit aby zakończyć.")
while True:
    inp_ = input("Podaj ścieżkę do pliku z danymi.\n")
    if inp_ == 'exit':
        break
    validate_txt_data(inp_)
    stations, end_point, car = read_txt(inp_)
    max_dist = int(input("Podaj maksymalna odległość na jaką chcesz zjechać."))
    if inp_ == 'exit':
        break
    solu = init_solution(car, end_point, max_dist, stations)

    P = float(input("Podaj prawdopodobieństwo przyjmowania zmiany stacji."))
    if inp_ == 'exit':
        break

    best_sol, _, iters, swaps = simulated_annealing(new_solution, solu, stations, end_point, max_dist, P)

    print(f"Rozwiązanie po {iters} iteracjach:")
    print(f"Wartość funkcji celu: {best_sol.solution_value()}")
    print(f"Kwota wydana na paliwo: {best_sol.get_cost_of_solution()}$")
    print(f"Funkcja kary: {best_sol.get_penalty()}")
    print("Kolejno stacje do odwiedzenia:")
    for station in best_sol.get_solution():
        print(f"Stacja: {station[0]} ilość paliwa: {station[1]}")
