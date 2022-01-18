import pygame, sys
import map_design as levels

# SCREEN SETUP
# SCREEN CONSTANTS
screen_w = 1000
screen_h = 600
block_size = 50

FPS = 60

screen = pygame.display.set_mode((screen_w, screen_h))

pygame.display.set_caption('Ninja platformer')

clock = pygame.time.Clock()


# COLORS
WHITE = (255, 255, 255)
BLACK = (0,0,0)
YELLOW = (242, 235, 31)
GREEN = (31, 242, 137)
RED = (255, 0, 0)


# ninja numbers

x_margin = 10
y_margin = 11
x_pad = 19
y_pad = 17


# SPRITE SHEET METHODS
################################################################################
class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    def images_at(self, rects, colorkey=None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]


    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0, y_margin=0, y_padding=0, width = None, height = None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.

        if width and height:
            x_sprite_size = width
            y_sprite_size = height

        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                             - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                             - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)



# PLAYER CLASS
class player(pygame.sprite.Sprite):
    def __init__(self, picture_path, h_vel, v_vel):
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()

        self.h_vel = h_vel
        self.v_vel = v_vel

    def h_move(self):
        self.rect.x += self.vel

    def jump(self):
        pass





############################################################################################
############################################################################################
# DEFINE EACH NINJA ANIMATION
ninja_sheet = SpriteSheet('ninja-black-32x32.png')

ninja_list = ninja_sheet.load_grid_images(6, 12, x_margin, x_pad, y_margin, y_pad)
# print(ninja_list)


# IDLE
ninja_idle = ninja_sheet.image_at((11, 11, 18, 16)).convert_alpha()
ninja_idle = pygame.transform.scale(ninja_idle, (block_size, block_size))


# RUNNING

ninja_run1 = ninja_sheet.image_at((40, 107, 12, 16)).convert_alpha()
ninja_run1 = pygame.transform.scale(ninja_run1, (block_size, block_size))

ninja_run2 = ninja_sheet.image_at((40, 43, 12, 16)).convert_alpha()
ninja_run2 = pygame.transform.scale(ninja_run2, (block_size, block_size))

ninja_run3 = ninja_sheet.image_at((41, 11, 12, 16)).convert_alpha()
ninja_run3 = pygame.transform.scale(ninja_run3, (block_size, block_size))

ninja_run4 = ninja_run2

run_rt_list = [ninja_run1, ninja_run2, ninja_run3, ninja_run4]

run_lt_list = [pygame.transform.flip(player, True, False) for player in run_rt_list]



# GAME BACKGROUND
moon_bg = 'Moon-Mountain-BG.png'
moon_bg = pygame.image.load(moon_bg).convert_alpha()




###################################################################################
def draw_grid(width, height, size):

    for x in range(1, width, size):
        for y in range(1, height, size):
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, BLACK, rect, 2)

player_delay = 1000
player_run_prev = pygame.time.get_ticks()


#########################################################################
############################## MAP LAYOUT ###############################
#########################################################################

class Level:
    def __init__(self, layout, block_size):
        self.layout = layout
        self.tile_list = []
        self.tile_plants = []
        self.block_size = block_size


        temple_sheet = SpriteSheet('Temple_spritesheet.png')
        gate_sheet = SpriteSheet('Japan_Gate.png')

    # GAME OBJECTS
        gate = gate_sheet.image_at((228, 372, 732, 541)).convert_alpha()
        gate = pygame.transform.scale(gate, (self.block_size, self.block_size))


        # GROUND
        temple_ground = temple_sheet.image_at((290, 480, 32, 32)).convert_alpha()
        temple_ground = pygame.transform.scale(temple_ground, (self.block_size, self.block_size))


        # PLANTS
        tree_big = temple_sheet.image_at((396, 296, 107, 109)).convert_alpha()
        tree_big = pygame.transform.scale(tree_big, (self.block_size * 2, self.block_size * 2))

        tree_small = temple_sheet.image_at((430, 199, 71, 82), -1).convert_alpha()
        tree_small = pygame.transform.scale(tree_small, (self.block_size * 1.5, self.block_size * 2))

        self.hedge_small = temple_sheet.image_at((370, 268, 34, 20)).convert_alpha()
        self.hedge_small = pygame.transform.scale(self.hedge_small, (self.block_size * 1.5, self.block_size))


        # TEMPLE PLATFORMS
        platform_big = temple_sheet.image_at((256, 288, 64, 24)).convert_alpha()
        platform_big = pygame.transform.scale(platform_big, (self.block_size * 2, self.block_size))

        platform_small = pygame.transform.scale(platform_big, (self.block_size, self.block_size / 1.5))

        platform_long = temple_sheet.image_at((0, 320, 255, 21)).convert_alpha()
        platform_long = pygame.transform.scale(platform_long, (350, 30))



        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * self.block_size
                y_val = i * self.block_size

                if col == 'G':
                    image_rect = temple_ground.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (temple_ground, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'B':
                    image_rect = platform_big.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (platform_big, (image_rect))
                    self.tile_list.append(tile)


                elif col == 'S':
                    image_rect = platform_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (platform_small, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'L':
                    image_rect = platform_long.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (platform_long, (image_rect))
                    self.tile_list.append(tile)


                elif col =='d':
                    image_rect = gate.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (gate, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'b':
                    image_rect = tree_big.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (tree_big, (image_rect))
                    self.tile_plants.append(tile)

                elif col == 's':
                    image_rect = tree_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (tree_small, (image_rect))
                    self.tile_plants.append(tile)

                elif col == 'h':
                    image_rect = self.hedge_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.hedge_small, (image_rect))
                    self.tile_plants.append(tile)


    def draw(self):
        for tile in self.tile_list:

            screen.blit(tile[0], tile[1])

    def draw_plants(self):

        for tile in self.tile_plants:

            screen.blit(tile[0], tile[1])


level_1 = Level(levels.Level_1, block_size)
level_1_plants = Level(levels.Level_1_plants, block_size)


while True:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        player_run_current = pygame.time.get_ticks()


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(moon_bg, (0,0))

    # draw_grid(screen_w, screen_h, block_size)

    level_1.draw()
    level_1_plants.draw_plants()


    pygame.display.flip()
    clock.tick(FPS)























