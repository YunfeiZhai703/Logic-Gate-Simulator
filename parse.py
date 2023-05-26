"""Parse the definition file and build the logic network.

Used in the Logic Simulator project to analyse the syntactic and semantic
correctness of the symbols received from the scanner and then builds the
logic network.

Classes
-------
Parser - parses the definition file and builds the logic network.
"""
import sys
from typing import List
from scanner import Scanner, Symbol, SymbolList
from errors import Error, ErrorCodes
from names import Names


class Parser:

    """Parse the definition file and build the logic network.

    The parser deals with error handling. It analyses the syntactic and
    semantic correctness of the symbols it receives from the scanner, and
    then builds the logic network. If there are errors in the definition file,
    the parser detects this and tries to recover from it, giving helpful
    error messages.

    Parameters
    ----------
    names: instance of the names.Names() class.
    devices: instance of the devices.Devices() class.
    network: instance of the network.Network() class.
    monitors: instance of the monitors.Monitors() class.
    scanner: instance of the scanner.Scanner() class.

    Public methods
    --------------
    parse_network(self): Parses the circuit definition file.
    """

    def __init__(self, names, devices, network, monitors, scanner):
        """Initialise constants."""
        self.names: Names = names
        self.scanner: Scanner = scanner
        self.devices = devices
        self.network = network
        self.monitors = monitors
        self.symbol = self.scanner.get_symbol()
        self.errors: List[Error] = []

        self.ports_list = [
            self.DATA,
            self.CLK,
            self.SET,
            self.CLEAR,
            self.Q,
            self.QBAR] = range(6)  # delete if not needed

    def add_error(self, error_code, message):
        """Add an error to the list of errors."""
        self.errors.append(Error(
            self.current_line,
            self.current_character,
            self.current_position,
            error_code,
            message))

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        return True

    def advance(self):
        self.symbol = self.scanner.get_symbol()

    def parse_devices_header(self):
        if (self.symbol.type == self.scanner.OPEN_SQUARE_BRACKET):
            self.advance()

            if (self.symbol.type ==
                    self.scanner.HEADING and self.symbol.name == "devices"):
                self.advance()

                if (self.symbol.type == self.scanner.CLOSE_SQUARE_BRACKET):
                    self.advance()

                    self.parse_devices()

                else:
                    self.add_error(
                        ErrorCodes.INVALID_HEADER, "Expected ']'")

            else:
                self.add_error(ErrorCodes.INVALID_HEADER, "Expected 'devices'")

        else:
            self.add_error(ErrorCodes.INVALID_HEADER, "Expected '['")

    def validate_device_name(self):
        if (self.symbol.type == self.scanner.NAME):
            if (self.names.query(self.symbol.name) is None):
                self.names.insert(self.symbol.name)
            else:
                self.add_error(
                    ErrorCodes.NAME_DEFINED,
                    f"Name '{self.symbol.name}' already defined")

            self.advance()

        else:
            self.add_error(ErrorCodes.INVALID_NAME, "Expected name")

    def parse_devices(self):
        pass

    def parse_device_line(self):
        if (self.validate_device_name()):
            devices_are_valid = True
            self.advance()

            # advance to comma

            while (
                self.symbol.type == self.scanner.COMMA and devices_are_valid
            ):
                self.advance()

                if (self.validate_device_name()):
                    self.advance()
                else:
                    devices_are_valid = False

            if (devices_are_valid):
                if (self.symbol.type == self.scanner.EQUAL):
                    self.advance()

                    if (self.symbol.type == self.scanner.LOGIC):
                        self.parse_logic_gate()
                    else:
                        self.add_error(
                            ErrorCodes.INVALID_LOGIC_GATE,
                            "Expected logic gate")

                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '='")

        if self.symbol.type == self.scanner.SEMICOLON:
            self.advance()
        else:
            self.add_error(ErrorCodes.SYNTAX_ERROR, "Expected ';'")

    def parse_logic_gate(self):
        if (self.symbol.name == "AND"):
            pass
        if (self.symbol.name == "NAND"):
            pass
        if (self.symbol.name == "OR"):
            pass
        if (self.symbol.name == "NOR"):
            pass
        if (self.symbol.name == "XOR"):
            pass
        if (self.symbol.name == "DTYPE"):
            pass
        if (self.symbol.name == "CLOCK"):
            pass
