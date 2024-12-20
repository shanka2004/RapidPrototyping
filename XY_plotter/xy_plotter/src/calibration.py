# src/calibration.py (Calibration Function)
import sys
import os
import config.settings as settings
import math
# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

def calibrate_plotter(move_to_position, X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, STEPS_PER_MM_X, STEPS_PER_MM_Y):
    
    print("Starting Calibration...")
    input("Ensure the pen is at the origin (0, 0) and press Enter to continue...")
    
    # Move to a known position (e.g., 100 mm, 100 mm) and measure actual distances
    print("Moving to (100, 100)...")
    move_to_position(100, 100, settings.LIMIT_LEFT, settings.LIMIT_RIGHT, settings.LIMIT_TOP)
    actual_distance_x = float(input("Enter the actual horizontal distance moved in mm: "))
    actual_distance_y = float(input("Enter the actual vertical distance moved in mm: "))
    
    # Calculate new steps per mm for X and Y axes
    if actual_distance_x > 0:
        STEPS_PER_MM_X = (100 * STEPS_PER_MM_X) / actual_distance_x
    if actual_distance_y > 0:
        STEPS_PER_MM_Y = (100 * STEPS_PER_MM_Y) / actual_distance_y
    print(f"Calibrated STEPS_PER_MM_X: {STEPS_PER_MM_X}")
    print(f"Calibrated STEPS_PER_MM_Y: {STEPS_PER_MM_Y}")
    l1, l2 = inverse_kinematics(actual_distance_x, actual_distance_y, settings.LIMIT_LEFT, settings.LIMIT_RIGHT, settings.LIMIT_TOP)

    # Save calibrated values to settings file
    with open('config/settings.py', 'w') as settings_file:
        settings_file.write(f"STEPS_PER_MM_X = {STEPS_PER_MM_X}\n")
        settings_file.write(f"STEPS_PER_MM_Y = {STEPS_PER_MM_Y}\n")
        settings_file.write(f"current_length_motor_1 = {l1}\n")
        settings_file.write(f"current_length_motor_2 = {l2}\n")
        settings_file.write(f"LIMIT_LEFT = {settings.LIMIT_LEFT}\n")
        settings_file.write(f"LIMIT_RIGHT = {settings.LIMIT_RIGHT}\n")
        settings_file.write(f"LIMIT_TOP = {settings.LIMIT_TOP}\n")
    
    print("Calibration complete!")
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