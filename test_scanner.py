import pytest
from scanner import Scanner, Symbol, ErrorCodes
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
def test_path_1():
    path = "tests/scanner/test_file_1.txt"
    return path


@pytest.fixture
def test_path_2():
    path = "tests/scanner/test_file_2.txt"


@pytest.fixture
def test_path_error_1():
    path = "tests/scanner/error_1.txt"
    return path


@pytest.fixture
def test_path_error_2():
    path = "tests/scanner/error_2.txt"
    return path


@pytest.fixture
def test_path_error_3():
    path = "tests/scanner/error_3.txt"
    return path


def test_get_symbol(test_names, test_path_1):
    """Test that names, numbers, symbols and keywords are all
    initialised and stored in the right sections"""
    test_scan = Scanner(test_path_1, test_names)

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


def test_keywords_error(test_names, test_path_error_1):
    """Test that keywords are not allowed as names"""
    test_scan = Scanner(test_path_error_1, test_names)
    test_scan.get_all_symbols()
    errors = test_scan.errors

    for e in errors:
        assert e.error_code == ErrorCodes.INVALID_NAME


def test_invalid_char_error(test_names, test_path_error_2):
    """Test that keywords are not allowed as names"""
    test_scan = Scanner(test_path_error_2, test_names)
    test_scan.get_all_symbols()
    errors = test_scan.errors

    for e in errors:
        assert e.error_code == ErrorCodes.INVALID_CHARACTER
        assert e.line_number == 32
        assert e.char_number == 12


def test_no_semicolon(test_names, test_path_error_3):
    """Test that it raises an error for no semicolon"""

    test_scan = Scanner(test_path_error_3, test_names)
    test_scan.get_all_symbols()
    errors = test_scan.errors

    for e in errors:
        assert e.error_code == ErrorCodes.SYNTAX_ERROR
