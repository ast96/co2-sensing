from datetime import datetime
from pathlib import Path
from random import getrandbits

import board
import adafruit_scd30


def generate_unique_filename():
    return datetime.now().isoformat() + '_' + hex(getrandbits(16)) + '.csv'

def get_script_directory():
    return str(Path(__file__).parent.resolve())

def get_output_directory():
    return get_script_directory() + '/output'

def create_file(file):
    Path.touch(file)

def connect_to_board():
    return adafruit_scd30.SCD30(board.I2C())

def check_connection_to_board(sensor_board):
    return sensor_board.data_available

def main():
    # note that the file got created by `root`, not my user
    path = Path(get_output_directory() + '/' + generate_unique_filename())
    create_file(path)

if __name__ == '__main__':
    main()
