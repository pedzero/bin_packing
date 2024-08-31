from domain.Element import Element


class Bin:
    def __init__(self, capacity: float):
        self.capacity = capacity
        self.used_capacity = 0.0
        self.elements: list[Element] = []

    def add_element(self, element: Element) -> bool:
        if (self.capacity - self.used_capacity) < element.size:
            return False

        self.elements.append(element)
        self.used_capacity += element.size
        return True

    def is_full(self):
        return self.capacity == self.used_capacity
