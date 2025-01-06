import subprocess
import os
import signal
import psutil  # For process management
import tkinter as tk
import tkinter.messagebox as messagebox

# Global variables
process = None  # For the live feed process
zoom_level = 1.0  # Initial zoom level (1.0 means no zoom)
root = None  # Global variable for the Tkinter window



MOTOR_PROGRAM_PATH = "/home/pi/Desktop/Platinenprojekt/motor_test.py"  # Path to motor_test.py

def start_program(program_command):
    """
    Executes the given command or script with proper handling of arguments.
    Supports both direct script names and full commands.
    """
    try:
        # If the command starts with "sudo", split it into parts
        if program_command.startswith("sudo"):
            command_list = program_command.split()
        else:
            # Otherwise, resolve the virtual environment python path
            python_executable = os.path.join(os.environ.get("VIRTUAL_ENV", ""), "bin", "python3")
            if not os.path.exists(python_executable):
                python_executable = "python3"  # Default to system Python if VENV is not found

            # Combine python interpreter with the script
            command_list = [python_executable, program_command]
        
        # Run the command in a new subprocess
        subprocess.Popen(command_list)
    except Exception as e:
        messagebox.showerror("Error", f"The program '{program_command}' could not be started.\n{e}")


def start_live_feed():
    """
    Starts the live feed using libcamera-hello.
    """
    global process, zoom_level
    try:
        # Command to start live feed with libcamera
        command = [
            "libcamera-hello",
            "--vflip",
            "--hflip",
            "--width", "4056",
            "--height", "3040",
            "--timeout", "0",
            "--roi", f"{(1-zoom_level)/2},{(1-zoom_level)/2},{zoom_level},{zoom_level}"
        ]

        # Stop any running process before starting a new one
        stop_live_feed()

        print("Appa is flying... Press 'Stop' to land him.")
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(command, stdout=devnull, stderr=devnull, preexec_fn=os.setsid)

    except Exception as e:
        print(f"Error starting live feed: {e}")

def stop_motor_program():
    """
    Stops the motor_test.py program if it is running.
    """
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            # Check if the exact path to motor_test.py is in the process's command line
            if MOTOR_PROGRAM_PATH in proc.info['cmdline']:
                print(f"Stopping motor_test.py: PID {proc.info['pid']}")
                proc.terminate()  # Terminate the process
                proc.wait()  # Wait for the process to terminate
                print("motor_test.py stopped successfully.")
                return
        print("motor_test.py is not running.")
    except Exception as e:
        print(f"Error stopping motor_test.py: {e}")

def stop_live_feed():
    """
    Stops the live feed.
    """
    global process
    if process:
        try:
            print("\nLanding Appa... Please wait.")
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)  # Stop process group
            process.wait()
            process = None
            print("Appa landed safely.")
        except Exception as e:
            print(f"Error stopping live feed: {e}")

def close_gui():
    """
    Stops the live feed, motor_test.py, and returns to the main interface.
    """
    global root
    try:
        stop_live_feed()  # Ensure live feed is stopped
        stop_motor_program()  # Ensure motor_test.py is stopped
    except Exception as e:
        print(f"Error during shutdown: {e}")
    finally:
        if root:
            print("Returning to the main interface...")
            root.quit()  # Exit the Tkinter main loop



def zoom_in():
    """
    Zooms in the live feed by decreasing the ROI size.
    """
    global zoom_level
    if zoom_level > 0.2:  # Prevent excessive zoom-in
        zoom_level -= 0.1
        print(f"Zooming In: Appa's view is now at Zoom Level = {zoom_level:.1f}")
        start_live_feed()  # Restart feed with updated zoom

def zoom_out():
    """
    Zooms out the live feed by increasing the ROI size.
    """
    global zoom_level
    if zoom_level < 1.0:  # Prevent excessive zoom-out
        zoom_level += 0.1
        print(f"Zooming Out: Appa's view is now at Zoom Level = {zoom_level:.1f}")
        start_live_feed()  # Restart feed with updated zoom

def create_gui():
    """
    Creates the Tkinter GUI for live feed control.
    """
    global root
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Controller")

    # GUI dimensions
    window_width = 250
    window_height = 150

    # Calculate the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Position the window in the top-right corner
    position_x = 1200
    position_y = 300
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

    # Add control buttons
    zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in, width=10)
    zoom_in_button.place(x=65, y=10)

    zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out, width=10)
    zoom_out_button.place(x=65, y=40)

    stop_button = tk.Button(root, text="Stop", command=close_gui, bg="red", fg="white", width=10)
    stop_button.place(x=65, y=70)

    # Start live feed
    start_live_feed()

    # Run the Tkinter main loop
    root.protocol("WM_DELETE_WINDOW", close_gui)  # Ensure clean exit on close
    root.mainloop()

if __name__ == "__main__":
    start_program("sudo /home/pi/Desktop/Platinenprojekt/.venv/bin/python /home/pi/Desktop/Platinenprojekt/motor_test.py")
    create_gui()
