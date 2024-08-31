from itertools import permutations
from domain.Bin import Bin
from domain.Element import Element


class Solver:
    elements: list[Element] = []
    bins: list[Bin] = []
    all_combinations: list = []
    valid_solutions: list[bins] = []

    def __init__(self, elements_size: list[float], bins_capacity: float):
        for e in elements_size:
            self.elements.append(Element(e))
            self.bins_capacity = bins_capacity
        self.all_combinations = list(permutations(self.elements))

    def solve_by_index(self, index: int):
        if index < 0 or index >= len(self.all_combinations):
            raise IndexError("Index out of range")

        self.bins = []

        combination = self.all_combinations[index]

        self.pack_elements(combination)

    def pack_elements(self, combination):
        current_bin = Bin(self.bins_capacity)
        self.bins.append(current_bin)

        for element in combination:
            if not current_bin.add_element(element):
                current_bin = Bin(self.bins_capacity)
                self.bins.append(current_bin)
                current_bin.add_element(element)
