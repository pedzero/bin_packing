from domain.Solver import Solver
from view.View import View

elements_size = [1.0, 3.0, 5.0, 2.0]
target = 8.0
capacity = 1.0

solver = Solver(elements_size, target, capacity)

view = View()
view.run(solver)
