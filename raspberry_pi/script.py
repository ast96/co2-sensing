import pathlib
import board
import adafruit_scd30

def foo():
    return "Hello world!"

def create_file(file):
    pathlib.Path.touch(file)
