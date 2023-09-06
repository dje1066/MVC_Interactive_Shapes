import pygame

import Shape2401
from ShapeFactory import ShapeFactory


class A5Canvas:
    """
    Class A5Canvas is the canvas or background on which everything is drawn.  We also use it to control
    the program since all the shapes are drawn ON the canvas and manipulated / created via the canvas
    A5Canvas just has a list of shapes that are created, drawn and manipulated
    You don't have to understand this class but it could help:
    Click and drag the mouse on the screen to draw an X shape (a Shape2400 object).
    Your job is to implement other shapes that a child classes of Shape2400.  Use combinations of the shift and
    control keys (when drawing) to determine the kind of shape.
    """

    # static variables....unfortunately python has no constants like C/Java/C++
    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 500
    screen = pygame.display.set_mode([DEFAULT_WIDTH, DEFAULT_HEIGHT])

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True

        # Variables for the mouse dragging event
        self.mouseDownPt = (0, 0)
        self.currentMousePt = (0, 0)
        self.mouseDown = False
        self.drawingShape = False

        self.dragRect = pygame.Rect(0, 0, 0, 0)
        self.shapeList = list()

        self.screen = pygame.display.set_mode([self.width, self.height])

    # getter method for determining if the program is still running
    # returns a bool
    def isRunning(self) -> bool:
        return self.running

    def setRunning(self, run):
        self.running = run

    # returns int: the width of the canvas/screen
    def getWidth(self) -> int:
        return self.width

    # returns int: the height of the canvas/screen
    def getHeight(self) -> object:
        return self.height

    def isMouseDown(self):
        return self.mouseDown

    # Calculate the minimum bounding rectangle that contains points pt1 and pt2
    def calcBoundRect(self, pt1: tuple, pt2: tuple) -> pygame.Rect:
        boundRect = pygame.Rect(pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1])
        if pt1[0] > pt2[0]:
            boundRect.x = pt2[0]
            boundRect.width = pt1[0] - pt2[0]
        if pt1[1] > pt2[1]:
            boundRect.y = pt2[1]
            boundRect.height = pt1[1] - pt2[1]
        return boundRect

    def updateDragShape(self, event, isdown):
        self.currentMousePt = event.pos

        # Start the drag rectangle
        if isdown and not self.mouseDown:
            self.mouseDownPt = event.pos
            self.mouseDown = True
            self.dragRect = self.calcBoundRect(self.mouseDownPt, self.mouseDownPt)
            self.drawingShape = True
        # Finish the drag rectangle
        elif not isdown and self.mouseDown:
            # Generate a new shape and remove the old drag shape
            self.dragRect = self.calcBoundRect(self.mouseDownPt, self.currentMousePt)
            assert isinstance(self.dragRect, pygame.Rect)
            newShape = ShapeFactory.createFromMouse(self.dragRect, event)
            print("New Shape: " + str(newShape))

            self.shapeList.append(newShape)
            self.dragRect = pygame.Rect(0, 0, 0, 0)
            self.mouseDownPt = event.pos
            self.mouseDown = False
            self.drawingShape = False
        # Update the Drag rect
        elif self.mouseDown:
            self.dragRect = self.calcBoundRect(self.mouseDownPt, self.currentMousePt)

    # Return the rectangular region currently being identified by the user clicking and dragging.
    def getDragRect(self) -> pygame.rect:
        return self.dragRect

    # Return all the shapes currently created for the canvas.
    def getShapes(self):
        return self.shapeList

    """
    Paint method for drawing the canvas
    You then call paint on each of the shape objects
    """
    def paint(self):
        self.screen.fill((255, 255, 255))

        dragRect = self.getDragRect()
        assert isinstance(dragRect, pygame.Rect)
        shapeList = self.getShapes()

        # Draw the mouse dragging rectangle to help you create a new shape
        if dragRect.width > 1 and dragRect.height > 1:
            pygame.draw.rect(self.screen, (225, 225, 200), dragRect, 5)

        # Draw all the shapes you've made
        for currShape in shapeList:
            assert isinstance(currShape, Shape2401.Shape2401)
            currShape.paint(self.screen)

        # Finally flip the back buffer....draw the screen to the ACTUAL screen.
        pygame.display.flip()

    """
    This chunk of functions all involves the mouse events and user actions
    Notice this has nothing / little to do with the class data.  It only deals with user input
    and then calls mutator and accessor methods to access class data (we'll see why soon).
    """
    def handleDragDraw(self, event) -> bool:
        """
        event: pygame event include mouse, keyboard and control events.
        :rtype: bool
        """
        # Start to make a new shape based on mouse down then mouse up.
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.isMouseDown():
                self.updateDragShape(event, True)
                return True
            return False
        elif event.type == pygame.MOUSEMOTION and self.isMouseDown():
            self.updateDragShape(event, True)
            return True
        elif event.type == pygame.MOUSEBUTTONUP and self.isMouseDown():
            self.updateDragShape(event, False)
            return True
        else:
            return False

    # Function for handling all mouse events that move existing shapes.
    # Returns False if nothing is moved
    def handle_shape_move(self, event):
        # if already drawing a new shape, don't move shapes
        if self.drawingShape:
            return False
        # see the first shape that might be moved.  overlapping shapes are a problem
        shape_list = self.getShapes()
        shape_move = False
        for curr_shape in shape_list:
            assert isinstance(curr_shape, Shape2401.Shape2401)
            shape_move = curr_shape.handleUI(event) or shape_move
        return shape_move

    def handleUIEvent(self, event) -> bool:
        if event.type == pygame.QUIT:
            self.setRunning(False)
            return True

        # Now either draw a new shape OR move existing shapes if there is a mouse event.
        shape_move = self.handle_shape_move(event)
        if not shape_move:
            draw_event = self.handleDragDraw(event)
            return draw_event
        else:
            return shape_move
