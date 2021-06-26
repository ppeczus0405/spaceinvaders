# SCALING, CUSTOMIZE TO YOUR DISPLAY
GLOBAL_SCALE = 1.2 # Customize scale of all objects in game
SCALE_WINDOW = 1.0 # Customize scale of window
SCALE_OBJECTS = GLOBAL_SCALE * SCALE_WINDOW # DONT TOUCH

# FOR CUSTOMIZE
FPS = 120

# BASE DIMENSIONS, DONT TOUCH
BASE_WIDTH = 975
BASE_HEIGHT = 975

# WINDOW SIZE, DONT TOUCH
WIDTH = int(BASE_WIDTH * SCALE_WINDOW)
HEIGHT = int(BASE_HEIGHT * SCALE_WINDOW)

# PLAYER START POSITION, HP RECTANGLE, DONT TOUCH
PLAYER_START_X = int(SCALE_WINDOW * (BASE_WIDTH - (100 * GLOBAL_SCALE)) / 2)
PLAYER_START_Y = int(SCALE_WINDOW * (BASE_HEIGHT - 125 * GLOBAL_SCALE))
PLAYER_MAX_HEALTH = 100
HP_HEIGHT = int(9 * SCALE_OBJECTS)

# ENEMY_START_POSITION, DONT_TOUCH
ENEMY_START_Y = int(15 * SCALE_OBJECTS)
ENEMY_BASE_HEALTH = 1
ENEMY_BASE_SPEED = 1
ENEMY_BASE_CHANCE = 500

SPAWN_ENEMY_TRIALS = 10
SPAWN_ENEMY_CHANCE = 500

# MOVING
LASER_MOVE = int(9 * SCALE_OBJECTS)
PLAYER_MOVE = int(5 * SCALE_OBJECTS)

# CORRECTIONS
SHIP_CORRECTION = int(10 * SCALE_OBJECTS)
LASER_CORRECTION_PLAYER = int(45 * SCALE_OBJECTS)
LASER_CORRECTION_RG_X = int(-15 * SCALE_OBJECTS)
LASER_CORRECTION_RG_Y = int(2 * SCALE_OBJECTS)
LASER_CORRECTION_B_X = int(-25 * SCALE_OBJECTS)
LASER_CORRECTION_B_Y = int(12 * SCALE_OBJECTS)

# LASER
LASER_POWER = 5

# LEVELS
LEVEL_HP = 1
LEVEL_CHANCE = 20
LEVEL_SPEED = 0.04 * SCALE_OBJECTS
NEXT_LEVEL_BASE = 1.4
FIRST_LEVEL_SCORE = 3

# FONT
FONT = 'Impact'
FONT_SIZE = int(44 * SCALE_WINDOW)
FONT_X = int(775 * SCALE_WINDOW)
