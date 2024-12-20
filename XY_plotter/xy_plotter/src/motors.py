# src/motors.py (Motor Control Functions)
import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import time
from config.pins import X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, PEN_SERVO_PIN
import RPi.GPIO as GPIO
import config.settings as settings
import math

# Pen Control Functions
def pen_up(servo):
    servo.ChangeDutyCycle(7)  # Adjust value as needed for pen up position
    time.sleep(0.5)

def pen_down(servo):
    servo.ChangeDutyCycle(2)  # Adjust value as needed for pen down position
    time.sleep(0.5)

# Inverse Kinematics Function
# Calculate the required cable lengths for given x, y coordinates
def inverse_kinematics(x, y, limit_left, limit_right, limit_top):
    # Length from motor 1 (top left) to the pen position
    dx1 = limit_left + x
    dy1 = y
    l1 = math.sqrt(dx1**2 + dy1**2)

    # Length from motor 2 (top right) to the pen position
    dx2 = limit_right - x
    dy2 = y
    l2 = math.sqrt(dx2**2 + dy1**2)

    return l1, l2

# Motor Control Functions
# Move motors to achieve the desired x, y position using inverse kinematics
def move_to_position(x, y, limit_left, limit_right, limit_top):
    # Calculate required cable lengths
    import config.settings as settings
    l1, l2 = inverse_kinematics(x, y, limit_left, limit_right, limit_top)
    print("l1",l1)
    print("l2",l2)
    print("settings.current_length_motor_1",settings.current_length_motor_1)
    print("settings.current_length_motor_2",settings.current_length_motor_2)
    # Load calibrated steps per mm from settings
    steps_per_mm = settings.STEPS_PER_MM_Y  # Assuming Y calibration applies to both cables
    if settings.current_length_motor_1 != l1 or settings.current_length_motor_2 != l2:
        # Calculate the number of steps needed for each motor
        steps_motor_1 = int(abs(l1-settings.current_length_motor_1) * steps_per_mm)
        steps_motor_2 = int(abs(l2-settings.current_length_motor_2) * steps_per_mm)

        # Determine motor directions
        direction_motor_1 = GPIO.HIGH if l1-settings.current_length_motor_1 < 0 else GPIO.LOW
        direction_motor_2 = GPIO.LOW if l2-settings.current_length_motor_2 < 0 else GPIO.HIGH

        # Set motor directions
        GPIO.output(X_DIR_PIN, direction_motor_1)  # Motor 1 (top left)
        GPIO.output(Y_DIR_PIN, direction_motor_2)  # Motor 2 (top right)

        # Move both motors simultaneously
        for _ in range(max(steps_motor_1, steps_motor_2)):
            if _ < steps_motor_1:
                GPIO.output(X_STEP_PIN, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(X_STEP_PIN, GPIO.LOW)
                time.sleep(0.0001)
            if _ < steps_motor_2:
                GPIO.output(Y_STEP_PIN, GPIO.HIGH)
                time.sleep(0.0001)
                GPIO.output(Y_STEP_PIN, GPIO.LOW)
                time.sleep(0.0001)

    # Update current cable lengths
    print("DONE")
    print(f"STEPS_PER_MM_X = {settings.STEPS_PER_MM_X}\n")
    print(f"STEPS_PER_MM_Y = {settings.STEPS_PER_MM_Y}\n")
    print(f"current_length_motor_1 = {l1}\n")
    print(f"current_length_motor_2 = {l2}\n")
    print(f"LIMIT_LEFT = {settings.LIMIT_LEFT}\n")
    print(f"LIMIT_RIGHT = {settings.LIMIT_RIGHT}\n")
    print(f"LIMIT_TOP = {settings.LIMIT_TOP}\n")
    with open('config/settings.py', 'w') as settings_file:
        settings_file.write(f"STEPS_PER_MM_X = {settings.STEPS_PER_MM_X}\n")
        settings_file.write(f"STEPS_PER_MM_Y = {settings.STEPS_PER_MM_Y}\n")
        settings_file.write(f"current_length_motor_1 = {l1}\n")
        settings_file.write(f"current_length_motor_2 = {l2}\n")
        settings_file.write(f"LIMIT_LEFT = {settings.LIMIT_LEFT}\n")
        settings_file.write(f"LIMIT_RIGHT = {settings.LIMIT_RIGHT}\n")
        settings_file.write(f"LIMIT_TOP = {settings.LIMIT_TOP}\n")
# src/motors.py (Motor Control Functions)
# import sys
# import os
# import time
# import math
# import json
# import RPi.GPIO as GPIO

# # Add the root directory of the project to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# from config.pins import X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, PEN_SERVO_PIN
# import config.settings as settings

# # Pen Control Functions
# def pen_up(servo):
#     servo.ChangeDutyCycle(7)  # Adjust value as needed for pen up position
#     time.sleep(0.5)

# def pen_down(servo):
#     servo.ChangeDutyCycle(2)  # Adjust value as needed for pen down position
#     time.sleep(0.5)

# # Inverse Kinematics Function
# def inverse_kinematics(x, y, limit_left, limit_right, limit_top):
#     # Length from motor 1 (top left) to the pen position
#     dx1 = limit_left + x
#     dy1 = y
#     l1 = math.sqrt(dx1**2 + dy1**2)

#     # Length from motor 2 (top right) to the pen position
#     dx2 = limit_right - x
#     dy2 = y
#     l2 = math.sqrt(dx2**2 + dy1**2)

#     return l1, l2

# # Motor Control Functions
# def move_to_position(x, y, limit_left, limit_right, limit_top):
#     # Load current lengths from state.json
#     state_file_path = os.path.join('config', 'state.json')
#     if os.path.exists(state_file_path):
#         with open(state_file_path, 'r') as state_file:
#             state = json.load(state_file)
#             current_length_motor_1 = state.get("current_length_motor_1", 0)
#             current_length_motor_2 = state.get("current_length_motor_2", 0)
#     else:
#         # Initialize state if the file doesn't exist
#         current_length_motor_1 = 0
#         current_length_motor_2 = 0

#     # Calculate required cable lengths
#     l1, l2 = inverse_kinematics(x, y, limit_left, limit_right, limit_top)

#     # Load calibrated steps per mm from settings
#     steps_per_mm = settings.STEPS_PER_MM_Y  # Assuming Y calibration applies to both cables

#     if current_length_motor_1 != l1 or current_length_motor_2 != l2:
#         # Calculate the number of steps needed for each motor
#         steps_motor_1 = int(abs(l1 - current_length_motor_1) * steps_per_mm)
#         steps_motor_2 = int(abs(l2 - current_length_motor_2) * steps_per_mm)

#         # Determine motor directions
#         direction_motor_1 = GPIO.HIGH if l1 - current_length_motor_1 < 0 else GPIO.LOW
#         direction_motor_2 = GPIO.HIGH if l2 - current_length_motor_2 < 0 else GPIO.LOW

#         # Set motor directions
#         GPIO.output(X_DIR_PIN, direction_motor_1)  # Motor 1 (top left)
#         GPIO.output(Y_DIR_PIN, direction_motor_2)  # Motor 2 (top right)

#         # Move both motors simultaneously
#         for _ in range(max(steps_motor_1, steps_motor_2)):
#             if _ < steps_motor_1:
#                 GPIO.output(X_STEP_PIN, GPIO.HIGH)
#                 time.sleep(0.0001)
#                 GPIO.output(X_STEP_PIN, GPIO.LOW)
#                 time.sleep(0.0001)
#             if _ < steps_motor_2:
#                 GPIO.output(Y_STEP_PIN, GPIO.HIGH)
#                 time.sleep(0.0001)
#                 GPIO.output(Y_STEP_PIN, GPIO.LOW)
#                 time.sleep(0.0001)

#     # Update current cable lengths in state.json
#     state = {
#         "current_length_motor_1": l1,
#         "current_length_motor_2": l2
#     }
#     with open(state_file_path, 'w') as state_file:
#         json.dump(state, state_file)

#     print("DONE")
