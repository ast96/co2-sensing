from pathlib import Path
import board
import adafruit_scd30

def create_file(file):
    Path.touch(file)

def connect_to_board():
    return adafruit_scd30.SCD30(board.I2C())

def check_connection_to_board(sensor_board):
    return sensor_board.data_available
