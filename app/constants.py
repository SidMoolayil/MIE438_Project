import numpy as np
import cv2

IS_WINDOWS = False
IS_MAC = False
IS_LINUX = False

# below dict of the form <color>: (lowerBound, upperBound)
# bounds were tested via trial & error
CURRENT_COLORS = {
    'red': (np.array([0, 75, 75]), np.array([0, 100, 100])),
    'green': (np.array([40, 50, 50]), np.array([50, 255, 255])),
    'blue': (np.array([]), np.array([])),
    'yellow': (np.array([23, 50, 50]), np.array([33, 255, 255])),
    'black': (np.array([0, 0, 0]), np.array([200, 80, 80])),
    'pink': (np.array([155, 50, 50]), np.array([180, 255, 255])),
    'orange': (np.array([10, 50, 50]), np.array([20, 255, 255]))
}

FONT = cv2.FONT_HERSHEY_SIMPLEX

# time (in ms) that openCV holds the frame for display
WAIT_KEY = 1

# default program context
DEFAULT_CONTEXT = {
        'clock_speed_factor': 1,
        'num_cores': 1,
        'colors': CURRENT_COLORS.copy(),
        'instruction_number': 0,
        'multiprocess': False,
        'q': None
    }