from pathlib import Path
import board
import adafruit_scd30
import script

def test_create_file(tmp_path):
    file = tmp_path / 'test-output.txt'
    script.create_file(file)
    assert Path(file).exists()

def test_check_connection_to_board():
    sensor_board = adafruit_scd30.SCD30(board.I2C())
    assert script.check_connection_to_board(sensor_board) == 1

def test_connect_to_board():
    assert isinstance(script.connect_to_board(), adafruit_scd30.SCD30)
