import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from config.pins import *
from motors import pen_up, pen_down, move_to_position
from calibration import calibrate_plotter
from homing import home_plotter
from gcode import execute_gcode
import RPi.GPIO as GPIO
import time
import os
import config.settings as settings

# PWM for Servo
servo = GPIO.PWM(PEN_SERVO_PIN, 50)  # 50 Hz
servo.start(0)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="XY Plotter Control")
    parser.add_argument('--calibrate', action='store_true', help="Calibrate the plotter")
    parser.add_argument('--home', action='store_true', help="Home the plotter")
    parser.add_argument('--gcode', type=str, help="Path to G-code file to execute")

    args = parser.parse_args()

    if args.calibrate:
        calibrate_plotter(move_to_position, X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, settings.STEPS_PER_MM_X, settings.STEPS_PER_MM_Y)
    elif args.home:
        home_plotter(X_STEP_PIN, X_DIR_PIN, X_LIMIT_SWITCH_PIN, Y_STEP_PIN, Y_DIR_PIN, Y_LIMIT_SWITCH_PIN)
    elif args.gcode:
        pen_up(servo)  # Start with pen up
        # home_plotter(X_STEP_PIN, X_DIR_PIN, X_LIMIT_SWITCH_PIN, Y_STEP_PIN, Y_DIR_PIN, Y_LIMIT_SWITCH_PIN)  # Home the plotter
        execute_gcode(args.gcode, move_to_position, lambda: pen_up(servo), lambda: pen_down(servo))
    else:
        print("No valid arguments provided. Use --help for options.")

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
        servo.stop()
