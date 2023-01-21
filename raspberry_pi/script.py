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

def collect_data_row(sensor_board):
    data_row = datetime.now().isoformat()
    data_row += ',' + '{0:.0f}'.format(sensor_board.CO2)
    data_row += ',' + '{0:.1f}'.format(sensor_board.temperature)
    return data_row

def make_header_row():
    return 'Timestamp,CO2,Temperature'

def write_line_to_file(line, file):
    file.write(line + '\n')

def main():
    MAX_ITERATIONS = 360    # 360 reads = 180 min / 0.5 min/read (3 hrs)
    sensor_board = connect_to_board()
    collect_data_row(sensor_board)      # warm up the sensor
    # note that the file got created by `root`, not my user
    path = Path(get_output_directory() + '/' + generate_unique_filename())
    create_file(path)
    with open(path, 'a') as f:
        write_line_to_file(make_header_row(), f)
        i = 0
        while i < MAX_ITERATIONS:
            write_line_to_file(collect_data_row(sensor_board), f)
            time.sleep(30)
            i++

    # then, test it by running it for 2 minutes, instead
    # (optionally) have it shut down the raspberry pi at the end

if __name__ == '__main__':
    main()
