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
    path = "/Users/frankzhai/Desktop/gf2/docs/enbf/ebnf.txt"
    return path

def test_get_symbol(test_names, test_path, expected_output_type, expected_output_id):
    """Test that names, numbers, symbols and keywords are all
    initialised and stored in the right sections"""
    test_scan = Scanner(test_path, test_names)
    

    