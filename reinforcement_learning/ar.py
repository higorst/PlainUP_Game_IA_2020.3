import pygame
from pygame.locals import *
import random
from time import sleep

import numpy as np
from numpy import asarray
from numpy import save
from numpy import load

# arquivos de configuração
import constants
import address


class RL():

    def __init__(self, alpha, gamma, epsilon, episodes, init_table=False):
        super().__init__()

        self.init_table = init_table

        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        '''
            estados: distâncias possível em y da passagem
            açãos: voar / não voar
        '''
        self.q_table = self.start_q_table()

        self.last_x_dist = 0
        self.last_y_dist = 0

    def update_epsilon(self, epsilon):
        self.epsilon = epsilon

    def save_q_table(self):
        # save to npy file
        save(
            'reinforcement_learning/q_table.npy',
            asarray(self.q_table)
        )

    def start_q_table(self):
        data = asarray([])
        if not self.init_table:
            print('loading table ..')
            # load q_table
            data = load('reinforcement_learning/q_table.npy')

        else:
            print('init table ..')
            # init q_table
            data = np.zeros([2, 2], dtype=int)
        return data

    def action(self,
               #  plain pos
               x_plain, y_plain,
               #  plain dist pass
               x_dist, y_dist,
               #  pass pos
               x_pos_pass, y_pos_pass
               ):
        '''
            0 - fly
            1 - not fly
        '''
        # state = 1 # acima
        # state = 0 # abaixo

        state = 0 if y_plain > (y_pos_pass + 32) else 1

        n = random.randint(0, 100) / 100
        if y_plain < 0:
            action = 1
        elif n < self.epsilon:
            action = random.randint(0, 1)
            print("aleatório")
        else:
            action = 0 if self.q_table[state,
                                       0] >= self.q_table[state, 1] else 1
        # print("estado:",state,"action:",action,"\t",self.q_table[state,0]," ",self.q_table[state,1])
        return tuple([action, state])

    def q_learning(self,
                   #  plain pos
                   x_plain, y_plain,
                   #  plain dist pass
                   x_dist, y_dist,
                   #  pass pos
                   x_pos_pass, y_pos_pass,
                   action, last_state
                   ):

        distancia_anterior = self.last_y_dist
        distancia_atual = y_dist

        state = 0 if y_plain > (y_pos_pass + 32) else 1
        '''
            state = 1 # acima
            state = 0 # abaixo
            0 - fly
            1 - not fly

            quando voa o gap é 6
            e antes de terminar o voo se escolher n voar o gap é 3

        '''

        if distancia_atual - 6 < distancia_anterior:
            recompensa = True
        else:
            recompensa = False

        # reinforcement
        reforco = 100 if recompensa else -100

        # actual value
        old = self.q_table[state, action]

        # future state
        state_future = 0
        if action == 0 and state == 0:
            if y_plain - constants.GAP < (y_pos_pass + 32):
                state_future = 1
            else:
                state_future = 0

        elif action == 0 and state == 1:
            state_future = 1

        elif action == 1 and state == 0:
            state_future = 0

        elif action == 1 and state == 1:
            if y_plain + constants.GRAVITY >= (y_pos_pass + 32):
                state_future = 0
            else:
                state_future = 1
        # print("\n",
        #     "distancia_anterior:", distancia_anterior,"\n",
        #     "distancia_atual:", distancia_atual,"\n\n",
        #     "y_plain:",y_plain,"\n",
        #     "y_pos_pass:", y_pos_pass,"\n",
        #     "y_dist:", y_dist,"\n\n",
        #     "recompensa:", recompensa,"\n",
        #     "state_future:", state_future,"\n",
        # )

        value1 = self.q_table[state_future, 0]
        value2 = self.q_table[state_future, 1]
        max_s_t_2 = value1 if value1 >= value2 else value2

        new = old + self.alpha * (reforco + (self.gamma * max_s_t_2) - old)
        self.q_table[state, action] = new
        # self.q_table[state, action] = self.q_table[state, action] / 10

        self.last_x_dist = x_dist
        # self.last_y_dist = y_dist + ( 0 if action == 1 else constants.GAP)
        self.last_y_dist = y_dist
