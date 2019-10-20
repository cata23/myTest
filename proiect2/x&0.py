# my fist app probably an x&0 game

import pygame
import time

x0 = "X"
grid = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]

winner = None

def initBoard(displaySize):
    background = pygame.surface(displaySize.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    #draw grid lines




class App:
    button_start = pygame.Rect(100, 100, 50, 50)

    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 500, 500

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("MENU")
        self._running = True
        self._image_surf = pygame.image.load("fundal.jpg").convert()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(mouse_pos)

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self._image_surf, (0, 0))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        white = (255, 255, 255)
        red = (255, 0, 0)
        button = pygame.Rect(100, 100, 50, 50)
        pygame.draw.rect(self._display_surf, [255, 0, 0], button)  # draw button
        pygame.display.update()
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
