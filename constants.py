SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

FPS = 60

# velocidade do game
GAME_SPEED = 4

# distância variada na vertical
GAP = 15 + GAME_SPEED

# usado para queda do pássaro
GRAVITY = 1 + GAME_SPEED * 0.1
TIME_SHOW_FIRE = 10

# ground set
GROUND_WIDHT = SCREEN_WIDTH + 1
GROUND_HEIGHT = SCREEN_HEIGHT // 6

# tree set
DISTANCE_BETWEEN_TREES = 430
# DISTANCE_BETWEEN_TREES = SCREEN_WIDTH // 3
TREE_GAP = 125
TREE_WIDTH = SCREEN_WIDTH // 15
TREE_HEIGHT = SCREEN_HEIGHT - GROUND_HEIGHT
TREE_SPACE_OFF = SCREEN_HEIGHT * 0.3
TREE_VARIATION = 70

# score set
SCORE_X = 10
SCORE_Y = SCREEN_HEIGHT * 0.93
SCORE_DISTANCE = 25

# plain set
PLAIN_X = 390