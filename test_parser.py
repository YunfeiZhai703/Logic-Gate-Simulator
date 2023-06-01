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
    path = "tests/parser/test2.txt"
    return path


@pytest.fixture
def test_error_1():
    path = "tests/parser/inputs_error.txt"
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


def test_error_inputs(test_error_1):
    new_parser = set_up(test_error_1)
    new_errors = new_parser.errors
    for e in new_errors:
        assert e.error_code == ErrorCodes.INVALID_INPUTS
