import pygame
from random import randint


class Snake:
    size = 10

    def __init__(self) -> None:
        self.coords = [[randint(0, 800), randint(0, 600)]]

    def draw(self, screen) -> None:
        for x, y in self.coords:
            pygame.draw.rect(screen, 'lime', (x, y, self.size, self.size))

class Apple:
    ...


if __name__ == '__main__':
    pygame.init()
    screen_size = size_x, size_y = (800, 600)
    screen = pygame.display.set_mode(screen_size)
    snake = Snake()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((0, 0, 0))
        snake.draw(screen)
        pygame.display.update()