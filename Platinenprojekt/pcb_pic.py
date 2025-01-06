import os
import subprocess

def capture_test_picture():
    try:
        save_dir = "/home/pi/Desktop/Platinenprojekt/pictures"
        os.makedirs(save_dir, exist_ok=True)

        # Use a fixed filename
        filename = os.path.join(save_dir, "pcb.jpg")
        
        # Capture the image using libcamera-still
        command = [
            "libcamera-still",  # Command to capture image
            "--vflip",
            "--hflip",
            "-o", filename,    # Output file
            "--width", "4056",  # Set image width (adjust as needed)
            "--height", "3040", # Set image height (adjust as needed)
            "--timeout", "500" # Timeout for camera initialization
        ]
        
        print(f"Capturing image and saving to {filename}...")
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Image captured successfully!")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while capturing the image: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    capture_test_picture()