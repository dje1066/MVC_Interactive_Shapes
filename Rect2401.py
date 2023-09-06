from pygame import *
from Shape2401 import *

"""
SOLUTION FOR A5: To Remove
"""

class RectModel(ShapeModel):

    def __init__(self, rect, colour):
        super().__init__(rect, colour)

    """
    def paint(self, screen):
        curr_rect = self.getBounds()
        fill_colour = self.getFillColour()

        # Draw the filled in rectangle
        pygame.draw.rect(screen, fill_colour, curr_rect)

        self.paintOutline(screen)
    """

    # The "Shape" class is type "S".
    # A rectangle is "R", Triangle is "T" and Circle is "C"
    def getTypeName(self):
        return "R"

class RectView(ShapeView):

    def paint(self, screen):
        curr_rect = self._model.getBounds()
        fill_colour = self._model.getFillColour()

        # Draw the filled in rectangle
        pygame.draw.rect(screen, fill_colour, curr_rect)

        self.paintOutline(screen)

class Rect2401(Shape2401):

    def __init__(self, rect, colour):
        self._model = RectModel(rect, colour)
        self._view = RectView(self._model)
        self._controller = ShapeController(self._model)