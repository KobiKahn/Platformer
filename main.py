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


# GAME SPRITE_SHEET

temple_sheet = SpriteSheet('Temple_spritesheet.png')





############################################################################################
############################################################################################
# GAME OBJECTS

# GROUND
temple_ground = temple_sheet.image_at((290, 480, 32, 32)).convert_alpha()
temple_ground = pygame.transform.scale(temple_ground, (50, 50))

# PLANTS

tree_big = temple_sheet.image_at((396, 296, 107, 109)).convert_alpha()

tree_small = temple_sheet.image_at((430, 199, 71, 82), -1).convert_alpha()

bush_small = temple_sheet.image_at((370, 268, 34, 20)).convert_alpha()
bush_small = pygame.transform.scale(bush_small, (50, 30))

# TEMPLE PLATFORMS
platform_large = temple_sheet.image_at((256, 288, 64, 24)).convert_alpha()
platform_large = pygame.transform.scale(platform_large, (100, 35))

platform_small = pygame.transform.scale(platform_large, (60, 30))

platform_long = temple_sheet.image_at((0, 320, 255, 21)).convert_alpha()
platform_long = pygame.transform.scale(platform_long, (350, 30))



############################################################################################
############################################################################################
# DEFINE EACH NINJA ANIMATION
ninja_sheet = SpriteSheet('ninja-black-32x32.png')

ninja_list = ninja_sheet.load_grid_images(6, 12, x_margin, x_pad, y_margin, y_pad)
# print(ninja_list)



# IDLE
ninja_idle = ninja_sheet.image_at((11, 11, 18, 16)).convert_alpha()
ninja_idle = pygame.transform.scale(ninja_idle, (45, 50))


# RUNNING

ninja_run1 = ninja_sheet.image_at((40, 107, 12, 16)).convert_alpha()
ninja_run1 = pygame.transform.scale(ninja_run1, (45, 50))

ninja_run2 = ninja_sheet.image_at((40, 43, 12, 16)).convert_alpha()
ninja_run2 = pygame.transform.scale(ninja_run2, (45, 50))

ninja_run3 = ninja_sheet.image_at((41, 11, 12, 16)).convert_alpha()
ninja_run3 = pygame.transform.scale(ninja_run3, (45, 50))

ninja_run4 = ninja_run2

run_rt_list = [ninja_run1, ninja_run2, ninja_run3, ninja_run4]

run_lt_list = [pygame.transform.flip(player, True, False) for player in run_rt_list]



# GAME BACKGROUND
moon_bg = 'Moon-Mountain-BG.png'
moon_bg = pygame.image.load(moon_bg).convert_alpha()




###################################################################################
# def draw_grid(width, height, size):

#     for x in range(1, width, size):
#         for y in range(1, height, size):
#             rect = pygame.Rect(x, y, size, size)
#             pygame.draw.rect(screen, BLACK, rect, 2)

player_delay = 1000
player_run_prev = pygame.time.get_ticks()


#########################################################################
############################## MAP LAYOUT ###############################
#########################################################################



while True:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        player_run_current = pygame.time.get_ticks()


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(moon_bg, (0,0))

# DRAW GROUND
    for i in range(2):
        for j in range(0, screen_w // block_size):
            screen.blit(temple_ground, (j* block_size, screen_h - block_size * i))


    screen.blit(platform_large, (200, 300))
    screen.blit(platform_small, (500, 300))
    screen.blit(platform_long, (300, 100))
    screen.blit(tree_big, (100, 444))
    screen.blit(tree_small, (100, 470))
    screen.blit(ninja_idle, (50, 505))
    screen.blit(bush_small, (400, 550))
    # draw_grid(screen_w, screen_h, block_size)



    pygame.display.flip()
    clock.tick(FPS)























