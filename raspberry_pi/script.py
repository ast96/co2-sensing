from datetime import datetime
from pathlib import Path
from random import getrandbits
from subprocess import run
from time import sleep

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
    data_row = datetime.now().isoformat(timespec='seconds')
    data_row += ',' + '{0:.0f}'.format(sensor_board.CO2)
    data_row += ',' + '{0:.1f}'.format(sensor_board.temperature)
    return data_row

def make_header_row():
    return 'Timestamp,CO2,Temperature'

def write_line_to_file(line, file):
    file.write(line + '\n')

def main():
    # 360 reads = 180 min / 0.5 min/read (3 hrs)
    # 5 minute fudge factor
    MAX_ITERATIONS = 1140
    run(['/usr/sbin/i2cdetect', '-y', '1'], capture_output=True)
    sleep(0.1)
    run(['/usr/sbin/i2cdetect', '-y', '1'], capture_output=True)
    try:
        sensor_board = connect_to_board()
    except:
        sleep(1)
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
            sleep(30)
            i += 1
    run(['/usr/sbin/shutdown', '-h', 'now'], capture_output=True)


if __name__ == '__main__':
    main()
