import pygame as pg
from A5Canvas import *

def bare_pygame():
    pygame.init()
    screen = pg.display.set_mode([500, 500])
    running = True

    red = 50
    blue = 50
    green = 50
    background = (red, green, blue)

    pg.time.set_timer(pygame.USEREVENT, 100, 0)
    while running is True:
        for event in pg.event.get():
            # Throwing all events at the MVC_Canvas class
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.USEREVENT:
                red = (red + 2) % 255
                green = (green + 1) % 255
                blue = (blue + 3) % 255
                background = (red, green, blue)
                screen.fill(background)
                screen.set_at([40, 40], (0, 0, 0))
                pg.display.flip()
    pg.quit


# basic starter method to set everything up.
# Notice that everything in handled by A5Canvas
def main():
    pygame.init()
    # screen = pygame.display.set_mode([500, 500])
    canvas = A5Canvas(500, 500)

    while canvas.isRunning():
        for event in pygame.event.get():
            # Throwing all events at the MVC_Canvas class
            canvas.handleUIEvent(event)
            canvas.paint()
    pygame.quit

# Demo used for class....and to show you how pygame works.
# Just switch the commenting from bare_pygame and main to see the bare program
#bare_pygame()

main()
# End of main
