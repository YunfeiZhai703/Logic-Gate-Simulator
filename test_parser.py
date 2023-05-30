import pytest
from scanner import Scanner, Symbol, ErrorCodes
from names import Names
from parser import Parser, ErrorCodes


@pytest.fixture
def test_names():
    names = Names()
    return names


@pytest.fixture
def test_scanner():
    scanner = Scanner()
    return scanner


@pytest.fixture
def test_parser():
    parser = Parser()
    return parser
