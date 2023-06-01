import pytest
from scanner import Scanner, Symbol, SymbolList
from parse import Parser
from errors import Error, ErrorCodes
from names import Names
from devices import Device, Devices
from network import Network
from monitors import Monitors


@pytest.fixture
def test_file_1():
    path = "tests/parser/test1.txt"
    return path


@pytest.fixture
def test_file_2():
    path = "tests/parser/test_device_parse.txt"
    return path


@pytest.fixture
def test_error_1():
    path = "tests/parser/test_inputs_error.txt"
    return path


@pytest.fixture
def test_error_2():
    path = "tests/parser/test_heading_error.txt"
    return path


@pytest.fixture
def test_error_3():
    path = "tests/parser/test_device_error.txt"
    return path


@pytest.fixture
def test_error_4():
    path = "tests/parser/test_device_stored.txt"
    return path


@pytest.fixture
def test_error_5():
    path = "tests/parser/test_dtype_pin_not_valid.txt"
    return path


@pytest.fixture
def test_error_6():
    path = "tests/parser/test_monit_heading_error.txt"
    return path


@pytest.fixture
def test_error_7():
    path = "tests/parser/test_conns_heading_error.txt"
    return path


@pytest.fixture
def test_error_8():
    path = "tests/parser/test_no_monit_heading_error.txt"


@pytest.fixture
def test_error_9():
    path = "tests/parser/test_syntax_error.txt"
    return path


@pytest.fixture
def test_error_10():
    path = "tests/parser/test_missing_parameters.txt"
    return path


def set_up(path):
    test_names = Names()
    test_scanner = Scanner(path, test_names)
    test_devices = Device(test_names)
    test_network = Network(test_names, test_devices)
    test_monitors = Monitors(test_names, test_devices, test_network)
    test_parser = Parser(
        test_names,
        test_devices,
        test_network,
        test_monitors,
        test_scanner)
    return test_parser


def test_parser(test_file_1):
    """Test the parser to see if it is working properly"""
    new_parser = set_up(test_file_1)
    new_parser.parse_network()
    assert new_parser.errors == []


def test_device_parser(test_error_3):
    """Test the logic gate errors"""
    new_parser = set_up(test_error_3)
    new_parser.parse_devices_block()
    new_errors = new_parser.errors
    e = new_errors[0]
    assert e.error_code == ErrorCodes.INVALID_LOGIC_GATE


def missing_heading(test_error_8):
    """Test missing heading errors"""
    new_parser = set_up(test_error_8)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.MISSING_HEADER


def test_error_inputs(test_error_1):
    """Test inputs out of range errors"""
    new_parser = set_up(test_error_1)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_INPUTS


def test_syntax_errors(test_error_9):
    """Test all types of possible syntax error"""
    new_parser = set_up(test_error_9)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.SYNTAX_ERROR


def test_missing_parameter(test_error_10):
    """Test for missing parameter for clock"""
    new_parser = set_up(test_error_10)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.MISSING_REQUIRED_PARAMETER


def test_missing_ports():
    pass


def test_device_not_stored(test_error_4):
    # Tests if a device in conns or monit has not been defined in [devices]
    new_parser = set_up(test_error_4)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_DEVICE


def test_dtype_pin_invalid(test_error_5):
    # Tests if a dtype pin specified is invalid, i.e. not Q or QBAR
    new_parser = set_up(test_error_5)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_PIN


def test_missing_bracket_in_header(test_error_6):
    # Tests if missing a closed bracket in the header definition, monit
    new_parser = set_up(test_error_6)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_HEADER


def test_missing_bracket_in_header(test_error_7):
    # Tests if missing an open bracket in the header definition, conns
    new_parser = set_up(test_error_7)
    new_parser.parse_network()
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_HEADER
