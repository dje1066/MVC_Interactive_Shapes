from pygame import *
from Shape2401 import *
import math

"""
SOLUTION FOR A5: To Remove
"""

class CircleModel(ShapeModel):
    """
    def __init__(self, rect, colour):
        super().__init__(rect, colour)
        self.radius = min(rect.width / 2.0, rect.height / 2.0)
    """


    def __init__(self, rect, colour):
        super().__init__(rect, colour)
        # Set the center point
        min_dim = min(self.rect.width, self.rect.height) / 2
        self.radius = min_dim
        self.center_x = self.rect.x + self.radius
        self.center_y = self.rect.y + self.radius


    # Moves the shape to start at position (newX, newY)
    def moveShape(self, newX, newY):
        super().moveShape(newX, newY)
        self.center_x = self.rect.x + self.radius
        self.center_y = self.rect.y + self.radius

    def getCenter(self):
        return (self.center_x, self.center_y)

    def getRadius(self):
        return self.radius

    """
    def paint(self, screen):
        curr_rect = self.getBounds()
        fill_colour = self.getFillColour()
        centerpt = (curr_rect.x + self.radius, curr_rect.y + self.radius)

        pygame.draw.circle(screen, fill_colour, centerpt, self.radius, 0)

        self.paintOutline(screen)
    """

    def intersectsPt(self, ptTest) -> bool:
        # Basic intersection test is to see if the point is within the bounds
        if ptTest[0] < self.rect.x or ptTest[1] < self.rect.y:
            return False
        elif ptTest[0] > self.rect.x + self.rect.width or ptTest[1] > self.rect.y + self.rect.height:
            return False
        else:
            dist_from_center = self.pt_dist(ptTest, (self.center_x, self.center_y))
            return dist_from_center < self.radius

    def __str__(self):
        basetxt = super().__str__()
        centertxt = " Center: (" + str(self.center_x) + ", " + str(self.center_y) + ")"
        circletxt = " Radius: " + str(self.radius)  + centertxt
        return basetxt + circletxt


    # The "Shape" class is type "S".
    # A rectangle is "R", Triangle is "T" and Circle is "C"
    def getTypeName(self):
        return "C"

class CircleView(ShapeView):

    def paint(self, screen):
        curr_rect = self._model.getBounds()
        fill_colour = self._model.getFillColour()
        radius = 0
        if isinstance(self._model, CircleModel):
            radius = self._model.getRadius()

        centerpt = (curr_rect.x + radius, curr_rect.y + radius)

        pygame.draw.circle(screen, fill_colour, centerpt, radius, 0)
        self.paintOutline(screen)


class Circle2401(Shape2401):

    def __init__(self, rect, colour):
        self._model = CircleModel(rect, colour)
        self._view = CircleView(self._model)
        self._controller = ShapeController(self._model)

