import pygame   
import random
from pygame.locals import *
from time import sleep

import threading

# arquivos de configuração
import constants
import address

class Plain(pygame.sprite.Sprite, threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.isBroken = False

        self.flied = 0

        self.speed = constants.GAME_SPEED

        self.current_image = 0

        # convert_alpha === interprets the image
        self.image = pygame.image.load(
            address.PLAINS[0]
        ).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = constants.PLAIN_X
        self.rect[1] = constants.SCREEN_HEIGHT // 4 + random.randint(
            -constants.GAP,
            constants.GAP
        )
        self.dist_x = 1280 - self.rect[0] - 77
        self.dist_y = 0

        self.gap = constants.GAP

    def explosion(self):
        self.isBroken = True
        self.image = pygame.image.load(
            address.PLAINS[2]
        ).convert_alpha()

    def broken(self):
        self.image = pygame.image.load(
            address.PLAINS[3]
        ).convert_alpha()

    def set_distx_disty_pass(self, dist_x, dist_y):
        self.dist_x = dist_x
        self.dist_y = dist_y
    
    def get_distx_disty_pass(self):
        # print(self.dist_x, self.dist_y)
        return tuple([self.dist_x, self.dist_y])

    def update(self):
        if self.flied == 0 and not self.isBroken:
            self.image = pygame.image.load(
                address.PLAINS[0]
            ).convert_alpha()
        else:
            self.flied -= 1

        self.speed += constants.GRAVITY

        # update height
        self.rect[1] += self.speed // 3
    
    def fly(self):
        self.image = pygame.image.load(
            address.PLAINS[1]
        ).convert_alpha()
        self.flied = constants.TIME_SHOW_FIRE
        self.speed = -self.gap

    def updateGAP(self, gap):
        self.gap = gap

    def get_pos(self):
        return tuple([(self.rect[0] + 73), self.rect[1] + 22])

class Tree(pygame.sprite.Sprite, threading.Thread):

    def __init__(self, inverted, xpos, ysize, up_down, ypos):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.move = up_down
        self.down = constants.TREE_VARIATION
        self.up = 0
        self.passed = False

        self.image = pygame.image.load(
            address.TREES[random.randint(0, 7)]
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, 
            (
                constants.TREE_WIDTH, 
                constants.TREE_HEIGHT)
            )

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = constants.SCREEN_HEIGHT - ysize

        self.x_pos_pass = xpos
        self.y_pos_pass = ypos
        

        self.mask = pygame.mask.from_surface(self.image)

    def update_passed(self):
        self.passed = True

    def get_pos(self):
        return tuple([self.x_pos_pass, self.y_pos_pass])

    def get_passed(self):
        return self.passed

    def update(self):
        self.rect[0] -= constants.GAME_SPEED
        self.x_pos_pass -= constants.GAME_SPEED
        # up/down
        if self.move:
            if self.down > 0:
                self.rect[1] += 1
                self.up += 1
                self.down -= 1

                self.y_pos_pass += 1

            elif self.up > 0: 
                self.rect[1] -= 1
                self.up -= 1

                self.y_pos_pass -= 1
                
            else:
                self.down = constants.TREE_VARIATION

class Score(pygame.sprite.Sprite, threading.Thread):

    def __init__(self, number_score, pos):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.current_image = number_score

        self.image = pygame.image.load(
            address.NUMBERS[self.current_image]
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect[0] = 260 - (constants.SCORE_DISTANCE * 3) + (pos * constants.SCORE_DISTANCE)
        self.rect[1] = constants.SCORE_Y

    def update(self):
        self.image = self.image = pygame.image.load(
            address.NUMBERS[self.current_image]
        ).convert_alpha()

class Ground(pygame.sprite.Sprite, threading.Thread):

    def __init__(self, xpos):
        threading.Thread.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(
            address.GROUND[random.randint(0, 7)]
        ).convert_alpha()
        self.image = pygame.transform.scale(
            self.image, 
            (
                constants.GROUND_WIDHT, 
                constants.GROUND_HEIGHT
            )
        )

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()

        self.rect[0] = xpos
        self.rect[1] = constants.SCREEN_HEIGHT - constants.GROUND_HEIGHT

    def update(self):
        self.rect[0] -= constants.GAME_SPEED
