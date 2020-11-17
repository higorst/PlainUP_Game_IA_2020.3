import pygame
import random
from pygame.locals import *
from time import sleep

# arquivos de configuração
import constants
import components

# -----------------------------------------------------------------
# trees
# -----------------------------------------------------------------


def get_random_trees(xpos):
    up_down = random.randint(False, True)
    size = random.randint(
        131 * 2,
        constants.SCREEN_HEIGHT - 131
    )
    # size = constants.SCREEN_HEIGHT // 2
    # up_down = False

    ypos = constants.SCREEN_HEIGHT - size - (constants.TREE_GAP // 2)

    tree = components.Tree(
        False,
        xpos,
        size,
        up_down,
        ypos
    )
    tree_inverted = components.Tree(
        True,
        xpos,
        constants.SCREEN_HEIGHT - size - constants.TREE_GAP,
        up_down,
        ypos
    )

    return (tree, tree_inverted)


def i_have_to_create_another_one(tree_group, LAST_TREE):
    if LAST_TREE.rect[0] <= (constants.SCREEN_WIDTH - constants.DISTANCE_BETWEEN_TREES):
        tree, tree_inverted = get_random_trees(
            constants.SCREEN_WIDTH
        )
        LAST_TREE = tree
        tree_group.add(tree)
        tree_group.add(tree_inverted)
    return tuple([tree_group, LAST_TREE])


def i_have_to_destroy_tree(tree_group):
    tree = tree_group.sprites()[0]
    if tree.rect[0] < -constants.TREE_WIDTH:
        # remove tree
        tree_group.remove(tree_group.sprites()[0])
        # remove tree_inverted
        tree_group.remove(tree_group.sprites()[0])
    return tree_group

# -----------------------------------------------------------------
# score
# -----------------------------------------------------------------

def set_score(score_group, SCORE):
    for pos_number in range(0, len(str(SCORE))):
        score_group.add(
            components.Score(
                int(str(SCORE)[pos_number]), 
                pos_number
            )
        )
    return score_group

def get_score(tree):
    if (tree.rect[0] + constants.TREE_WIDTH) < constants.PLAIN_X and tree.get_passed() == False:
        tree.update_passed()
        return 1
    else:
        return 0


def i_have_to_destroy_ground(ground_group):
    ground = ground_group.sprites()[0]
    if ground.rect[0] <= -constants.GROUND_WIDHT:
        # remove ground
        ground_group.remove(ground_group.sprites()[0])
        # add a new ground
        ground = components.Ground(constants.SCREEN_WIDTH)
        ground_group.add(ground)
    return ground_group


def get_create_ground(ground):
    if ground.rect[0] <= 0:
        return True

# -----------------------------------------------------------------
# others
# -----------------------------------------------------------------

def dist_agent(tree, agent):
    i = 0
    while tree.sprites()[i].get_passed():
        i += 2
    tree = tree.sprites()[i]
    agent_x, agent_y = agent.get_pos()

    tree_x, tree_y = tree.get_pos()

    dist_x = tree_x - agent_x
    dist_y = agent_y - tree_y
    dist_y = dist_y if dist_y >= 0 else dist_y*(-1)

    return tuple([dist_x, dist_y, tree_x, tree_y])

def collided(plain_group, tree_group, ground_group):
    if (pygame.sprite.groupcollide(
        plain_group,
        ground_group,
        False,
        False,
        pygame.sprite.collide_mask
    ) or
        pygame.sprite.groupcollide(
        plain_group,
        tree_group,
        False,
        False,
        pygame.sprite.collide_mask
    )):
        return False
    return True
