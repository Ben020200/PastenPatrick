import time
import threading
import board
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import keyboard  # To detect key presses

# Initialize the Adafruit Motor HATs
kit1 = MotorKit(i2c=board.I2C(), address=0x60)  # Default address
kit2 = MotorKit(i2c=board.I2C(), address=0x61)  # Second HAT with address 0x61

# Global variables to track motor state
motor1_state = None
motor2_state = None
motor3_state = None
mode = "fast"  # Start in fast mode
running = True

# Function to move stepper motor continuously with adjustable speed
def motor_control_thread(stepper_motor, state_var, speed):
    global mode
    while running:
        if state_var[0] == "clockwise":
            step_type = stepper.SINGLE if mode == "fast" else stepper.MICROSTEP
            stepper_motor.onestep(direction=stepper.FORWARD, style=step_type)
            time.sleep(max(0.005, 0.02 * (1 - speed)))  # Smooth delays for microstepping
        elif state_var[0] == "counterclockwise":
            step_type = stepper.SINGLE if mode == "fast" else stepper.MICROSTEP
            stepper_motor.onestep(direction=stepper.BACKWARD, style=step_type)
            time.sleep(max(0.005, 0.02 * (1 - speed)))  # Smooth delays for microstepping
        else:
            # Release motor coils when idle to prevent noise
            stepper_motor.release()
            time.sleep(0.1)  # Small delay to avoid busy-waiting

# Thread function to monitor keyboard input
def keyboard_monitor_thread():
    global motor1_state, motor2_state, motor3_state, mode, running

    while running:
        # Handle up/down keys for motor1 and motor2
        if keyboard.is_pressed('down'):
            motor1_state[0] = "clockwise"
            motor2_state[0] = "clockwise"
        elif keyboard.is_pressed('up'):
            motor1_state[0] = "counterclockwise"
            motor2_state[0] = "counterclockwise"
        else:
            motor1_state[0] = None
            motor2_state[0] = None

        # Independent handling of r/l keys for motor2
        if keyboard.is_pressed('r'):
            motor2_state[0] = "clockwise"
            motor1_state[0] = "counterclockwise"
        elif keyboard.is_pressed('l'):
            motor1_state[0] = "clockwise"
            motor2_state[0] = "counterclockwise"

        # Handle left/right keys for motor3
        if keyboard.is_pressed('left'):
            motor3_state[0] = "clockwise"
        elif keyboard.is_pressed('right'):
            motor3_state[0] = "counterclockwise"
        else:
            motor3_state[0] = None

        # Switch between slow (s) and fast (f) mode
        if keyboard.is_pressed('s'):
            mode = "slow"
            print("Switched to SLOW mode (MICROSTEP).")
            time.sleep(0.2)  # Debounce
        elif keyboard.is_pressed('f'):
            mode = "fast"
            print("Switched to FAST mode (SINGLE step).")
            time.sleep(0.2)  # Debounce

        # Stop the program if 'q' is pressed
        if keyboard.is_pressed('q'):
            running = False

        time.sleep(0.05)  # Faster response to inputs

# Main function to start threads and control motors
def main():
    global motor1_state, motor2_state, motor3_state, running

    # Initialize motor states
    motor1_state = [None]
    motor2_state = [None]
    motor3_state = [None]

    # Set the initial speed (pseudo duty cycle)
    motor1_speed = 1  # 100% duty cycle
    motor2_speed = 1  # 100% duty cycle
    motor3_speed = 1  # 100% duty cycle

    # Create threads for motor control and keyboard monitoring
    motor1_thread = threading.Thread(target=motor_control_thread, args=(kit1.stepper1, motor1_state, motor1_speed))
    motor2_thread = threading.Thread(target=motor_control_thread, args=(kit1.stepper2, motor2_state, motor2_speed))
    motor3_thread = threading.Thread(target=motor_control_thread, args=(kit2.stepper1, motor3_state, motor3_speed))
    keyboard_thread = threading.Thread(target=keyboard_monitor_thread)

    motor1_thread.start()
    motor2_thread.start()
    motor3_thread.start()
    keyboard_thread.start()

    try:
        motor1_thread.join()
        motor2_thread.join()
        motor3_thread.join()
        keyboard_thread.join()
    except KeyboardInterrupt:
        running = False

    # Release motors when done
    kit1.stepper1.release()
    kit1.stepper2.release()
    kit2.stepper1.release()

if __name__ == "__main__":
    main()
