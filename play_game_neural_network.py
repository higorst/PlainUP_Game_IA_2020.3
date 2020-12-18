import pygame
import random
from pygame.locals import *
from time import sleep

from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
# arquivos de configuração
import constants
import components
import methods
import address

NUM_AGENTES = 5

NUM_EPISODES = 100
ALPHA = 0.125
GAMMA = 0.9
E_GREEDY = 0.15

list_of_scores = []

def run(pygame, clock, screen, ground_group, plain_group):
    
    # -----------------------------------------------------------
    # Configurações iniciais
    # -----------------------------------------------------------

    # game background image
    BACKGROUND = pygame.image.load(address.BACKGROUND)
    BACKGROUND = pygame.transform.scale(
        BACKGROUND,
        constants.SCREEN_SIZE
    )

    SCORE = 0

    # plain group
    plain_group = plain_group
    plain = plain_group.sprites()[0]
    # plain_group = pygame.sprite.Group()
    # plain = components.Plain()
    # plain_group.add(plain)

    # tree group
    tree_group = pygame.sprite.Group()
    tree, tree_inverted = methods.get_random_trees(
        constants.SCREEN_WIDTH
    )
    LAST_TREE = tree
    tree_group.add(tree)
    tree_group.add(tree_inverted)

    # score group
    score_group = pygame.sprite.Group()
    score = components.Score(0, 0)
    score_group.add(score)

    # -----------------------------------------------------------

    # game loop
    game_loop = True
    while game_loop:
        
        action_up = 0;
        clock.tick(constants.FPS)

        screen.fill((0, 0, 0))
        # setting the game's background image
        screen.blit(BACKGROUND, (0, 0))

        # clean score
        for x in score_group:
            score_group.remove(x)

        tree = tree_group.sprites()[0]
        agent = plain

        SCORE += methods.get_score(tree)

        # verificar distância do agente para a passagem
        dist_x, dist_y, tree_x, tree_y = methods.dist_agent(tree_group, agent)
        # print(dist_y, tree_y)
        rn = NetworkReader.readFrom('model_training.xml') 

        value_action = rn.activate((dist_x, dist_y, tree_x, tree_y))[0]

        plain.set_distx_disty_pass(dist_x, dist_y)

        # -----------------------------------
        # show components
        # -----------------------------------
        FIRST_TREE = tree_group.sprites()[0]

        # show plain
        plain_group.update()
        plain_group.draw(screen)

        # add new tree
        tree_group, LAST_TREE = methods.i_have_to_create_another_one(tree_group, LAST_TREE)        
        # remove tree group
        tree_group = methods.i_have_to_destroy_tree(tree_group)        
        # remove ground group
        ground_group = methods.i_have_to_destroy_ground(ground_group) 
        # set show score
        score_group = methods.set_score(score_group, SCORE)

        # show tree
        tree_group.update()
        tree_group.draw(screen)
        # show ground
        ground_group.update()
        ground_group.draw(screen)

        # show score
        score_group.update()
        score_group.draw(screen)
        # -----------------------------------

        # screen update
        pygame.display.update()

        # verificar colisão
        game_loop = methods.collided(plain_group, tree_group, ground_group)

        if (float(value_action) > 0.173):
            plain.fly()
        # change events // user interaction
        for event in pygame.event.get():
            # game close event
            if event.type == QUIT:
                # pygame.quit()
                game_loop = False
            

            if event.type == KEYDOWN:
               
                if event.key == K_ESCAPE:
                        game_loop = False
        
        if not game_loop:
            plain.explosion()
            screen.fill((0, 0, 0))
            # setting the game's background image
            screen.blit(BACKGROUND, (0, 0))
            # show tree
            tree_group.update()
            tree_group.draw(screen)
            # show ground
            ground_group.update()
            ground_group.draw(screen)

            # show score
            score_group.update()
            score_group.draw(screen)
            # show plain
            plain_group.update()
            plain_group.draw(screen)
            # screen update
            pygame.display.update()
            sleep(0.5)

            plain.broken()
            screen.fill((0, 0, 0))
            # setting the game's background image
            screen.blit(BACKGROUND, (0, 0))
            # show tree
            tree_group.draw(screen)
            # show ground
            ground_group.draw(screen)

            # show score
            score_group.update()
            score_group.draw(screen)
            # show plain
            plain_group.draw(screen)
            # screen update
            pygame.display.update()
            sleep(1)
                
            return tuple([SCORE, ground_group])






