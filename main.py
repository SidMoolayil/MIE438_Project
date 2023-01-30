'''

Main starting script for our project.

Steps:
    1) Startup script where we receive user input from command line
    2) Main control loop

'''

from app import commands, color_test, constants, utils, color_loop

if __name__ == '__main__':
    available_colors = utils.preset_avail_colors_before_startup(['pink', 'green', 'yellow', 'orange'])
    program_context = commands.startup(available_colors)
    color_loop.start(program_context, multiprocess=True)
