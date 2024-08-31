# Exemplo de uso
from domain.Solver import Solver

elements_size = [1/8, 3/8, 5/8, 2/8]
solver = Solver(elements_size, 1.0)

index = 3
solver.solve_by_index(index)

# A solução está agora armazenada em solver.bins
for i, bin in enumerate(solver.bins):
    print(f"Bin {i+1}: {[element.size for element in bin.elements]}, {bin.used_capacity}")
