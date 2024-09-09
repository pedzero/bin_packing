import sys
import time

import pygame

from domain.Color import Colors
from domain.Solver import Solver


class View:
    states = {
        "start": 1,
        "solving": 2,
        "ended": 3
    }

    current_state = states["start"]

    clr = Colors.instance()

    def __init__(self):
        pygame.init()
        self.width = 1152
        self.height = 648
        self.fps = 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        self._running = True
        self._set_caption("Bin Packing")

        self._button_pressed = False

        self.solver = None
        self.solution_index = 0

    def _event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            if event.type == pygame.MOUSEBUTTONUP:
                self._button_pressed = False

    def _quit(self):
        pygame.quit()
        sys.exit()

    def _draw_text(self, text, size, color, coordinates, center = True):
        font = pygame.font.SysFont("Arial", size)
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if center:
            text_rect.center = coordinates
        else:
            text_rect.topleft = coordinates

        self.screen.blit(text_obj, text_rect)

    def _draw_button(self, text, font_size, size, color, coord, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if coord[0] + size[0] > mouse[0] > coord[0] and coord[1] + size[1] > mouse[1] > coord[1]:

            pygame.draw.rect(self.screen, color, (coord[0], coord[1], size[0], size[1]))

            self.__draw_button_overlay(size, coord)

            if click[0] == 1 and action is not None and not self._button_pressed:
                action()
                self._button_pressed = True

        else:
            pygame.draw.rect(self.screen, color, (coord[0], coord[1], size[0], size[1]))

        self._draw_text(text, font_size, self.clr.colors["BLACK"], (coord[0] + (size[0] / 2), coord[1] + (size[1] / 2)))

    def __draw_button_overlay(self, size, coordinates):
        s = pygame.Surface(size)
        s.set_alpha(128)
        s.fill((0, 0, 0))
        self.screen.blit(s, coordinates)

    def _drawImage(self, directory, size, coordinates):
        self.screen.blit(pygame.transform.scale(pygame.image.load(directory), size), coordinates)

    def _draw_element(self, text, font_size, size, color, coord):
        pygame.draw.rect(self.screen, color, (coord[0], coord[1], size[0], size[1]))
        self._draw_text(text, font_size, self.clr.colors["BLACK"], (coord[0] + (size[0] / 2), coord[1] + (size[1] / 2)))

    def _set_caption(self, caption):
        pygame.display.set_caption(caption)

    def run(self, solver: Solver):
        self.solver = solver
        while self._running:
            clock = pygame.time.Clock()

            self.screen.fill((200, 200, 200))

            pygame.draw.rect(self.screen, (150, 150, 150), (902, 0, 250, self.height))

            if self.current_state == self.states["start"]:
                self.draw_title(f"S = {{{', '.join(str(element.size) for element in solver.elements)}}}")

            if self.current_state == self.states["solving"]:
                title = None
                try:
                    title = f"S = {{{', '.join(str(element.size) for element in solver.all_combinations[self.solution_index - 1])}}}"
                finally:
                    self.draw_title(title)
                    self.draw_solution()

            if self.current_state == self.states["ended"]:
                self.draw_title("Fim das Soluções")

            self.draw_valid_solution()

            text = ""
            if self.solver.filter_solutions:
                text = "X"
            self._draw_button(text, 22, (30, 30), (200, 200, 200), (912, 558),
                              self.toggle_filter)
            self._draw_text("Filtrar soluções", 22, (0, 0, 0), (950, 560), False)

            self._draw_button("Resolver", 22, (110, 40), (0, 204, 153), (912, 598),
                              self.button_resolve)
            self._draw_button("Próximo", 22, (110, 40), (0, 153, 153), (1032, 598),
                              self.button_step)

            self._event()

            pygame.display.update()
            clock.tick(self.fps)

        pygame.quit()

    def button_step(self):
        if not self.solver.solve_by_index(self.solution_index):
            self.current_state = self.states["ended"]
            return False
        self.solution_index += 1

        if self.current_state == self.states["start"]:
            self.current_state = self.states["solving"]
        return True

    def button_resolve(self):
        while self.button_step():
            pass

    def toggle_filter(self):
        self.solver.toggle_solution_filter()

    def draw_title(self, text: str):
        self._draw_text(text, 32, (0, 0, 0), (451, 32))

    def draw_solution(self):
        bin_color = (10, 20, 30)
        bin_size = (100, 400)
        gap = 20
        bins = len(self.solver.bins)
        max_size = (bins * (bin_size[0] + (gap - 1)))
        pos = ((self.width - max_size - 250) / 2, (self.height - bin_size[1]) / 2)

        pygame.draw.rect(self.screen, (150, 150, 150), (pos[0] - 10, pos[1] - 10, max_size + 5, bin_size[1] + 20))

        for i, bin in enumerate(self.solver.bins):
            if bin.is_full():
                pygame.draw.rect(self.screen, (0, 100, 50), (pos[0] - 3, pos[1] - 3, bin_size[0] + 6, bin_size[1] + 6))
            pygame.draw.rect(self.screen, bin_color, (pos[0], pos[1], bin_size[0], bin_size[1]))
            element_pos = (pos[0], pos[1] + bin_size[1])
            for j, element in enumerate(self.solver.bins[i].elements):
                element_pos = (element_pos[0], element_pos[1] - (element.size * bin_size[1] / bin.capacity))
                self._draw_element(str(element.size), 22, (bin_size[0], (element.size * bin_size[1] / bin.capacity)),
                                   self.clr.get_color_as_tuple(element.color), (element_pos[0], element_pos[1]))

            pos = (pos[0] + bin_size[0] + gap, pos[1])

    def draw_valid_solution(self):
        position = (1027, 20)
        font_size = int(24 - (len(self.solver.elements) / 10) * 20)

        if (len(self.solver.valid_solutions) > 0):
            self._draw_text(
                "Soluções Válidas",
                font_size + 4,
                (0, 100, 50),
                position
            )
            position = (position[0], position[1] + font_size + 10)
        for i, solution in enumerate(self.solver.valid_solutions):
            self._draw_text(
                f"S = {{{', '.join(str(element.size) for element in self.solver.valid_solutions[i])}}}",
                font_size,
                (0, 0, 0),
                position
            )
            position = (position[0], position[1] + font_size + 10)
            if position[1] > 550:
                return
