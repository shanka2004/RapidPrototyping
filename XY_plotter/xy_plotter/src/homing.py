# src/homing.py (Homing Function)
import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import time
from config.pins import X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN, PEN_SERVO_PIN
import RPi.GPIO as GPIO
import config.settings as settings
import math

def home_plotter(X_STEP_PIN, X_DIR_PIN, X_LIMIT_SWITCH_PIN, Y_STEP_PIN, Y_DIR_PIN, Y_LIMIT_SWITCH_PIN):
    print("Homing the plotter...")
    
    # Home X-axis
    GPIO.output(X_DIR_PIN, GPIO.LOW)  # Set direction towards limit switch
    ##############
    while GPIO.input(X_LIMIT_SWITCH_PIN):  # Move until limit switch is pressed
        GPIO.output(X_STEP_PIN, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(X_STEP_PIN, GPIO.LOW)
        time.sleep(0.001)
    print("X-axis homed.")
    
    # Home Y-axis
    GPIO.output(Y_DIR_PIN, GPIO.LOW)  # Set direction towards limit switch
    while GPIO.input(Y_LIMIT_SWITCH_PIN):  # Move until limit switch is pressed
        GPIO.output(Y_STEP_PIN, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(Y_STEP_PIN, GPIO.LOW)
        time.sleep(0.001)
    print("Y-axis homed.")
    ###############
    
    
    # Set current motor lengths to home position
    settings.current_length_motor_1 = settings.LIMIT_TOP
    settings.current_length_motor_2 = settings.LIMIT_TOP
    
    print("Homing complete!")
