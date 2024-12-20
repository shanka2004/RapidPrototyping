# src/gcode.py (G-code Execution)
import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import time
from config.pins import X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, PEN_SERVO_PIN
import RPi.GPIO as GPIO
import config.settings as settings
import math

def execute_gcode(file_path, move_to_position, pen_up, pen_down):
    current_x, current_y = 0, 0

    with open(file_path, 'r') as gcode_file:
        for line in gcode_file:
            if line.startswith('G0') or line.startswith('G1'):  # Linear movement
                parts = line.split()
                x, y = None, None

                for part in parts:
                    if part.startswith('X'):
                        x = float(part[1:])
                    elif part.startswith('Y'):
                        y = float(part[1:])

                if x is not None or y is not None:
                    target_x = x if x is not None else current_x
                    target_y = y if y is not None else current_y

                    # Move motors to target position
                    move_to_position(target_x, target_y, settings.LIMIT_LEFT, settings.LIMIT_RIGHT, settings.LIMIT_TOP)

                    # Update current position
                    current_x, current_y = target_x, target_y

            elif line.startswith('G0 Z') or line.startswith('G1 Z'):  # Pen control
                if 'Z' in line:
                    z_height = float(line.split('Z')[-1])
                    if z_height > 0:  # Pen up
                        pen_up()
                    else:  # Pen down
                        pen_down()
