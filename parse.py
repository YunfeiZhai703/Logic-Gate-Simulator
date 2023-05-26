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
from devices import Devices
from network import Network
from monitors import Monitors


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
        self.devices: Devices = devices
        self.network: Network = network
        self.monitors: Monitors = monitors
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
            self.scanner.current_line,
            self.scanner.current_character,
            self.scanner.current_position,
            error_code,
            message))

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.

        self.parse_devices_block()  # parsing devices block

        return True

    def advance(self):
        self.symbol = self.scanner.get_symbol()
        print(self.symbol)

    def parse_devices_block(self):
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

    def validate_device_name(self, device_list):
        if (self.symbol.type == self.scanner.NAME):
            if (self.symbol.name not in device_list):
                return True
            else:
                self.add_error(
                    ErrorCodes.NAME_DEFINED,
                    f"Name '{self.symbol.name}' already defined")
                return False

        else:
            self.add_error(ErrorCodes.INVALID_NAME, "Expected name")

    def parse_devices(self):
        i = 0
        while (self.symbol.type != self.scanner.OPEN_SQUARE_BRACKET):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [conns] block")
                break
            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in devices, please check that you have a [conns] block")
                break

            self.parse_device_line()

    def parse_device_line(self):
        print("Device line symbol:" + str(self.symbol))
        device_list = []

        if (self.validate_device_name(device_list)):
            device_list.append(self.symbol.name)
            devices_are_valid = True
            self.advance()

            while (
                self.symbol.type == self.scanner.COMMA and devices_are_valid
            ):
                self.advance()

                if (self.symbol.type == self.scanner.EQUAL):
                    break

                if (self.validate_device_name(device_list)):
                    device_list.append(self.symbol.name)
                    self.advance()
                else:
                    devices_are_valid = False

            if (devices_are_valid):
                if (self.symbol.type == self.scanner.EQUAL):
                    self.advance()

                    if (self.symbol.type == self.scanner.LOGIC):
                        gate = self.symbol.name
                        self.advance()
                        self.parse_logic_gate(gate, device_list)
                        self.advance()
                        print(device_list)
                    else:
                        self.add_error(
                            ErrorCodes.INVALID_LOGIC_GATE,
                            "Expected logic gate")

                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '='")

    def parse_logic_gate(self, gate, device_list):
        if (gate == "AND"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_gate(
                        device_id,
                        self.devices.AND,
                        2,
                    )
            else:
                number_inps = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        number_inps = int(self.symbol.name)

                        if (number_inps < 1 or number_inps > 16):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Number of inputs must be between 1 and 16")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_gate(
                                        device_id,
                                        self.devices.AND,
                                        number_inps,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass
        if (gate == "NAND"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_gate(
                        device_id,
                        self.devices.NAND,
                        2,
                    )
            else:
                number_inps = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        number_inps = int(self.symbol.name)

                        if (number_inps < 1 or number_inps > 16):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Number of inputs must be between 1 and 16")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_gate(
                                        device_id,
                                        self.devices.NAND,
                                        number_inps,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass
        if (gate == "OR"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_gate(
                        device_id,
                        self.devices.OR,
                        2,
                    )
            else:
                number_inps = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        number_inps = int(self.symbol.name)

                        if (number_inps < 1 or number_inps > 16):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Number of inputs must be between 1 and 16")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_gate(
                                        device_id,
                                        self.devices.OR,
                                        number_inps,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass
        if (gate == "NOR"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_gate(
                        device_id,
                        self.devices.NOR,
                        2,
                    )
            else:
                number_inps = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        number_inps = int(self.symbol.name)

                        if (number_inps < 1 or number_inps > 16):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Number of inputs must be between 1 and 16")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_gate(
                                        device_id,
                                        self.devices.NOR,
                                        number_inps,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass
        if (gate == "XOR"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_gate(
                        device_id,
                        self.devices.XOR,
                        2,
                    )
            else:
                number_inps = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        number_inps = int(self.symbol.name)

                        if (number_inps != 2):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Number of inputs must be 2")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_gate(
                                        device_id,
                                        self.devices.XOR,
                                        number_inps,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass

        if (gate == "DTYPE"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_d_type(
                        device_id
                    )
            else:
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected ';'")
            pass

        if (gate == "CLOCK"):
            clock_period = None
            if (self.symbol.type == self.scanner.OPEN_BRACKET):
                self.advance()

                if (self.symbol.type == self.scanner.NUMBER):
                    clock_period = int(self.symbol.name)

                    if (clock_period < 1):
                        self.add_error(
                            ErrorCodes.INVALID_NUMBER,
                            "Clock period must be greater than 0")

                    self.advance()

                    if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                        self.advance()

                        if (self.symbol.type == self.scanner.SEMICOLON):
                            device_ids = self.names.lookup(
                                device_list
                            )
                            for device_id in device_ids:
                                self.devices.make_clock(
                                    device_id,
                                    clock_period
                                )
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ';'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected ')'")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected number")
            else:
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected '('")

            pass

        if (gate == "SWITCH"):
            if (self.symbol.type == self.scanner.SEMICOLON):
                device_ids = self.names.lookup(
                    device_list
                )
                for device_id in device_ids:
                    self.devices.make_switch(
                        device_id,
                        0,
                    )
            else:
                switch_output = None
                if (self.symbol.type == self.scanner.OPEN_BRACKET):
                    self.advance()

                    if (self.symbol.type == self.scanner.NUMBER):
                        switch_output = int(self.symbol.name)

                        if (switch_output < 0 or switch_output > 1):
                            self.add_error(
                                ErrorCodes.INVALID_NUMBER,
                                "Output must be between 0 or 1")

                        self.advance()

                        if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                            self.advance()

                            if (self.symbol.type == self.scanner.SEMICOLON):
                                device_ids = self.names.lookup(
                                    device_list
                                )
                                for device_id in device_ids:
                                    self.devices.make_switch(
                                        device_id,
                                        switch_output,
                                    )
                            else:
                                self.add_error(
                                    ErrorCodes.SYNTAX_ERROR,
                                    "Expected ';'")
                        else:
                            self.add_error(
                                ErrorCodes.SYNTAX_ERROR,
                                "Expected ')'")
                    else:
                        self.add_error(
                            ErrorCodes.SYNTAX_ERROR,
                            "Expected number")
                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '('")

            pass

    def parse_conns_block(self):
        if (self.symbol.type == self.scanner.OPEN_SQUARE_BRACKET):
            self.advance()

            if (self.symbol.type ==
                    self.scanner.HEADING and self.symbol.name == "conns"):
                self.advance()

                if (self.symbol.type == self.scanner.CLOSE_SQUARE_BRACKET):
                    self.advance()

                    self.parse_conns()

                else:
                    self.add_error(
                        ErrorCodes.INVALID_HEADER, "Expected ']'")

            else:
                self.add_error(ErrorCodes.INVALID_HEADER, "Expected 'conns'")

        else:
            self.add_error(ErrorCodes.INVALID_HEADER, "Expected '['")

    def validate_inputs_name(self, conns_list):
        if (self.symbol.type == self.scanner.NAME):
            if (self.symbol.name not in conns_list):
                return True
            else:
                self.add_error(
                    ErrorCodes.CONNS_DEFINED,
                    f"Name '{self.symbol.name}' already defined")
                return False

        else:
            self.add_error(ErrorCodes.INVALID_NAME, "Expected name")

    def parse_conns(self):
        i = 0
        while (self.symbol.type != self.scanner.OPEN_SQUARE_BRACKET):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [monitor] block")
                break
            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in devices, please check that you have a [conns] block")
                break

            self.parse_conns_line()

    def parse_conns_line(self):
        print("Conns line current symbol: " + self.symbol.name)
        output = self.symbol.name
        # TODO: Handle DTYPE Name as it has two outputs (check for "." and then
        # check for "Q" or "QBAR")

        print("Conns line symbol:" + str(self.symbol))
        conns_list = []
        device_list = []

        if (self.validate_device_name(conns_list, device_list)):
            conns_list.append(self.symbol.name)
            conns_are_valid = True
            self.advance()

            while (
                self.symbol.type == self.scanner.EQUAL and conns_are_valid
            ):
                self.advance()

                if (self.validate_conns_name(conns_list)):
                    conns_list.append(self.symbol.name)
                    self.advance()
                else:
                    conns_are_valid = False

            if (conns_are_valid):
                if (self.symbol.type == self.scanner.EQUAL):
                    self.advance()

                    if (self.symbol.type == self.scanner.LOGIC):
                        gate = self.symbol.name
                        self.advance()
                        self.parse_logic_gate(gate, conns_list)
                        self.advance()
                        print(conns_list)
                    else:
                        self.add_error(
                            ErrorCodes.INVALID_LOGIC_GATE,
                            "Expected logic gate")

                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '='")

    def parse_monit_block(self):
        if (self.symbol.type == self.scanner.OPEN_SQUARE_BRACKET):
            self.advance()

            if (self.symbol.type ==
                    self.scanner.HEADING and self.symbol.name == "monit"):
                self.advance()

                if (self.symbol.type == self.scanner.CLOSE_SQUARE_BRACKET):
                    self.advance()

                    self.parse_monit()

                else:
                    self.add_error(
                        ErrorCodes.INVALID_HEADER, "Expected ']'")

            else:
                self.add_error(ErrorCodes.INVALID_HEADER, "Expected 'monit'")

        else:
            self.add_error(ErrorCodes.INVALID_HEADER, "Expected '['")

    def monit_validate_monit_name(self):
        pass

    def parse_monit(self):
        i = 0
        while (self.symbol.type != self.scanner.OPEN_SQUARE_BRACKET):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    # TODO: Do we need a way to identify the end of the text file
                    # or can we go back to start to see "[devices]"?
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [devices] block")
                break
            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in devices, please check that you have a [conns] block")
                break

            self.parse_monit_line()

    def parse_monit_line(self):
        print("Monit line symbol:" + str(self.symbol))
        monit_list = []

        if (self.validate_monit_name(monit_list)):
            monit_list.append(self.symbol.name)
            monit_are_valid = True
            self.advance()

            while (
                self.symbol.type == self.scanner.COMMA and monit_are_valid
            ):
                # Need to add if its followed by a dot and DATA, CLEAR, SET, Q OR QBAR as condition
                self.advance()

                if (self.symbol.type == self.scanner.SEMICOLON):
                    break

                if (self.validate_monit_name(monit_list)):
                    monit_list.append(self.symbol.name)
                    self.advance()
                else:
                    monit_are_valid = False

            if (monit_are_valid):
                if (self.symbol.type == self.scanner.SEMICOLON):
                    self.advance()

                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected ';'")
