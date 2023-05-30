import pytest
from scanner import Scanner, Symbol, ErrorCodes
from names import Names
from parse import *


@pytest.fixture
def test_names():
    names = Names()
    return names


@pytest.fixture
def test_file_1():
    path = "tests"
