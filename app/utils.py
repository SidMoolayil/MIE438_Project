'''

    Utility class for doing misc tasks

'''

import cv2
import numpy as np
from . import constants


def pprint_dict_keys(dict, compare_dict):
    '''
    Labels the keys that aren't included
    '''
    for k, v in compare_dict.items():
        if k in dict:
            print(k)
        else:
            print('%s (not included)' % k)


def pprint_setup_instructions():
    print('\n\n\n---Startup Instructions---\n'
          '\'help\': print startup instructions\n'
          '\'n\': next set of instructions\n'
          '\'p\': previous set of instructions\n\n\n')


def pprint_execution_instructions(ignore1, ignore2):
    # dummy params to fit the interface defined in mp commands
    print('\n\n\n---Execution Instructions---\n'
          '\'help\': print execution instructions\n'
          '\'color\': change to color adjustment mode to toggle colors recognized by the camera\n'
          '\'motor\': manually adjust conveyor belt motor speed\n'
          '\'n\': change to idle to select different command modes\n\n\n')


def get_pixel_color():
    cam = cv2.VideoCapture(0)

    while True:
        ret, img = cam.read()

        img = cv2.resize(img, (340, 220))

        print(img[25, 25])


def preset_avail_colors_before_startup(colors_to_keep):
    new_dict = {}

    for color in colors_to_keep:
        if color in constants.CURRENT_COLORS:
            new_dict[color] = constants.CURRENT_COLORS[color]

    return new_dict


if __name__ == '__main__':
    get_pixel_color()