import pytest
from scanner import Scanner, Symbol
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
    path = "tests/scanner/test_file_1.txt"
    return path


def test_get_symbol(test_names, test_path):
    """Test that names, numbers, symbols and keywords are all
    initialised and stored in the right sections"""
    test_scan = Scanner(test_path, test_names)

    test_string = [
        "[",
        "devices",
        "]",
        "G1",
        ",",
        "G8",
        ",",
        "G9",
        "=",
        "AND",
        ";"]

    for symbol in test_string:
        assert symbol == test_scan.get_symbol().name

    headings = "devices"

    # scan until heading is found
    while True:
        symbol = test_scan.get_symbol()
        if symbol.name == headings:
            assert symbol.type == test_scan.HEADING
        if symbol.name in ["G1", "G8", "G9"]:
            assert symbol.type == test_scan.NAME
        if symbol.type == test_scan.EOF:
            break
