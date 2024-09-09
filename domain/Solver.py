from itertools import permutations
from domain.Bin import Bin
from domain.Element import Element


class Solver:
    elements: list[Element] = []
    bins: list[Bin] = []
    all_combinations: list = []
    valid_solutions: list[bins] = []
    unique_solutions: set[frozenset] = set()

    filter_solutions: bool = True

    def __init__(self, elements_size: list[float], bins_capacity: float):
        for e in elements_size:
            self.elements.append(Element(e))
        self.bins_capacity = bins_capacity
        self.all_combinations = list(permutations(self.elements))

    def toggle_solution_filter(self):
        self.filter_solutions = not self.filter_solutions

    def solve_by_index(self, index: int) -> bool:
        if index < 0 or index >= len(self.all_combinations):
            return False

        self.bins = []

        combination = self.all_combinations[index]
        self.pack_elements(combination)

        return True

    def solve_all(self):
        self.bins = []

        for i, combination in enumerate(self.all_combinations):
            self.pack_elements(combination)

    def pack_elements(self, combination):
        current_bin = Bin(self.bins_capacity)
        self.bins.append(current_bin)

        for element in combination:
            if not current_bin.add_element(element):
                current_bin = Bin(self.bins_capacity)
                self.bins.append(current_bin)
                current_bin.add_element(element)

        for i, _bin in enumerate(self.bins):
            if _bin.is_full():
                if not self.filter_solutions:
                    self.valid_solutions.append(list(_bin.elements))
                else:
                    solution_set = frozenset(_bin.elements)
                    if solution_set not in self.unique_solutions:
                        self.unique_solutions.add(solution_set)
                        self.valid_solutions.append(list(_bin.elements))
