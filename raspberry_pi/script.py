from pathlib import Path
import board
import adafruit_scd30

def create_file(file):
    Path.touch(file)
