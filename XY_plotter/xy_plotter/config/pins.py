# src/pins.py (Pin Configuration File)
import RPi.GPIO as GPIO

# GPIO Pin Configuration for Motors and Servo
X_STEP_PIN = 17
X_DIR_PIN = 27
X_LIMIT_SWITCH_PIN = 5  # Limit switch for X-axis home position
Y_STEP_PIN = 10
Y_DIR_PIN = 9
Y_LIMIT_SWITCH_PIN = 6  # Limit switch for Y-axis home position
PEN_SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([X_STEP_PIN, X_DIR_PIN, Y_STEP_PIN, Y_DIR_PIN], GPIO.OUT)
GPIO.setup(PEN_SERVO_PIN, GPIO.OUT)
GPIO.setup([X_LIMIT_SWITCH_PIN, Y_LIMIT_SWITCH_PIN], GPIO.IN, pull_up_down=GPIO.PUD_UP)
