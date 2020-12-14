import pygame
import random
from pygame.locals import *
from time import sleep

# arquivos de configuração
import constants
import components
import methods
import address

from reinforcement_learning import ar as rl

list_of_scores = []

def run(
        pygame, clock, screen, ground_group, plain_group, 
        RL,
        ar=False,
        episodes=0,
        episode=0,
        alpha=0,
        gamma=0,
        epsilon=0,
        init_table=False
    ):
    # -----------------------------------------------------------
    # Reinforcement Learning
    # -----------------------------------------------------------
    # RL = rl.RL(
    #     alpha=alpha, 
    #     gamma=gamma, 
    #     epsilon=epsilon, 
    #     episodes=episodes,
    #     init_table=init_table
    # )
    # RL.start_q_table()
    # RL.update_epsilon(0 if episode > 9 else 0.1 if episode > 4 else epsilon)
    RL.update_epsilon(0 if episode == episodes - 1 else (epsilon / 2) if episode > (episodes // 2) else (epsilon / 4) if episode > (episodes // 4) else (epsilon / 6) if episode > (episodes // 6) else epsilon)
    action = 10
    state = 10

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

        if game_loop:
            # ---------------------------------------------
            # RL
            x_plain, y_plain = plain.get_pos()
            x_dist, y_dist = plain.get_distx_disty_pass()
            x_pos_pass = tree_x
            y_pos_pass = tree_y

            if action != 10:
                RL.q_learning(x_plain, y_plain, x_dist, y_dist, x_pos_pass, y_pos_pass, action, state)

            if game_loop:
                action, state = RL.action(x_plain, y_plain, x_dist, y_dist, x_pos_pass, y_pos_pass)
                if action == 0:
                    plain.fly()
            # ---------------------------------------------


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
            sleep(0.4)

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
            sleep(0.4)

            return tuple([SCORE, ground_group, RL])