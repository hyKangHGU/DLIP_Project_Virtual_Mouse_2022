import autopy as ap

# Size of Camera and Monitor Screen
wCam, hCam = 640, 360
# wCam, hCam = 1280, 720
W_SCR, H_SCR = ap.screen.size()

# Color
BLUE  = ( 255,   0,   0)
GREEN = (   0, 255,   0)
RED   = (   0,   0, 255)
PINK  = ( 255,   0, 255)

# Mode Definition
NO_MODE             = 0
MOUSE_MOVE          = 1
MOUSE_L_CLICK_WAIT  = 2
MOUSE_L_CLICKING    = 3
MOUSE_R_CLICK_WAIT  = 4
MOUSE_R_CLICKING    = 5
MOUSE_DRAG_DOWN     = 6
MOUSE_DRAG_UP       = 7
SCROLL_WAIT         = 8
SCROLL_MOVE         = 9
MIDDLE_FINGER_UP    = 10

# Minimum distance of finger landmarks (using in click functions)
MIN_NUM56_DISTANCE  = 0.20
MIN_NUM58_DISTANCE  = 0.37

# Minimum value 
MIN_CHNAGE_DISTANCE = 4     # [pixel]
MIN_CNT_SCROLL      = 3     # [frame]

# Mouse cursor moving velocity
smoothening_x = 0.6                     # low value -> high speed
smoothening_y = smoothening_x / 1.5

# ======== Initialization ========== #
pTime = 0
plocX, plocY = ap.mouse.location()
clocX, clocY = 0, 0
pconX, pconY = 0, 0
fingers_prev = False

pMode = NO_MODE
cMode = NO_MODE
cnt_scroll = 0