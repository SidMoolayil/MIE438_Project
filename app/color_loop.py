import cv2
import numpy as np
import msvcrt
from multiprocessing import Process, Manager
from . import constants, commands, utils


def start(program_context, multiprocess=False):
    if multiprocess:
        num_cores = program_context['num_cores']
        program_context['multiprocess'] = True
        if num_cores > 1:
            m = Manager()
            q = m.Queue()
            program_context['q'] = q
            p = Process(target=color_loop_mp, args=(program_context, q,))
            p.start()

            commands.execution_mode(program_context, q)

            # propagate stoppage further down to the child process
            q.put_nowait('quit')
            p.join()

        else:
            print('WARNING: Your device does not have enough processors to use multiprocessing!')
            print('Switching to regular color_loop!')
            color_loop(program_context)
    else:
        color_loop(program_context)


def color_loop_mp(program_context, q):
    cam = cv2.VideoCapture(0)
    constants.FONT = cv2.FONT_HERSHEY_SIMPLEX
    q_value = ''

    while True:
        ret, img = cam.read()
        img = cv2.resize(img, (340, 220))
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for color, bounds in program_context['colors'].items():
            color_detected = detect_color(img, imgHSV, bounds)

            if color_detected:
                show_notification(color, img)

        # Blocking method of getting user input
        # if check_for_kb() == 'n':
        #     print('Thank you for visiting the automated sorted. Goodbye.')
        #     break

        if not q.empty():
            q_value = q.get_nowait()

        if q_value == 'quit':
            print('Thank you for visiting the automated sorted. Goodbye.')
            return
        elif q_value:
            handle_logic_for_child_process(q_value, program_context)

        # after we're done with q_value discard it
        q_value = ''
        cv2.imshow("cam", img)
        cv2.waitKey(constants.WAIT_KEY)


def handle_logic_for_child_process(command, program_context):
    if command in constants.CURRENT_COLORS:
        commands.toggle_color(command, program_context)
    elif command == 'color_info':
        utils.pprint_dict_keys(program_context['colors'], constants.CURRENT_COLORS)
    else:
        # if not a recognize command, just print what was shared through the queue
        print(command)


def color_loop(program_context):
    cam = cv2.VideoCapture(0)
    constants.FONT = cv2.FONT_HERSHEY_SIMPLEX

    while True:
        ret, img = cam.read()
        img = cv2.resize(img, (340, 220))
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        for color, bounds in program_context['colors'].items():
            color_detected = detect_color(img, imgHSV, bounds)

            if color_detected:
                show_notification(color, img)

        # Blocking method of getting user input
        # if check_for_kb() == 'n':
        #     print('Thank you for visiting the automated sorted. Goodbye.')
        #     break

        cv2.imshow("cam", img)
        cv2.waitKey(constants.WAIT_KEY)


def check_for_kb():
    if msvcrt.kbhit():
        kb = msvcrt.getwch()
        print(kb)
        return kb


def detect_color(img, imgHSV, bounds):
    # given a color tuple of (lowerBound, upperBound), see if it's detected and return
    # assume the image has already been resized.
    mask = cv2.inRange(imgHSV, bounds[0], bounds[1])

    kernel_open = np.ones((5, 5))
    kernel_close = np.ones((20, 20))

    mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    mask_final = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

    conts, h = cv2.findContours(mask_final.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, conts, -1, (255, 0, 0), 3)

    for i in range(len(conts)):
        x, y, w, h = cv2.boundingRect(conts[i])
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img,
                    str(i + 1),
                    (x, y + h),
                    constants.FONT,
                    4,
                    (0, 255, 255))

    return len(conts) > 0


def show_notification(color, img):
    '''

    :param color: key of the color (eg. pink, red, green, etc.)
    :param img: the image frame to be updated by this function
    :return: void
    '''
    pass

