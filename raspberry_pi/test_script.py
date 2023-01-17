from pathlib import Path

import board
import adafruit_scd30

import script


sensor_board = adafruit_scd30.SCD30(board.I2C())

def test_generate_unique_filename_1():
    name1 = script.generate_unique_filename()
    name2 = script.generate_unique_filename()
    assert name1 != name2

def test_generate_unique_filename_2():
    name = script.generate_unique_filename()
    assert name[-4:] == '.csv'

def test_get_script_directory():
    assert script.get_script_directory() == '/home/akselthomas/workspace/co2-sensing/raspberry_pi'

def test_get_output_directory():
    assert script.get_output_directory() == '/home/akselthomas/workspace/co2-sensing/raspberry_pi/output'
    
def test_create_file(tmp_path):
    file = tmp_path / 'test-output.txt'
    script.create_file(file)
    assert Path(file).exists()

def test_check_connection_to_board():
    assert script.check_connection_to_board(sensor_board) == 1

def test_connect_to_board():
    assert isinstance(script.connect_to_board(), adafruit_scd30.SCD30)

def test_collect_data_row_1():
    assert isinstance(script.collect_data_row(sensor_board), str)

def test_collect_data_row_2():
    data_row = script.collect_data_row(sensor_board)
    assert len(data_row.split(',')) == 3

