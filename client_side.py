import easygui
import pygame

from coms import *

pygame.init()

SCREEN_SIZE = (1000, 750)
DISPLAY_COLOUR = (0, 200, 0)
DEMO_IMAGE = "sprites/screen_demo.png"
FONT = "fonts/newyorkescape.ttf"
# FONT = "fonts/CHECKBK0.TTF"
# FONT = "fonts/Beef'd.ttf"
SWEEP_SPRITE = pygame.image.load("sprites/sweep.png")


class Display:
    def __init__(self, screen_size, grid_size, ship_name):
        self.grid_size = grid_size
        self._current_data = []
        self.objects = []
        self.screen_size = screen_size
        self.ship_name = ship_name
        self.cell_size = int(screen_size[1] / (grid_size[1] + 1))
        self.board_pos = (round((self.screen_size[0] - (self.cell_size * (self.grid_size[0] + 1))) / 2), 0)
        self.font = pygame.font.Font(FONT, round(self.cell_size * 0.5), bold=1)
        sweep_rect = (self.board_pos[0] + self.cell_size, self.board_pos[1] + self.cell_size,
                      (self.cell_size * self.grid_size[0]), (self.cell_size * self.grid_size[1]))
        self._sweep = Sweep(sweep_rect, round(self.screen_size[1] / 40), cell_size=self.cell_size)
        self._last_data_read = None
        self._getter = HTTPGetter()

    def add_entities(self, entities):
        pass

    def clear_entities(self, quick=False):
        pass

    def _draw_board(self, screen):
        for x in range(self.grid_size[0] + 1):
            start_pos = (self.board_pos[0] + (self.cell_size * (x + 1)),
                         self.board_pos[1] + self.cell_size)
            end_pos = (self.board_pos[0] + (self.cell_size * (x + 1)),
                       self.board_pos[1] + (self.cell_size * (self.grid_size[1] + 1)))
            pygame.draw.line(screen,
                             DISPLAY_COLOUR,
                             start_pos,
                             end_pos
                             )

            if x >= 1:
                char_render = self.font.render(str(x), 1, DISPLAY_COLOUR, (0, 0, 0))
                size = char_render.get_size()
                char_pos = ((x * self.cell_size) + self.board_pos[0] + (self.cell_size / 2) - (size[0] / 2),
                            self.board_pos[1] + (self.cell_size / 2) - (size[1] / 2))
                screen.blit(char_render, char_pos)

        for y in range(self.grid_size[1] + 1):
            start_pos = (self.board_pos[0] + self.cell_size,
                         self.board_pos[1] + (self.cell_size * (y + 1)))
            end_pos = (self.board_pos[0] + (self.cell_size * (self.grid_size[0] + 1)),
                       self.board_pos[1] + (self.cell_size * (y + 1)))
            pygame.draw.line(screen,
                             DISPLAY_COLOUR,
                             start_pos,
                             end_pos
                             )

            if y >= 1:
                char_render = self.font.render(chr(y + 64), 1, DISPLAY_COLOUR, (0, 0, 0))
                size = char_render.get_size()
                char_pos = (self.board_pos[0] + (self.cell_size / 2) - (size[0] / 2),
                            (y * self.cell_size) + self.board_pos[1] + (self.cell_size / 2) - (size[1] / 2))
                screen.blit(char_render, char_pos)

    def update(self):
        self._check_for_updates()

        for o in self.objects:
            o.update()
        self._sweep.update()

    def draw(self, screen):
        self._draw_board(screen)
        for o in self.objects:
            o.draw(screen)
        self._sweep.draw(screen)

    def sweep(self):
        self._sweep.reset()

    def _check_for_updates(self):
        new_data = self._getter.get()
        if new_data == self._last_data_read:
            return

    def _object_exists(self, obj):
        for o in self.objects:
            if o.matches(obj):
                return True
        return False


class ScreenObject:
    def __init__(self, pos, type_text, direction):
        self.pos = pos
        self.type_text = type_text
        self.direction = direction

    def matches(self, obj):
        return self.pos == obj.pos and self.type_text == obj.type_text and self.direction == obj.direction


class Sweep:
    def __init__(self, rect, speed=20, cell_size=20):
        self._rect = rect
        self._speed = speed
        self._sprite_width = 4 * cell_size
        self._sprite = pygame.transform.scale(SWEEP_SPRITE, (self._sprite_width, self._rect[3]))
        self._x_pos = -self._sprite_width
        self.finished = False

    def update(self):
        if self.finished:
            return
        self._x_pos += self._speed
        if self._x_pos > self._rect[2]:
            self.finished = True

    def draw(self, screen):
        if self.finished:
            return
        # pygame.draw.rect(screen, (255, 255, 255), self._rect, 1)
        # pygame.draw.rect(screen, (255, 255, 255),
        #                  (self._rect[0] + self._x_pos,
        #                   self._rect[1]) + (self._sprite.get_size()[0],
        #                                     self._sprite.get_size()[1]))

        if self._x_pos >= 0 and self._x_pos + self._sprite_width <= self._rect[2]:
            screen.blit(self._sprite, (self._rect[0] + self._x_pos, self._rect[1]))
        elif self._x_pos > self._rect[2] - self._sprite_width:
            screen.blit(self._sprite, (self._rect[0] + self._x_pos, self._rect[1]),
                        (0,  # Crop x
                         0,  # Crop y
                         self._sprite_width - ((self._x_pos + self._sprite_width) - self._rect[2]),  # Crop width
                         self._rect[3],  # Crop height
                         ))
        elif self._x_pos < 0 and abs(self._x_pos) < self._sprite_width:
            screen.blit(self._sprite,
                        (self._rect[0], self._rect[1]),  # Pos
                        (- self._x_pos,  # Crop x
                         0,  # Crop y
                         self._sprite_width + self._x_pos,  # Crop width
                         self._rect[3]  # Crop height
                         )
                        )
        else:
            pass

    def reset(self):
        self._x_pos = -self._sprite_width
        self.finished = False


def main():
    pygame.init()
    screen_size = SCREEN_SIZE

    ship_name = easygui.enterbox("Enter Ship Name:", "Sensor Viewer")
    if ship_name is None or ship_name == "":
        return
    full_screen = easygui.buttonbox("Select display mode:", "Sensor Viewer", ["Windowed", "Fullscreen"])
    if full_screen is None:
        return
    full_screen = (full_screen == "Fullscreen")

    # Initialise screen
    clock = pygame.time.Clock()

    if full_screen:
        screen_choices = ["Primary (This display)", "Secondary (Another display)"]
        resp = easygui.buttonbox("Choose display:", "Sensor Viewer", screen_choices)
        if resp is None:
            return
        if resp == screen_choices[0]:
            screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
            resp = easygui.multenterbox("Enter screen size:\n(resolution of secondary monitor)",
                                        "Sensor Viewer", ["Width:", "Height:"], list(screen_size))
            if resp is None:
                return
            else:
                screen_size = [int(i) for i in resp]
            resp = easygui.msgbox("Ensure that the secondary display is configured in Windows to be oriented directly "
                                  "above the primary display, and aligned along the left hand side as shown below:",
                                  "Sensor View",
                                  image=DEMO_IMAGE
                                  )
            if resp is None:
                return
            os.environ['SDL_VIDEO_WINDOW_POS'] = "0,-{}".format(screen_size[1])
            screen = pygame.display.set_mode(screen_size, pygame.NOFRAME)
    else:
        resp = easygui.multenterbox("Enter window size:",
                                    "Sensor Viewer", ["Width:", "Height:"], list(screen_size))
        if resp is None:
            return
        else:
            screen_size = [int(i) for i in resp]
        screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('{} Sensor Viewer'.format(ship_name))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    viewer = Display(screen_size, (20, 20), ship_name)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                viewer.sweep()

        viewer.update()

        screen.blit(background, (0, 0))
        viewer.draw(screen)
        pygame.display.flip()

        clock.tick(30)


main()
