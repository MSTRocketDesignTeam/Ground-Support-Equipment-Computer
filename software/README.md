# GSEC User Interface

## Purpose

This directory includes the code required to run the GSEC GUI and trigger functions that will be physically executed on the rocket.

## Structure

**main.py** - Runs the executable script to start the GUI

**GUI.py** - Manages the GUI and sends commands to the controller based on the buttons pressed.

**theming.py** - Handles GUI theming

**controller.py** - Manages the logic around running sequences of functions and runs status checks before executing critical functions.

**commands.py** - Directly interfaces with the hardware by sending commands and reading sensor data directly from it.

**testing_simulator.py** - Fakes output like the commands.py module would send to test GUI redundancy under failure.
