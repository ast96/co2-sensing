from datetime import datetime
from pathlib import Path
from random import randbytes

import board
import adafruit_scd30


def generate_unique_filename():
    return datetime.now().isoformat() + "_" + str(randbytes(4))

def create_file(file):
    Path.touch(file)

def connect_to_board():
    return adafruit_scd30.SCD30(board.I2C())

def check_connection_to_board(sensor_board):
    return sensor_board.data_available

def main():
    return

if __name__ == '__main__':
    main()
