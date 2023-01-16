from pathlib import Path
import board
import adafruit_scd30

def create_file(file):
    Path.touch(file)

def connect_to_board():
    sensor_board = adafruit_scd30.SCD30(board.I2C())
    return sensor_board.data_available
