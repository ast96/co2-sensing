from pathlib import Path
import script

def test_create_file(tmp_path):
    file = tmp_path / 'test-output.txt'
    script.create_file(file)
    assert Path(file).exists()

def test_connect_to_board():
    assert script.connect_to_board() == 1
