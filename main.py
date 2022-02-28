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
    def __init__(self, picture_path, x, y, tile_set, plant_set):

        self.tile_set = tile_set
        self.plant_set = plant_set

        self.ninja_sheet = SpriteSheet(picture_path)

        self.last = pygame.time.get_ticks()
        self.image_delay = 100
        self.current_frame = 0

        self.right = True
        self.left = False

        self.falling = False
        self.jumping = False
        self.y_vel = 0
        self.jump_count = 10
        self.gravity = 3

        self.cam_left = False
        self.cam_right = False
        self.free_move = True

        # IDLE
        self.ninja_idle_rt = self.ninja_sheet.image_at((444, 49, 141, 229), -1)
        self.ninja_idle_rt = pygame.transform.scale(self.ninja_idle_rt, (block_size * .95, block_size * 1.25))
        self.ninja_idle_lt = pygame.transform.flip(self.ninja_idle_rt, True, False)

        self.image = self.ninja_idle_rt
        self.image_rect = self.image.get_rect()

        self.image_rect.x = x
        self.image_rect.y = y


        # RUNNING ANIMATIONS
        # self.ninja_run_rt_list_wrong = self.ninja_sheet.load_grid_images(1, 10, 450, 60, 1026, 0, 155, 228, -1)
        self.ninja_run_rt_wrong = []
        self.ninja_run_rt = []


        # GET EACH RUN
        self.ninja_run_rt_1 = self.ninja_sheet.image_at((450, 1026, 152, 221), -1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_1)

        self.ninja_run_rt_2 = self.ninja_sheet.image_at((645, 795, 150, 222), -1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_2)

        self.ninja_run_rt_3 = self.ninja_sheet.image_at((882, 1031, 142, 223), -1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_3)

        self.ninja_run_rt_4 = self.ninja_sheet.image_at((1074, 1033, 138, 224), -1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_4)

        self.ninja_run_rt_5 = self.ninja_sheet.image_at((1260, 1035, 139, 226), - 1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_5)

        self.ninja_run_rt_6 = self.ninja_sheet.image_at((1431, 1034, 141, 228), - 1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_6)

        self.ninja_run_rt_7 = self.ninja_sheet.image_at((1616, 1033, 139, 224), - 1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_7)

        self.ninja_run_rt_8 = self.ninja_sheet.image_at((1809, 1032, 141, 224), - 1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_8)

        self.ninja_run_rt_9 = self.ninja_sheet.image_at((1998, 1031, 141, 224), - 1)
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_9)

        self.ninja_run_rt_10 = self.ninja_idle_rt
        self.ninja_run_rt_wrong.append(self.ninja_run_rt_10)

        for player in self.ninja_run_rt_wrong:
            player = pygame.transform.scale(player, (block_size * .95, block_size * 1.25))
            self.ninja_run_rt.append(player)

        self.ninja_run_lt = [pygame.transform.flip(player, True, False) for player in self.ninja_run_rt]

        # HITTING ANIMATIONS
        self.ninja_hit_rt_wrong = self.ninja_sheet.load_grid_images(1, 10, 445, 56, 515, 0, 140, 222, -1)
        self.ninja_hit_rt = []

        self.ninja_hit_rt_1 = self.ninja_sheet.image_at((445, 547, 140, 222), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_1)

        self.ninja_hit_rt_2 = self.ninja_sheet.image_at((639, 554, 161, 214), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_2)

        self.ninja_hit_rt_3 = self.ninja_sheet.image_at((800, 555, 155, 210), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_3)

        self.ninja_hit_rt_4 = self.ninja_sheet.image_at((990, 559, 173, 206), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_4)

        self.ninja_hit_rt_5 = self.ninja_sheet.image_at((1181, 554, 179, 213), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_5)

        self.ninja_hit_rt_6 = self.ninja_sheet.image_at((1379, 539, 149, 230), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_6)

        self.ninja_hit_rt_7 = self.ninja_sheet.image_at((1579, 539, 147, 256), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_7)

        self.ninja_hit_rt_8 = self.ninja_sheet.image_at((1757, 548, 146, 257), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_8)

        self.ninja_hit_rt_9 = self.ninja_sheet.image_at((1949, 544, 132, 241), -1)
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_9)

        self.ninja_hit_rt_10 = self.ninja_idle_rt
        self.ninja_hit_rt_wrong.append(self.ninja_hit_rt_10)

        for player in self.ninja_hit_rt_wrong:
            player = pygame.transform.scale(player, (block_size * .95, block_size * 1.25))
            self.ninja_hit_rt.append(player)

        self.ninja_hit_lt = [pygame.transform.flip(player, True, False) for player in self.ninja_hit_rt]

        # JUMPING ANIMATION
        self.ninja_jump_rt_wrong = self.ninja_sheet.load_grid_images(1, 10, 437, 46, 1262, 0, 158, 213, -1)
        self.ninja_jump_rt = []

        self.ninja_jump_rt_1 = self.ninja_idle_rt
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_1)

        self.ninja_jump_rt_2 = self.ninja_sheet.image_at((636, 1262, 159, 216), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_2)

        self.ninja_jump_rt_3 = self.ninja_sheet.image_at((827, 1262, 168, 219), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_3)

        self.ninja_jump_rt_4 = self.ninja_sheet.image_at((1031, 1265, 176, 218), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_4)

        self.ninja_jump_rt_5 = self.ninja_sheet.image_at((1242, 1266, 176, 216), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_5)

        self.ninja_jump_rt_6 = self.ninja_jump_rt_5
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_6)

        self.ninja_jump_rt_7 = self.ninja_sheet.image_at((1631, 1265, 176, 215), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_7)

        self.ninja_jump_rt_8 = self.ninja_sheet.image_at((1832, 1263, 170, 216), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_8)

        self.ninja_jump_rt_9 = self.ninja_sheet.image_at((2042, 1263, 158, 216), -1)
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_9)

        self.ninja_jump_rt_10 = self.ninja_idle_rt
        self.ninja_jump_rt_wrong.append(self.ninja_jump_rt_10)

        for player in self.ninja_jump_rt_wrong:
            player = pygame.transform.scale(player, (block_size * .95, block_size * 1.25))
            self.ninja_jump_rt.append(player)

        self.ninja_jump_lt = [pygame.transform.flip(player, True, False) for player in self.ninja_jump_rt]


    def camera_move(self, dx):

        for tile in self.plant_set:
            tile[1].x += dx

        for tile in self.tile_set:
            if not tile[1].colliderect(self.image_rect.x + (-1 * dx), self.image_rect.y, self.image_rect.width, self.image_rect.height):
                # print('HIT')
                tile[1].x += dx




    def update(self):
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if self.image_rect.x > 200 and self.image_rect.x < screen_w - 200:
            self.free_move = True

        else:
            self.free_move = False

        # RUN RIGHT
        if keys[pygame.K_RIGHT]:
            if self.free_move:
                self.cam_right = False
                self.cam_left = False
                self.left = False
                self.right = True
                now = pygame.time.get_ticks()
                dx = 5

                if (now - self.last) >= self.image_delay and self.jumping == False:
                    self.last = now

                    if (self.current_frame + 1) < len(self.ninja_run_rt):
                        self.current_frame += 1
                    else:
                        self.current_frame = 0
                    self.image = self.ninja_run_rt[self.current_frame]


            elif self.image_rect.x >= screen_w - 200:
                self.free_move = False
                self.cam_right = True
                self.cam_left = False
                dx = 0
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay and self.jumping == False:
                    self.last = now
                    if (self.current_frame + 1) < len(self.ninja_run_rt):
                        self.current_frame += 1
                    else:
                        self.current_frame = 0
                    self.image = self.ninja_run_rt[self.current_frame]

                # self.camera_move(-5)


            elif self.image_rect.x <= 200:
                self.free_move = True
                self.image_rect.x = 201


            # RUN LEFT
        elif keys[pygame.K_LEFT]:
            if self.free_move:
                self.cam_right = False
                self.cam_left = False
                self.left = True
                self.right = False
                dx = -5
                now = pygame.time.get_ticks()

                if (now - self.last) >= self.image_delay and self.jumping == False:
                    self.last = now

                    if (self.current_frame + 1) < len(self.ninja_run_lt):
                        self.current_frame += 1
                    else:
                        self.current_frame = 0

                    self.image = self.ninja_run_lt[self.current_frame]
            # CHECK IF CAMERA MOVE OR NOT
            elif self.image_rect.x <= 200:
                self.free_move = False
                self.cam_left = True
                self.cam_right = False

                dx = 0
                now = pygame.time.get_ticks()
                if (now - self.last) >= self.image_delay and self.jumping == False:
                    self.last = now
                    if (self.current_frame + 1) < len(self.ninja_run_lt):
                        self.current_frame += 1
                    else:
                        self.current_frame = 0
                    self.image = self.ninja_run_lt[self.current_frame]

                # self.camera_move(5)

            # CHECK IF FREE MOVE
            elif self.image_rect.x >= screen_w - 200:
                self.free_move = True
                self.image_rect.x = screen_w - 201


        elif keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            # RIGHT HITTING ANIMATION
            if self.right:
                if (now - self.last) >= self.image_delay:
                    self.last = now
                    if (self.current_frame + 1) < len(self.ninja_hit_rt):
                        self.current_frame += 1

                    else:
                        self.current_frame = 0
                    self.image = self.ninja_hit_rt[self.current_frame]
            # LEFT HITTING ANIMATION
            else:
                if (now - self.last) >= self.image_delay:
                    self.last = now
                    if (self.current_frame + 1) < len(self.ninja_hit_lt):
                        self.current_frame += 1

                    else:
                        self.current_frame = 0
                    self.image = self.ninja_hit_lt[self.current_frame]


        # IDLE
        else:
            self.current_frame = 0
            dx = 0

            if self.right:
                self.image = self.ninja_idle_rt

            elif self.left:
                self.image = self.ninja_idle_lt


        # JUMPING MECHANIC
        if keys[pygame.K_UP] and not self.jumping and not self.falling:

            self.jumping = True
            self.y_vel = -13

        dy += self.y_vel
        self.y_vel += 1

        if self.y_vel < 0:
            self.jumping = True
            self.falling = False
        
        else: 
            self.jumping = False
            self.falling = True


# COLLISION DETECTION
        if self.free_move:
            for tile in self.tile_set:
                if tile[1].colliderect(self.image_rect.x + dx, self.image_rect.y, self.image_rect.width, self.image_rect.height):
                    dx = 0
        else:
            for tile in self.tile_set:
                if tile[1].colliderect(self.image_rect.x + 5, self.image_rect.y, self.image_rect.width, self.image_rect.height):
                    self.cam_right = False

                elif tile[1].colliderect(self.image_rect.x - 5, self.image_rect.y, self.image_rect.width, self.image_rect.height):
                    self.cam_left = False


        for tile in self.tile_set:
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y + dy, self.image_rect.width, self.image_rect.height):

                if self.y_vel < 0:
                    dy = tile[1].bottom - self.image_rect.top
                    self.y_vel = 0
                    self.jumping = False
                    self.falling = True

                elif self.y_vel > 0:
                    dy = tile[1].top - self.image_rect.bottom
                    self.y_vel = 0
                    self.jumping = False
                    self.falling = False

        if self.cam_left and keys[pygame.K_LEFT]:
            self.camera_move(5)
            dx = 0

        elif self.cam_right and keys[pygame.K_RIGHT]:
            self.camera_move(-5)
            dx = 0

        self.image_rect.x += dx
        self.image_rect.y += dy



        self.draw()

    def draw(self):
        screen.blit(self.image, self.image_rect)
        # pygame.draw.rect(screen, (255,255,255), self.image_rect, 2)



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
        self.gate = gate_sheet.image_at((228, 372, 732, 541)).convert_alpha()
        self.gate = pygame.transform.scale(self.gate, (self.block_size, self.block_size))


        # GROUND
        self.temple_ground = temple_sheet.image_at((290, 480, 32, 32)).convert_alpha()
        self.temple_ground = pygame.transform.scale(self.temple_ground, (self.block_size, self.block_size))


        # PLANTS
        self.tree_big = temple_sheet.image_at((396, 296, 107, 109)).convert_alpha()
        self.tree_big = pygame.transform.scale(self.tree_big, (self.block_size * 2, self.block_size * 2))

        self.tree_small = temple_sheet.image_at((430, 199, 71, 82), -1).convert_alpha()
        self.tree_small = pygame.transform.scale(self.tree_small, (self.block_size * 1.5, self.block_size * 2))

        self.hedge_small = temple_sheet.image_at((370, 268, 34, 20)).convert_alpha()
        self.hedge_small = pygame.transform.scale(self.hedge_small, (self.block_size * 1.5, self.block_size))


        # TEMPLE PLATFORMS
        self.platform_big = temple_sheet.image_at((256, 288, 64, 24)).convert_alpha()
        self.platform_big = pygame.transform.scale(self.platform_big, (self.block_size * 2, self.block_size))

        self.platform_small = pygame.transform.scale(self.platform_big, (self.block_size, self.block_size / 1.5))

        self.platform_xsmall = pygame.transform.scale(self.platform_big, (self.block_size / 1.5, self.block_size / 1.5))

        self.platform_long = temple_sheet.image_at((0, 320, 255, 21)).convert_alpha()
        self.platform_long = pygame.transform.scale(self.platform_long, (350, 30))

        # TEMPLE WALLS
        self.pillar_bottom = temple_sheet.image_at((225, 224, 31, 96)).convert_alpha()
        self.pillar_bottom = pygame.transform.scale(self.pillar_bottom, (block_size, block_size))

        self.pillar_top = pygame.transform.flip(self.pillar_bottom, False, True)

    def make_layout(self):
        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * self.block_size
                y_val = i * self.block_size

                if col == 'G':
                    image_rect = self.temple_ground.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.temple_ground, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'B':
                    image_rect = self.platform_big.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.platform_big, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'p':
                    image_rect = self.pillar_bottom.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.pillar_bottom, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'P':
                    image_rect = self.pillar_top.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.pillar_top, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'S':
                    image_rect = self.platform_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.platform_small, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'X':
                    image_rect = self.platform_xsmall.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.platform_xsmall, (image_rect))
                    self.tile_list.append(tile)

                elif col == 'L':
                    image_rect = self.platform_long.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.platform_long, (image_rect))
                    self.tile_list.append(tile)


                elif col =='d':
                    image_rect = self.gate.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.gate, (image_rect))
                    self.tile_list.append(tile)

        return(self.tile_list)


    def make_plant_layout(self):
        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                x_val = j * self.block_size
                y_val = i * self.block_size

                if col == 'b':
                    image_rect = self.tree_big.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.tree_big, (image_rect))
                    self.tile_plants.append(tile)

                elif col == 's':
                    image_rect = self.tree_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.tree_small, (image_rect))
                    self.tile_plants.append(tile)

                elif col == 'h':
                    image_rect = self.hedge_small.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val

                    tile = (self.hedge_small, (image_rect))
                    self.tile_plants.append(tile)

        return(self.tile_plants)


    def draw(self):
        for tile in self.tile_list:

            screen.blit(tile[0], tile[1])




    def draw_plants(self):

        for tile in self.tile_plants:

            screen.blit(tile[0], tile[1])



def draw_grid(width, height, size):

    for x in range(1, width, size):
        for y in range(1, height, size):
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, BLACK, rect, 2)




level_1 = Level(levels.Level_1, block_size)
layout_list = level_1.make_layout()

level_1_plants = Level(levels.Level_1_plants, block_size)
plant_list = level_1_plants.make_plant_layout()



ninja = player('SamuraiLight.png', 410, 495, layout_list, plant_list)

################## IMAGES #######################
# GAME BACKGROUND
moon_bg = 'Moon-Mountain-BG.png'
moon_bg = pygame.image.load(moon_bg).convert_alpha()

# NINJA SWORD
sword_lt_img = 'SWORD_LT.png'
sword_lt = pygame.image.load(sword_lt_img).convert_alpha()
sword_lt = pygame.transform.scale(sword_lt, (40, 20))

sword_rt_img = 'SWORD_RT.png'
sword_rt = pygame.image.load(sword_rt_img).convert_alpha()
sword_rt = pygame.transform.scale(sword_rt, (40, 20))

###################################################################################

# MAIN LOOP
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


    ninja.update()



    pygame.display.flip()
    clock.tick(FPS)

