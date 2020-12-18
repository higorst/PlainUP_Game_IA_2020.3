import pygame
import random
from pygame.locals import *
from time import sleep

# game run
import play_game_ar as game

# arquivos de configuração
import constants
import components
import methods
import address

from numpy import asarray
from numpy import save
from numpy import load

import matplotlib.pyplot as plt

# -----------------------------------------------------------
# RL MODULE
from reinforcement_learning import ar as rl

print("\n\n\tReinforcement Learning (RL)\n")
# episodes =   int(input("[PARAM] Episodes:        "))
# alpha    = float(input("[PARAM] Learning Rate:   "))
# gamma    = float(input("[PARAM] Discount Factor: "))
# epsilon  = float(input("[PARAM] E-greedy:        "))
episodes   = 10
alpha      = 0.125
gamma      = 0.125
epsilon    = 0.03
# ----------------
init_table = True
results    = []
run_ar     = True
print()
RL = rl.RL(
        alpha=alpha, 
        gamma=gamma, 
        epsilon=epsilon, 
        episodes=episodes,
        init_table=init_table
    )
# -----------------------------------------------------------

# -----------------------------------------------------------
# Configurações iniciais
# -----------------------------------------------------------

# start game
pygame.init()
screen = pygame.display.set_mode(constants.SCREEN_SIZE)

# game background image
BACKGROUND = pygame.image.load(address.BACKGROUND)
BACKGROUND = pygame.transform.scale(
    BACKGROUND,
    constants.SCREEN_SIZE
)
MENU_SHOW = pygame.image.load(address.MENU_SHOW)
MENU_SHOW = pygame.transform.scale(
    MENU_SHOW,
    (580, 176)
)
BEST_SCORE = pygame.image.load(address.BEST_SCORE)
BEST_SCORE = pygame.transform.scale(
    BEST_SCORE,
    (161, 44)
)

# limit game frames
clock = pygame.time.Clock()

# -------------------------------
# ground group
ground_group = pygame.sprite.Group()
ground = components.Ground(0)
ground_group.add(ground)
ground = components.Ground(constants.SCREEN_WIDTH)
ground_group.add(ground)
ground = components.Ground(constants.SCREEN_WIDTH * 2)
ground_group.add(ground)

# plain group
plain_group = pygame.sprite.Group()
plain = components.Plain()
plain_group.add(plain)

# score group
score_group = pygame.sprite.Group()
# ler score gravado (best)
file_score = open('assets/score.txt', 'r')
SCORE = file_score.read()
file_score.close()
# set score
score_group = methods.set_score(score_group, SCORE)
# -------------------------------

# game loop
menu_loop = True
# while menu_loop:
for episode in range(episodes):
    # clock.tick(constants.FPS)
    print("\n\tepisode", episode + 1)

    screen.fill((0, 0, 0))
    # setting the game's background image
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(MENU_SHOW, (constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT // 20))

    # remove ground group
    ground_group = methods.i_have_to_destroy_ground(ground_group)        

    # show ground
    ground_group.update()
    ground_group.draw(screen)

    # best score
    score_group.update()
    score_group.draw(screen)

    # show plain
    # plain_group.update() -- do not update [static position]
    plain_group.draw(screen)

    # screen update
    screen.blit(BEST_SCORE, (10, constants.SCREEN_HEIGHT * 0.92))
    pygame.display.update()

    # chamada do método fly para o pássaro
    score, ground_group, RL = game.run(
        pygame=pygame, 
        clock=clock, 
        screen=screen,
        ground_group=ground_group,
        plain_group=plain_group,
        RL=RL,
        ar=True,
        episodes=episodes,
        episode=episode,
        alpha=alpha,
        gamma=gamma,
        epsilon=epsilon,
        init_table=init_table,
    )
    print("SCORE:",score)
    # ----------------------------------
    # ----------- AR - guardar resultados
    results.append([episode, score])
    # ----------------------------------
    # remove old plain and add a new
    plain_group = pygame.sprite.Group()
    plain = components.Plain()
    plain_group.add(plain)
    if int(SCORE) < int(score):
        SCORE = score
        score_group.empty()
        # set score
        score_group = methods.set_score(score_group, SCORE)
        file_score = open('assets/score.txt', 'w')
        file_score.write(str(score))
        file_score.close()
pygame.quit()

print(results)
results = asarray(results)
# save to npy file
save(
    'reinforcement_learning/results.npy', 
    results
)  

graph_x_1 = []
graph_y_1 = []
for index in range(episodes):
    graph_x_1.append(results[index][0])
    graph_y_1.append(results[index][1])

plt.plot(graph_x_1, graph_y_1, 'go-', label='Distância Alcançada ao Longo dos episódios', linewidth=1, linestyle='dashed', marker='X', markersize=10)
plt.show()
# input("\n[ENTER] to exit\n")