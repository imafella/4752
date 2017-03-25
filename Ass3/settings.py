# define some colors (R, G, B)
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
DARKGREY  = ( 40,  40,  40)
LIGHTGREY = (100, 100, 100)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
RED       = (255,   0,   0)
YELLOW    = (255, 255,   0)
PURPLE    = (255,   0, 255)
TILECOLOR = [WHITE, LIGHTGREY, YELLOW]

# display settings
FPS       = 60
TITLE     = "RL Grid World (V=Value Iterate, P=Policy Iterate, R=Reset)"
FONTNAME  = "monospace"
FONTSIZE  = 16
FONTBOLD  = True
FONTCOLOR = WHITE
BGCOLOR   = LIGHTGREY
GRIDCOLOR = DARKGREY
TILESIZE  = 64
MAPFILE   = 'rlgrid.txt'
MAXSIZE   = 3
DRAW_EXPANDED = True

# state types
STATE_WALKABLE = 0
STATE_BLOCKED  = 1
STATE_TERMINAL = 2

# legal actions that are possible from every state
# remember that these are in (row, col) format, so (1,0) is moving down by one
# with these default actions, it will iterate LEFT, UP, RIGHT, DOWN
LEGAL_ACTIONS = [(0, -1), (-1,  0), (0,  1), (1,  0)]

# RL settings
RL_GAMMA = 1.0