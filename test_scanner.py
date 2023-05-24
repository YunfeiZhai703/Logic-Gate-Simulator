import pytest
from scanner import *
from names import Names

@pytest.fixture
def test_names():
    names = Names()
    return names

@pytest.fixture
def test_symbol():
    symbol = Symbol()
    return symbol

@pytest.fixture
def test_path():
    path = "/Users/frankzhai/Desktop/gf2/docs/tests_file/test_file.txt"
    return path

def test_get_symbol(test_names, test_path):
    """Test that names, numbers, symbols and keywords are all
    initialised and stored in the right sections"""
    test_scan = Scanner(test_path, test_names)
    test_string = [
        "[devices]",
        "G1",
        "G8",
        "G9",
        "=",
        "AND",
        
  
    ]

    for symbol in test_string:
        assert symbol == test_scan.get_symbol()

    