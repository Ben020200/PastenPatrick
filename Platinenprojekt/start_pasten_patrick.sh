#!/bin/bash

# Activate the virtual environment
source /home/pi/Desktop/Platinenprojekt/.venv/bin/activate


# Run the Python script
python /home/pi/Desktop/Platinenprojekt/pasten_patrick.py

# Turn on the display (optional)
xset dpms force on
