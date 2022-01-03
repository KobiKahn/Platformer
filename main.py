import pygame, sys

clock = pygame.time.Clock()

screen_w = 1000
screen_h = 600

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption('Ninja platformer')

tile_size = 3

class grid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, length):
        super().__init__()
        self.x = x
        self.y = y

        self.width = width
        self.length = length

    def draw_grid(self):
        pygame.draw.rect(screen, (255, 255, 255), ((self.x, self.y), (self.width, self.length)))

Grid = grid(0,0,0,0)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0,0,0))

    for x in range(1, screen_h // tile_size):
        pygame.draw.rect(screen, (255,255,255), (x * tile_size, 0, 3, screen_h))

    for x in range(1, screen_w // tile_size):
        pygame.draw.rect(screen, (255,255,255), (x * tile_size), 0, 3, screen_w)



    pygame.display.flip()
    clock.tick(60)























