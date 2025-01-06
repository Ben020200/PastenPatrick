import time
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import json
import subprocess
import os
import signal

# Initialize the Adafruit Motor HATs
kit1 = MotorKit(i2c=board.I2C(), address=0x60)
kit2 = MotorKit(i2c=board.I2C(), address=0x61)

# Steps per unit
STEPS_PER_PIXEL_X = 486 / 445
STEPS_PER_PIXEL_Y = 472 / 445
STEPS_PER_DEGREE = 5

# Global variable for live feed process
live_feed_process = None

def start_live_feed():
    """
    Starts the live feed as a background process.
    """
    global live_feed_process
    try:
        command = [
            "libcamera-hello",
            "--vflip",
            "--hflip",
            "--width", "4056",
            "--height", "3040",
            "--timeout", "0"
        ]
        # Start live feed in the background
        live_feed_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
        print("Live feed started.")
    except Exception as e:
        print(f"Failed to start live feed: {e}")

def stop_live_feed():
    """
    Stops the live feed process.
    """
    global live_feed_process
    if live_feed_process:
        try:
            os.killpg(os.getpgid(live_feed_process.pid), signal.SIGTERM)  # Kill the process group
            live_feed_process = None
            print("Live feed stopped.")
        except Exception as e:
            print(f"Failed to stop live feed: {e}")

# Function to move a single stepper motor
def move_steps(stepper_motor, steps, direction):
    for _ in range(abs(steps)):
        if direction == "clockwise":
            stepper_motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        elif direction == "counterclockwise":
            stepper_motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        time.sleep(0.01)

# Function to move two motors simultaneously
def move_steps_simultaneously(motor1, motor2, steps, direction_motor1, direction_motor2):
    for _ in range(abs(steps)):
        if direction_motor1 == "clockwise":
            motor1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        elif direction_motor1 == "counterclockwise":
            motor1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)

        if direction_motor2 == "clockwise":
            motor2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
        elif direction_motor2 == "counterclockwise":
            motor2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
        time.sleep(0.01)

# Function to move to a specific position
def move_to_position(x_pixels, y_pixels, degree):
    x_steps = int(x_pixels * STEPS_PER_PIXEL_X)
    y_steps = int(y_pixels * STEPS_PER_PIXEL_Y)
    degree_steps = int(degree * STEPS_PER_DEGREE)

    if x_steps != 0:
        direction = "clockwise" if x_steps > 0 else "counterclockwise"
        print(f"Moving {x_pixels} pixels on x-axis ({direction})")
        move_steps(kit2.stepper1, x_steps, direction)

    if y_steps != 0:
        direction_motor1 = "counterclockwise" if y_steps > 0 else "clockwise"
        direction_motor2 = "counterclockwise" if y_steps > 0 else "clockwise"
        print(f"Moving {y_pixels} pixels on y-axis ({direction_motor1} for both motors)")
        move_steps_simultaneously(kit1.stepper1, kit1.stepper2, y_steps, direction_motor1, direction_motor2)

# Main function
def main():
    try:
        # Start the live feed
        start_live_feed()
        time.sleep(3)
        # Load positions and move motors
        with open("positions.json", "r") as f:
            positions = json.load(f)

        deltax = positions["deltax"]
        deltay = positions["deltay"]

        print(f"Moving to position: deltax={deltax}, deltay={deltay}")
        move_to_position(deltax, deltay, 0)

    except FileNotFoundError:
        print("positions.json not found. Run the template matching script first.")
    except KeyboardInterrupt:
        print("Operation interrupted by user.")
    finally:
        # Stop the live feed and release motors
        
        kit1.stepper1.release()
        kit1.stepper2.release()
        kit2.stepper1.release()
        time.sleep(8)
        stop_live_feed()
if __name__ == "__main__":
    main()
