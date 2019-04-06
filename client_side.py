import easygui
import pygame

pygame.init()

SCREEN_SIZE = (1000, 750)
DISPLAY_COLOUR = (0, 200, 0)


class Display:
    def __init__(self):
        self._grid_size = ()
        self._current_data = []

    def add_entities(self, entities):
        pass

    def clear_entities(self, quick=False):
        pass

    def draw(self, screen):
        pass


def main():
    ship_name = easygui.enterbox("Enter Ship Name:", "Sensor Viewer")
    if ship_name is None or ship_name == "":
        return
    full_screen = easygui.buttonbox("Select display mode:", "Sensor Viewer", ["Windowed", "Fullscreen"])
    if full_screen is None:
        return
    full_screen = (full_screen == "Fullscreen")
    screen_number = 1
    if full_screen and pygame.display.get_num_displays() > 1:
        screen_number = easygui.buttonbox("Select screen:",
                                          "Sensor View",
                                          [str(i + 1) for i in range(pygame.display.get_num_displays())])
        if screen_number is None:
            return

    # Initialise screen
    pygame.init()
    clock = pygame.time.Clock()

    if full_screen:
        screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN, display=screen_number)
    else:
        screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption('{} Sensor Screen'.format(ship_name))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    viewer = Display()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        screen.blit(background, (0, 0))
        viewer.draw(screen)
        pygame.display.flip()

        clock.tick(30)

main()