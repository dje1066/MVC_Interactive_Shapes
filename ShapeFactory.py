from pygame import *

from Shape2401 import *
from Rect2401 import *
from Circle2401 import *
from Triangle2401 import *

"""
This class is used to hide what different versions of shapes exist (information hiding)
This one class knows about the various shapes that can be drawn (useful in the next assignment)
It also lets us abstract away how shapes are drawn with the mouse
"""
TYPE_TRIANGLE = 'Triangle2401'
TYPE_RECT = 'Rect2401'
TYPE_CIRCLE = 'Circle2401'
TYPE_SHAPE = 'Shape2401'
TYPE_ARROW = 'Arrow2401'

shape_types = {TYPE_TRIANGLE, TYPE_RECT, TYPE_CIRCLE, TYPE_SHAPE, TYPE_ARROW}

class ShapeFactory:

    def createShape(type, bound_rect):
        # Confirm this is a legitimate shape type name
        assert(type in shape_types)

        # TODO: Add other shapes that can be drawn (based on "type")
        if type == 'Triangle2401':
            # Make a triangle
            return Triangle2401(bound_rect, (0, 255, 0))
        elif type == 'Rect2401':
            # Make a "rect"
            return Rect2401(bound_rect, (0, 0, 255))
        elif type == 'Circle2401':
            # Make a circle
            return Circle2401(bound_rect, (255, 40, 40))
        else:
            return Shape2401(bound_rect, (150, 150, 150))

    def createFromMouse(bound_rect, event_flags):
        mods = pygame.key.get_mods()
        # Indicates the shift AND CTRL keys are pressed when clicking and dragging.
        if (mods & pygame.KMOD_SHIFT) and (mods & pygame.KMOD_CTRL):
            # Make a triangle
            return ShapeFactory.createShape(TYPE_TRIANGLE, bound_rect)
        # TODO: Add other drawing options for other shapes.
        elif mods & pygame.KMOD_SHIFT:
            # Make bonus shape
            return ShapeFactory.createShape(TYPE_ARROW, bound_rect)
        elif mods & pygame.KMOD_CTRL:
            # Make a circle
            return ShapeFactory.createShape(TYPE_CIRCLE, bound_rect)
        else:
            return ShapeFactory.createShape(TYPE_RECT, bound_rect)

