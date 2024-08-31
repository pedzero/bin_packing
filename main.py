from domain.Solver import Solver
from view.View import View

#elements_size = [1/8, 3/8, 5/8, 2/8]
elements_size = [0.1, 0.15, 0.25, 0.5, 0.65, 0.3]
solver = Solver(elements_size, 1.0)

view = View()
view.run(solver)
