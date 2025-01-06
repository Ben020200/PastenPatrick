import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import os

# Function to execute external programs
import subprocess
import os
from tkinter import messagebox

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
        subprocess.run(command_list)
    except Exception as e:
        messagebox.showerror("Error", f"The program '{program_command}' could not be started.\n{e}")


# Function to create a window with a consistent size and position
def create_window(title, width, height):
    root = tk.Tk()
    root.title(title)
    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    return root

# Function to set the background image
def set_background(root, image_path, crop_center=False, center_width=400, center_height=300):
    """
    Sets the background image of a Tkinter window.
    Optionally crops the center of the image.
    """
    if crop_center:
        # Load the image and crop the center
        image = Image.open(image_path)
        image_width, image_height = image.size

        # Calculate the bounding box for the center crop
        left = (image_width - center_width) // 2
        top = (image_height - center_height) // 2
        right = left + center_width
        bottom = top + center_height

        # Crop and resize the image to fit the window
        cropped_image = image.crop((left, top, right, bottom))
        tk_image = ImageTk.PhotoImage(cropped_image)
    else:
        # Load the full image
        image = Image.open(image_path)
        tk_image = ImageTk.PhotoImage(image)

    # Display the image as a background
    background_label = tk.Label(root, image=tk_image)
    background_label.image = tk_image  # Prevent garbage collection
    background_label.place(relwidth=1, relheight=1)

# First Interface: Pasten Patrick
def pasten_patrick():
    def open_manual():
        start_program("/home/pi/Desktop/Platinenprojekt/live_feed.py")
        start_program("sudo /home/pi/Desktop/Platinenprojekt/.venv/bin/python /home/pi/Desktop/Platinenprojekt/motor_test.py")


    def open_automatic():
        root.destroy()
        schablone_interface()

    # Create the window
    root = create_window("Pasten Patrick", 400, 300)
    set_background(root, "/home/pi/Desktop/Platinenprojekt/APPA.png", crop_center=True)  # Cropped background

    # Add title label
    title_label = tk.Label(root, text="Choose a mode:", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333")
    title_label.place(relx=0.5, rely=0.2, anchor="center")  # Centered title near the top

    # Add "Manual" button on the left
    manual_button = tk.Button(root, text="Manual", command=open_manual, width=15, height=2, bg="#4CAF50", fg="#ffffff")
    manual_button.place(relx=0.3, rely=0.5, anchor="center")  # Positioned 30% from the left

    # Add "Automatic" button on the right
    auto_button = tk.Button(root, text="Automatic", command=open_automatic, width=15, height=2, bg="#2196F3", fg="#ffffff")
    auto_button.place(relx=0.7, rely=0.5, anchor="center")  # Positioned 70% from the left

    root.mainloop()


# Second Interface: Schablone
def schablone_interface():
    def proceed_to_stencil_pic():
        start_program("/home/pi/Desktop/Platinenprojekt/stencil_pic.py")
        root.destroy()
    
     
        platine_interface()

    root = create_window("Schablone", 400, 300)
    set_background(root, "/home/pi/Desktop/Platinenprojekt/APPA.png", crop_center=True)  # Cropped background

    tk.Label(root, text="stencil is clamped, folded down, lights off.", 
             font=("Arial", 14), wraplength=350, bg="#ffffff", fg="#333333").pack(pady=20)

    ok_button = tk.Button(root, text="OK", command=lambda: [proceed_to_stencil_pic()], 
                          width=15, height=2, bg="#2196F3", fg="#ffffff")
    ok_button.pack(pady=20)

    root.mainloop()

# Third Interface: Platine
def platine_interface():
    def proceed_to_pcb_pic():
        start_program("/home/pi/Desktop/Platinenprojekt/pcb_pic.py")
        root.destroy()
    
        programm_interface()

    root = create_window("Platine", 400, 300)
    set_background(root, "/home/pi/Desktop/Platinenprojekt/APPA.png", crop_center=True)  # Cropped background

    tk.Label(root, text="insert PCB clamp it, Lights on.", font=("Arial", 14), bg="#ffffff", fg="#333333").pack(pady=20)

    ok_button = tk.Button(root, text="OK", command=lambda: [proceed_to_pcb_pic()], 
                          width=15, height=2, bg="#2196F3", fg="#ffffff")
    ok_button.pack(pady=20)

    root.mainloop()

# Fourth Interface: Programm
def programm_interface():
    def start_programs():
        start_program("/home/pi/Desktop/Platinenprojekt/Platine_alles entfernen.py")
        start_program("/home/pi/Desktop/Platinenprojekt/schablone_alles entfernen.py")
        start_program("/home/pi/Desktop/Platinenprojekt/ohne_drehung.py")
        start_program("/home/pi/Desktop/Platinenprojekt/APPA.py")
        root.destroy()

    root = create_window("Programm", 400, 300)
    set_background(root, "/home/pi/Desktop/Platinenprojekt/APPA.png", crop_center=True)  # Cropped background

    tk.Label(root, text="Start the program", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333").pack(pady=20)

    start_button = tk.Button(root, text="START", command=start_programs, width=15, height=2, bg="#4CAF50", fg="#ffffff")
    start_button.pack(pady=20)
    
    root.mainloop()
    start_program("/home/pi/Desktop/Platinenprojekt/live_feed.py")
    start_program("sudo /home/pi/Desktop/Platinenprojekt/.venv/bin/python /home/pi/Desktop/Platinenprojekt/motor_test.py")

# Start the main interface
if __name__ == "__main__":
    pasten_patrick()
    
