from pygame import *
from Shape2401 import *

"""
GIVEN CODE showing a refactored triangle class.  Notice how Triangle2401 has a model, view and controller
(but only the model is being used until you decide to refactor the code).
"""

class TriangleModel(ShapeModel):

    # Based on the bound rect, determine the 3 points that make up the triangle
    def updateTrianglePts(self):
        t1 = (self.rect.x, self.rect.y + self.rect.height)
        t2 = (self.rect.x + self.rect.width, self.rect.y + self.rect.height)
        t3 = (self.rect.x + (self.rect.width / 2), self.rect.y)
        self.polyPoints = (t1, t2, t3)

    def __init__(self, rect, colour):
        super().__init__(rect, colour)
        # Set the three triangle points
        t1 = (rect.x, rect.y + rect.height)
        t2 = (rect.x + rect.width, rect.y + rect.height)
        t3 = (rect.x + (rect.width / 2), rect.y)
        self.polyPoints = (t1, t2, t3)

    def intersectsPt(self, ptTest):
        if super().intersectsPt(ptTest):
            in_triangle = self.pt_in_polygon(ptTest, self.polyPoints)
            return in_triangle
        else:
            return False

    # Moves the shape to start at position (newX, newY)
    def moveShape(self, newX, newY):
        super().moveShape(newX, newY)
        self.updateTrianglePts()

    def getPolyPoints(self):
        return tuple(self.polyPoints)

    """
    def paint(self, screen):
        # Paint the interior: Filled polygons have a edge width of 0.
        fillColour = self.getFillColour()
        pygame.draw.polygon(screen, fillColour, self.polyPoints, 0)

        self.paintOutline(screen)
    """

    def __str__(self):
        basetxt = super().__str__()
        return basetxt + " Points: " + str(self.polyPoints)

    # The "Shape" class is type "S".
    # A rectangle is "R", Triangle is "T" and Circle is "C"
    def getTypeName(self):
        return "T"

    # Make a copy of the polygon points and hand to the view
    def getPolyPoints(self):
        return tuple(self.polyPoints)


class TriangleView(ShapeView):

    def paint(self, screen):
        # Paint the interior: Filled polygons have a edge width of 0.
        fillColour = self._model.getFillColour()
        if isinstance(self._model, TriangleModel):
            pygame.draw.polygon(screen, fillColour, self._model.getPolyPoints(), 0)
        self.paintOutline(screen)


class Triangle2401(Shape2401):

    def __init__(self, rect, colour):
        self._model = TriangleModel(rect, colour)
        self._view = TriangleView(self._model)
        self._controller = ShapeController(self._model)

