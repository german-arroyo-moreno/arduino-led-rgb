#!/usr/bin/python3

import os
import sys
import serialv


def write_read(arduino_id, x):
    """
    Encodes a string and sends it to the specified serial device.

    Args:
        arduino_id (serial.Serial): The active serial port object to write to.
        x (str): The string message to send to the device.
    """
    # Encode the string to utf-8, add a newline character, and send it.
    # The .strip() method removes any leading/trailing whitespace from the input.
    arduino_id.write(bytes(x.strip() + "\n", 'utf-8'))
    # Print a confirmation message to the console.
    print(f"\tSending: {x}\\n")

# ----------------------------------------
#          MAIN PROGRAM
# ----------------------------------------

## 1. Discover potential Arduino devices
# ----------------------------------------
# Initialize an empty list to store device names.
devices = []
# Walk through the /dev/ directory to find all files.
# In Linux, connected devices often appear as files in /dev/.
for path, currentDirectory, files in os.walk("/dev/"):
    for f in files:
        # Arduinos often register as 'ttyACM' followed by a number (e.g., ttyACM0).
        if f.startswith("ttyACM"):
            devices.append(f)

## 2. User selection of the device
# ----------------------------------------
print("Select the device:")
# Enumerate and print the list of found devices for the user to choose from.
for index, d in enumerate(devices):
    print(f"[{index + 1}] {d}")

# Exit if no devices were found.
if not devices:
    print("No devices found!")
    sys.exit(1)

# Prompt the user for their choice.
chosen_str = input(": ")

# If the user just presses Enter, default to the first device (index 1).
if chosen_str == "":
    chosen_index = 1
else:
    # Convert input to an integer.
    # Clamp the value to be within the valid range of choices [1, number of devices].
    # This prevents IndexError if the user enters a number that is too high or low.
    chosen_index = max(1, min(int(chosen_str), len(devices)))

# Get the device name string from the list using the user's choice.
# We subtract 1 because list indices are 0-based.
device = devices[chosen_index - 1]
print(f"Selected driver: {device}")

## 3. Establish Serial Communication and Send Data
# ----------------------------------------
# The 'with' statement ensures the serial port is automatically closed even if errors occur.
# Connect to the chosen device port with a baud rate of 9600.
try:
    with serial.Serial(port=f'/dev/{device}', baudrate=9600, timeout=1) as arduino:
        print(f"Successfully connected to: {arduino.name}")
        exitLoop = False
        # Start a loop to continuously ask for user input.
        while not exitLoop:
            num = input("> ") # Taking input from user

            # If the user enters an empty string, exit the loop.
            if len(num) == 0:
                print("\tExit...")
                exitLoop = True
            else:
                # If input is provided, send it to the Arduino.
                write_read(arduino, num)

except serial.SerialException as e:
    print(f"Error: Could not open port '{device}'.")
    print(f"Details: {e}")
    print("Please check the connection and ensure you have the correct permissions.")
    sys.exit(1)
