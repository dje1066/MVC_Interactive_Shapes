import pygame
import math

class ShapeModel:
    # Type suggestions for the member variables.
    fillColour: tuple
    selected: bool
    highlighted: bool
    rect: pygame.rect

    def __init__(self, rect, colour):
        self.rect = rect
        self.fillColour = colour
        self.selected = False
        self.highlighted = False

        #TEMPORARY: Remove these variables after refactoring.  They are in ShapeController class
        self.mouseDown = False
        self.mouseStartPt = (0, 0)
        self.shapeStartPt = (rect.x, rect.y)



    """
      Useful for circle intersections: If the distance between the circle center
      and a mouse location is < the circle's radius, what would that indicate??
    """
    def pt_dist(self, pt1, pt2):
        """
        pt_dist is the distance between points pt1 and pt2
        :param pt1: 2-tuple (x,y) of point 1
        :param pt2: 2-tuple (x,y) of point 1
        :return: float distance between pt1 and pt2
        """
        dist_x = pt1[0] - pt2[0]
        dist_y = pt1[1] - pt2[1]
        return math.sqrt(dist_x * dist_x + dist_y * dist_y)



    """ ---------------------------------------------------- 
    USEFUL FOR TRIANGLE SHAPES ONLY
    # this is a variant on taking the cross product(but in 2D)....don't worry about what it means. ptInTriangle
    # should determine whether a point is in a triangle 
    # A call to pt_in_triangle should provide 4
    --------------------------------------------------------"""
    # this is a variant on taking the cross product(but in 2D)....don't worry about what it means. ptInTriangle
    # should determine whether a point is in a triangle
    def side_lines(self, p1, p2, p3):
        return ((p1[0] - p3[0]) * (p2[1] - p3[1])) - ((p2[0] - p3[0]) * (p1[1] - p3[1]))

    def pt_in_polygon(self, pt, poly_pts) -> bool:
        """
        Mysterious function that determines if pt is inside the polygon (like a triangle)
        defined by the points in poly_pts (you might want this for your Triangle2400 class)
        :param pt: 2-tuple point (x,y) coordinates
        :param poly_pts: 2-tuple point (x,y) coordinate list that makes up the polygon (like a triangle)
        :return: bool if pt is in the polygon.
        """
        # All cross product values are positive or negative if point intersects.
        cp_posneg = 0.0
        for idx in range(len(poly_pts)):
            pt1 = poly_pts[idx]
            pt2 = poly_pts[(idx + 1) % len(poly_pts)]
            cross = self.side_lines(pt, pt1, pt2)

            if cp_posneg == 0.0:
                cp_posneg = cross
            elif cp_posneg < 0.0 and cross > 0.0:
                return False
            elif cp_posneg > 0.0 and cross < 0.0:
                return False
        return True

    def intersectsPt(self, ptTest) -> bool:
        # Basic intersection test is to see if the point is within the bounds
        if ptTest[0] < self.rect.x or ptTest[1] < self.rect.y:
            return False
        elif ptTest[0] > self.rect.x + self.rect.width or ptTest[1] > self.rect.y + self.rect.height:
            return False
        else:
            return True

    # TEMPORARY:  Remove when code is refactored to MVC.  This is almost the exact duplicate
    # of the code found in ShapeController
    #  GIVEN:  Handling the mouse events or at least making things easier.
    # Migrated to the ShapeController class.
    def handleUI(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            mousePt = event.pos  # 2-tuple for point
            ptIntersect = self.intersectsPt(mousePt)
            isHighlighted = self.isHighlighted()

            # Selection with a mouse down event will also update the starting point
            if event.type == pygame.MOUSEBUTTONDOWN and not self.mouseDown and ptIntersect:
                self.setSelected(True)
                self.mouseDown = True
                self.mouseStartPt = mousePt
                bound = self.getBounds()
                self.shapeStartPt = (bound.x, bound.y)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN and not ptIntersect:
                self.setSelected(False)
                return False
            # Drag the shape.  Get the change in mouse position and move the shape that much
            elif event.type == pygame.MOUSEMOTION and self.mouseDown and ptIntersect:
                # bound = self.getBounds()
                newX = self.shapeStartPt[0] + mousePt[0] - self.mouseStartPt[0]
                newY = self.shapeStartPt[1] + mousePt[1] - self.mouseStartPt[1]
                self.moveShape(newX, newY)
                return True
            elif event.type == pygame.MOUSEBUTTONUP and self.mouseDown:
                newX = self.shapeStartPt[0] + mousePt[0] - self.mouseStartPt[0]
                newY = self.shapeStartPt[1] + mousePt[1] - self.mouseStartPt[1]
                self.moveShape(newX, newY)
                self.mouseDown = False
                return True
            elif event.type == pygame.MOUSEMOTION and (ptIntersect and (not isHighlighted)):
                self.setHighlighted(True)
                return True
            elif event.type == pygame.MOUSEMOTION and ((not ptIntersect) and isHighlighted):
                self.setHighlighted(False)
                # self.setSelected(False)
                return False
            else:
                return False

    def isSelected(self) -> bool:
        return self.selected

    def setSelected(self, selected):
        self.selected = selected

    def isHighlighted(self) -> bool:
        return self.highlighted

    def setHighlighted(self, highlighted):
        self.highlighted = highlighted

    def getBounds(self) -> pygame.rect:
        return self.rect

    # Moves the shape to start at position (newX, newY)
    def moveShape(self, newX, newY):
        self.rect.x = newX
        self.rect.y = newY

    def getOutlineColour(self):
        if self.isSelected():
            return pygame.Color(150, 150, 150)
        else:
            return pygame.Color(0, 0, 0)

    def getOutlineThickness(self):
        if self.isSelected():
            return 5
        else:
            return 2

    def getFillColour(self):
        if self.isHighlighted():
            return pygame.Color(200, 200, 200)
        else:
            return self.fillColour

    # TEMPORARY:  Removed when  code is refactored
    # GIVEN: Draw the outline surrounding the shape
    def paintOutline(self, screen):
        if self.isSelected():
            pygame.draw.rect(screen, self.getOutlineColour(), self.getBounds(), self.getOutlineThickness())

    #TEMPORARY: Remove when refactored.
    def paint(self, screen):
        curr_rect = self.getBounds()
        fill_colour = self.getFillColour()

        # Draw an X instead of a rectangle shape to indicate this isn't a real
        # concrete shape (just like there is no "mammal" species)
        pygame.draw.line(screen, fill_colour, (curr_rect.x, curr_rect.y),
                         (curr_rect.x + curr_rect.width, curr_rect.y + curr_rect.height))
        pygame.draw.line(screen, fill_colour, (curr_rect.x + curr_rect.width, curr_rect.y),
                         (curr_rect.x, curr_rect.y + curr_rect.height))
        # end of code to modify

        self.paintOutline(screen)


    # The "Shape" class is type "S".
    # A rectangle is "R", Triangle is "T" and Circle is "C"
    def getTypeName(self):
        return "S"

    def __str__(self):
        colour = self.getFillColour()
        shape_text = self.getTypeName() + ", " + str(colour[0]) + ", " + str(colour[1]) + ", " + str(colour[2])
        bound = self.getBounds()
        shape_text = shape_text + "," + str(bound.x) + "," + str(bound.y) + ","
        shape_text = shape_text + str(bound.width) + "," + str(bound.height)

        return shape_text


class ShapeController:
    _model: ShapeModel

    def __init__(self, model):
        self._model = model
        # Mouse handling variables
        self.mouseDown = False
        self.mouseStartPt = (0, 0)
        rect = self._model.getBounds()
        self.shapeStartPt = (rect.x, rect.y)


    #  GIVEN:  Handling the mouse events or at least making things easier.
    # Migrated to the ShapeController class.
    def handleUI(self, event) -> bool:
        if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN:
            mousePt = event.pos # 2-tuple for point
            ptIntersect = self._model.intersectsPt(mousePt)
            isHighlighted = self._model.isHighlighted()

            # Selection with a mouse down event will also update the starting point
            if event.type == pygame.MOUSEBUTTONDOWN and not self.mouseDown and ptIntersect:
                self._model.setSelected(True)
                self.mouseDown = True
                self.mouseStartPt = mousePt
                bound = self._model.getBounds()
                self.shapeStartPt = (bound.x, bound.y)
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN and not ptIntersect:
                self._model.setSelected(False)
                return False
            # Drag the shape.  Get the change in mouse position and move the shape that much
            elif event.type == pygame.MOUSEMOTION and self.mouseDown and ptIntersect:
                # bound = self.getBounds()
                newX = self.shapeStartPt[0] + mousePt[0] - self.mouseStartPt[0]
                newY = self.shapeStartPt[1] + mousePt[1] - self.mouseStartPt[1]
                self._model.moveShape(newX, newY)
                return True
            elif event.type == pygame.MOUSEBUTTONUP and self.mouseDown:
                newX = self.shapeStartPt[0] + mousePt[0] - self.mouseStartPt[0]
                newY = self.shapeStartPt[1] + mousePt[1] - self.mouseStartPt[1]
                self._model.moveShape(newX, newY)
                self.mouseDown = False
                return True
            elif event.type == pygame.MOUSEMOTION and (ptIntersect and (not isHighlighted)):
                self._model.setHighlighted(True)
                return True
            elif event.type == pygame.MOUSEMOTION and ((not ptIntersect) and isHighlighted):
                self._model.setHighlighted(False)
                # self.setSelected(False)
                return False
            else:
                return False


class ShapeView:
    _model: ShapeModel

    def __init__(self, model):
        self._model = model


    # GIVEN: Draw the outline surrounding the shape
    def paintOutline(self, screen):
        assert(self._model != None)
        if self._model.isSelected():
            pygame.draw.rect(screen, self._model.getOutlineColour(),
                             self._model.getBounds(),
                             self._model.getOutlineThickness())

    def paint(self, screen):
        assert (self._model != None)
        curr_rect = self._model.getBounds()
        fill_colour = self._model.getFillColour()

        # Draw an X instead of a rectangle shape to indicate this isn't a real
        # concrete shape (just like there is no "mammal" species)
        pygame.draw.line(screen, fill_colour, (curr_rect.x, curr_rect.y),
                         (curr_rect.x + curr_rect.width, curr_rect.y + curr_rect.height))
        pygame.draw.line(screen, fill_colour, (curr_rect.x + curr_rect.width, curr_rect.y),
                         (curr_rect.x, curr_rect.y + curr_rect.height))
        # end of code to modify

        self.paintOutline(screen)



class Shape2401:
    _model: ShapeModel
    _view: ShapeView
    _controller: ShapeController

    def __init__(self, rect, colour):
        # TODO: This will need to change when you refactor the code
        # The controller may not need child classes for each shape.
        # You will need a ShapeView child class for each new shape.
        self._model = ShapeModel(rect, colour)
        self._view = ShapeView(self._model)
        self._controller = ShapeController(self._model)

    # TODO: NEED TO CHANGE THIS
    def paint(self, screen):
        self._view.paint(screen)

    # TODO: Change this to use the controller
    def handleUI(self, event) -> bool:
        return self._controller.handleUI(event)