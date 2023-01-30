'''

    Runs initial startup loop where we receive user input.

    This file is to make testing across processors of different specs easier.
    (Eg. we can adjust variables dependent on clock speeds, memory, etc.)

    Poll for the following quantities:
        <string> colors - input toggles whether or not we detect a color
        <int> clock_speed_factor - the clock speed constant of the current device, relative to the PI 3+
        <int> num_cores - sets upper bound for number of processes we use in multiprocessing

    Credits to this SO answer:
    https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal/43065186

'''

from . import utils, constants
import platform

instruction_number = 0


def startup(current_colors):
    # detect os for any platform-dependent usage
    detect_os(platform.system())

    # start text
    print('\n\n\n ********** Welcome to the Automated Sorter! **********')
    utils.pprint_setup_instructions()

    # initialize default context
    program_context = constants.DEFAULT_CONTEXT
    program_context['colors'] = current_colors

    startup_instructions = {
        0: ask_colors,
        1: ask_clock_speed,
        2: ask_cores
    }

    while program_context['instruction_number'] <= 2:
        startup_instructions[program_context['instruction_number']](program_context)

    print(str(program_context))
    return program_context


def execution_mode(program_context, q=None):
    print('\n\n\n ********** Adjust things while the camera is running! **********')
    utils.pprint_execution_instructions('', '')
    print('Current program context: ')
    print(program_context)

    execution_instructions = {
        'help': utils.pprint_execution_instructions,
        'color': ask_colors_mp,
        'motor': ask_motor_mp
    }

    user_input = input('\n\n\nDo stuff while the camera is running: \n')
    while user_input != 'quit':
        if user_input in execution_instructions:
            execution_instructions[user_input](program_context, q)
            user_input = input('\n\n\nDo stuff while the camera is running: \n')
        else:
            print('WARNING: Command %s not found!' % user_input)
            user_input = input('\n\n\nDo stuff while the camera is running: \n')


def ask_motor_mp(program_context, q):
    q.put('WARNING: Motor code unimplented so far!!')


def ask_colors(program_context):
    print('\n\n\n***Currently detecting the following colors: ')
    utils.pprint_dict_keys(program_context['colors'], constants.CURRENT_COLORS)
    print('Select which colors to detect (less colors means faster performance)')
    print('Type the color name to toggle inclusion/exclusion. (n if satisfied)')
    input_string = input('Enter info now: ')
    is_common = check_for_common_instructions(input_string, program_context)

    if is_common:
        return

    toggle_color(input_string, program_context)


# Mostly asynchronous, but some blocking for when we need to switch back to main process for input
def ask_colors_mp(program_context, q):
    print('\n\n\n***Currently detecting the following colors: ')

    # makes sense to use queue instead of instantly printing because we are not guaranteed
    # that color_info prints before the rest of our statements.
    q.put('color_info')
    q.put('Select which colors to detect (less colors means faster performance)')
    q.put('Type the color name to toggle inclusion/exclusion. (n if satisfied)')

    while not q.empty():
        # cannot also pass input to queue, since only parent processes can use stdin
        pass

    input_string = input('Enter info now: ')
    is_common = check_for_common_instructions(input_string, program_context)

    if is_common:
        return

    # if not none (python implictly does this)
    if q:
        # cannot toggle this program_context, as this belongs to main process.
        # instead, send input string over queue (since it's a simple data type) and
        # manually do it on the color side.
        q.put_nowait(input_string)
    else:
        toggle_color(input_string, program_context)


def toggle_color(input_string, program_context):
    if input_string not in constants.CURRENT_COLORS:
        print('.....Unknown color.....\n')
        return
    else:
        if input_string in program_context['colors']:
            del program_context['colors'][input_string]
        else:
            program_context['colors'][input_string] = constants.CURRENT_COLORS[input_string]


def ask_clock_speed(program_context):
    print('\n\n\n***Current specified clock speed factor: %d' % program_context['clock_speed_factor'])
    print('Enter new clock speed? (n if satisfied)')
    input_string = input('Enter info now: ')
    is_common = check_for_common_instructions(input_string, program_context)

    if is_common:
        return

    try:
        program_context['clock_speed_factor'] = int(input_string)
    except ValueError:
        print('ERROR: Please enter a number for clock speed factor!')


def ask_cores(program_context):
    print('\n\n\n***Current specified number of cores: %d' % program_context['num_cores'])
    print('Enter new number of cores? (n if satisfied)')
    input_string = input('Enter info now: ')
    is_common = check_for_common_instructions(input_string, program_context)

    if is_common:
        return

    try:
        program_context['num_cores'] = int(input_string)
    except ValueError:
        print('ERROR: Please enter a number for number of cores!')


def check_for_common_instructions(user_input, program_context):

    # might be sloppy to do it this way? Not sure what the standard is
    global instruction_number
    if user_input == 'n':
        program_context['instruction_number'] += 1
        return True
    elif user_input == 'p' and instruction_number > 0:
        program_context['instruction_number'] -= 1
        return True
    elif user_input == 'help':
        utils.pprint_setup_instructions()
        return True

    return False


def detect_os(name):
    '''
    Figure out which OS we're using and flips the corresponding constant. Currently supports windows, linux, mac.
    :return: os string
    '''

    if name == 'Windows':
        constants.IS_WINDOWS = True
    elif name == 'Linux':
        constants.IS_LINUX = True
    elif name == 'Darwin':
        constants.IS_MAC = True
    else:
        # TODO: should probably raise a custom exception.
        raise Exception('Unsupported operating system')

    return name
