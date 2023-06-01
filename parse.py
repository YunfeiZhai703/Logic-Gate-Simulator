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
from devices import Device, Devices
from network import Network
from monitors import Monitors
import re


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
        self.stored_device_list: List[str] = []

    def add_error(self, error_code, message, prev_line=False):
        """Add an error to the list of errors."""

        if (prev_line):
            self.errors.append(Error(
                self.scanner.current_line - 1,
                self.scanner.get_previous_line(),
                self.scanner.current_position,
                error_code,
                message))
        else:
            self.errors.append(Error(
                self.scanner.current_line,
                self.scanner.get_current_line(),
                self.scanner.current_position,
                error_code,
                message))

    def parse_network(self):
        """Parse the circuit definition file."""

        # For now just return True, so that userint and gui can run in the
        # skeleton code. When complete, should return False when there are
        # errors in the circuit definition file.
        expection = False
        try:
            self.parse_devices_block()  # parsing devices block
            self.parse_conns_block()
            self.parse_monit_block()
        except Exception as e:
            print(e)
            expection = True

        if (len(self.errors) > 0 or len(self.scanner.errors) > 0 or expection):

            all_errors = self.scanner.errors + self.errors

            return False, all_errors

        return True, []

    def advance(self):
        """Advance the scanner to the next symbol."""
        self.symbol = self.scanner.get_symbol()
        print(self.symbol)

    def parse_devices_block(self):
        """Parses the header of the devices block, and then calls parse_devices."""
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
        """Validates the device name."""
        if (self.symbol.type == self.scanner.NAME):
            if (self.symbol.name not in device_list and self.symbol.name not in self.stored_device_list):
                return True
            else:
                self.add_error(
                    ErrorCodes.NAME_DEFINED,
                    f"Name '{self.symbol.name}' already defined")
                return False

        else:
            self.add_error(
                ErrorCodes.SYNTAX_ERROR,
                "Invalid symbol: " +
                self.symbol.name +
                " if this is a comma, you may have missed a end of line on the previous line")
            return False

    def parse_devices(self):
        """Parses the devices block. By """
        i = 0
        while (self.symbol.type != self.scanner.OPEN_SQUARE_BRACKET):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [conns] block")
                break

            if (self.symbol.type == self.scanner.EOF):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [conns] block")
                break

            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in devices, please check that you have a [conns] block")
                break

            res = self.parse_device_line()
            if res == "Failed":
                break

    def parse_device_line(self):
        """Parses a single line of the devices block."""
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
                    self.stored_device_list.append(self.symbol.name)
                    self.advance()
                else:
                    devices_are_valid = False
                    break

            if (devices_are_valid):
                if (self.symbol.type == self.scanner.EQUAL):
                    self.advance()

                    if (self.symbol.type == self.scanner.LOGIC):
                        gate = self.symbol.name
                        self.advance()
                        self.parse_logic_gate(gate, device_list)
                        self.advance()
                    else:
                        self.add_error(
                            ErrorCodes.INVALID_LOGIC_GATE,
                            "Expected logic gate")

                else:
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected '='")
        else:
            return "Failed"

    def parse_logic_gate(self, device_type, device_list):
        """
        Parses the logic gate, and creates the device.


        @Dhillon: A lot of this is very unessesary,
        look at the make_device function in devices.py
        it does the main part for you, I have rewrote the code for this!!! - Lakee
        """
        param = {
            "AND": 2,
            "OR": 2,
            "NAND": 2,
            "NOR": 2,
            "XOR": None,
            "SWITCH": 0,
            "CLOCK": None,
            "DTYPE": None,
        }[device_type]

        ending_bracket = None

        if (self.symbol.type == self.scanner.OPEN_BRACKET):
            self.advance()
            if (self.symbol.type == self.scanner.NUMBER):
                param = int(self.symbol.name)
                self.advance()
                if (self.symbol.type == self.scanner.CLOSE_BRACKET):
                    self.advance()
                    ending_bracket = True
                else:
                    ending_bracket = False
                    self.add_error(
                        ErrorCodes.SYNTAX_ERROR,
                        "Expected ')' after number")

        if (ending_bracket is False):
            return

        if (device_type == "CLOCK" and not param):
            self.add_error(
                ErrorCodes.MISSING_REQUIRED_PARAMETER,
                "Expected parameter for CLOCK")
            return

        device_kind = {
            "AND": self.devices.AND,
            "OR": self.devices.OR,
            "NAND": self.devices.NAND,
            "NOR": self.devices.NOR,
            "XOR": self.devices.XOR,
            "SWITCH": self.devices.SWITCH,
            "CLOCK": self.devices.CLOCK,
            "DTYPE": self.devices.D_TYPE,
        }[device_type]

        device_ids = self.names.lookup(
            device_list
        )
        for i, device_id in enumerate(device_ids):
            name = device_type + ":" + device_list[i]
            error = self.devices.make_device(
                device_id,
                device_kind,
                param,
                name
            )
            if (error != self.devices.NO_ERROR):
                self.add_error(
                    ErrorCodes.DEVICE_ERROR,
                    "Error in making device " +
                    name +
                    " Error code:" +
                    str(error))

    def parse_conns_block(self):
        """Parses the conns header then calls parse_conns."""
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

    def parse_conns(self):
        """Parses the conns block by calling parse_conns_line until it reaches the end of the block"""
        i = 0
        while (self.symbol.type != self.scanner.OPEN_SQUARE_BRACKET):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [conns] block")
                break
            if (self.symbol.type == self.scanner.EOF):
                self.add_error(
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [conns] block")
                break

            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in conns, please check that you have a [monitor] block")
                break
            self.parse_conns_line()

    def check_inputs_name(self, string):
        """Check if inputs are in the form Ia, where a is digit from 1 - 16"""
        input_valid = False
        pattern = r'^I([1-9]|1[0-6])$'
        dtype_pins = ["CLK", "DATA", "Q", "QBAR", "SET", "CLEAR"]
        if re.match(pattern, string) or string in dtype_pins:
            input_valid = True
        else:
            self.add_error(
                ErrorCodes.INVALID_INPUTS,
                "Invalid name for device input")

        return input_valid

    def validate_device_name_for_conns(self):
        """Validates the device name ensuring it is a valid device name and the device exists"""
        try:
            if self.names.query(self.symbol.name) is None:
                self.add_error(
                    ErrorCodes.INVALID_NAME,
                    "Invalid device name")
                return False
            else:
                return True
        except SyntaxError:
            self.add_error(
                ErrorCodes.SYNTAX_ERROR,
                "Invalid symbol: " +
                self.symbol.name +
                " if this is a equals sign, you may have missed a end of line on the previous line")
            return False

    def parse_conns_line(self):
        """Parses a single line of the conns block"""
        device_list = []
        ports_list = []

        if self.validate_device_name_for_conns():
            device_list.append(self.symbol.name)

            self.advance()

            # Checking for DTYPE outputs
            if self.symbol.type == self.scanner.DOT:
                self.advance()
                if self.symbol.name in ["Q", "QBAR"]:
                    ports_list.append(self.symbol.name)
                    self.advance()
                else:
                    self.add_error(
                        ErrorCodes.INVALID_PIN,
                        "Invalid name for device output of DTYPE")

            # Check for = sign denoting a connection
            if self.symbol.type == self.scanner.EQUAL:
                self.advance()

                # While not reached end of line or EOF
                while self.symbol.type not in [
                        self.scanner.SEMICOLON, self.scanner.EOF]:

                    # validate the device name
                    if self.validate_device_name_for_conns():
                        device_list.append(self.symbol.name)
                        self.advance()

                        if self.symbol.type == self.scanner.DOT:
                            self.advance()

                            # validate the input/output name
                            if self.check_inputs_name(self.symbol.name):
                                ports_list.append(self.symbol.name)
                                self.advance()

                                if self.symbol.type == self.scanner.SEMICOLON:
                                    # Reached end of line
                                    self.advance()
                                    # print(
                                    #     "------- Dev: ", device_list, "Ports: ", ports_list)
                                    break

                                elif self.symbol.type == self.scanner.COMMA:
                                    # Continue to next device
                                    self.advance()
                            else:  # Not sure if we raise the error immediately
                                raise ValueError('Inputs value out of range')
                    else:
                        break

                # output device is the first device in the list
                output_device_id = self.names.query(device_list[0])
                output_device = self.devices.get_device(output_device_id)

                # input devices are the rest of the devices in the list
                input_device_ids = self.names.lookup(device_list[1:])
                input_devices = [self.devices.get_device(
                    device_id) for device_id in input_device_ids]

                # If len of ports list is same as len of device list, then we
                # have a DTYPE
                if len(ports_list) == len(device_list):
                    dtype_mapping = {
                        "Q": self.devices.Q_ID,
                        "QBAR": self.devices.QBAR_ID}

                    output_device_pin_id = dtype_mapping[ports_list[0]]
                    # remove the DTYPE Q or QBAR from the list
                    ports_list.pop(0)
                else:
                    output_device_pin_id = None

                for i, input_dev in enumerate(input_devices):
                    port_name = ports_list[i]
                    input_id = None

                    if port_name in ["CLK", "DATA", "SET", "CLEAR"]:
                        input_id = {
                            "CLK": self.devices.CLK_ID,
                            "DATA": self.devices.DATA_ID,
                            "SET": self.devices.SET_ID,
                            "CLEAR": self.devices.CLEAR_ID}[port_name]
                    else:
                        input_device_pin_index = int(port_name[1:]) - 1

                        if input_dev:
                            input_dict = input_dev.inputs
                            input_keys = list(input_dict.keys())
                            if input_device_pin_index + 1 > len(input_keys):

                                self.add_error(
                                    ErrorCodes.INVALID_PIN,
                                    "Invalid pin for device input, device only has " +
                                    str(len(input_keys)) + " inputs",
                                    prev_line=True
                                )
                            else:
                                input_id = input_keys[input_device_pin_index]

                        else:
                            self.add_error(
                                ErrorCodes.INVALID_DEVICE,
                                "Device not defined in 'devices'")

                    if input_id:
                        error = self.network.make_connection(
                            output_device_id, output_device_pin_id, input_device_ids[i], input_id)

                        if error != self.network.NO_ERROR:
                            print(
                                "----------ERROR in make_connection----------Code: ", error)

        else:
            self.add_error(
                ErrorCodes.INVALID_DEVICE,
                "Device name not defined in 'devices'")

    def parse_monit_block(self):
        """Parses the monit block header and calls parse_monit()"""
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

    def parse_monit(self):
        """Parses the monit block by calling parse_monit_line() until EOF"""
        i = 0
        while (self.symbol.type != self.scanner.EOF):
            i += 1
            if (self.symbol.type == self.scanner.HEADING):
                self.add_error(
                    # TODO: Do we need a way to identify the end of the text file
                    # or can we go back to start to see "[devices]"?
                    ErrorCodes.SYNTAX_ERROR,
                    "Expected [monit] block")
                break
            if (i > 500):
                self.add_error(
                    ErrorCodes.OVERFLOW_ERROR,
                    "Overflow error: Looping too many times in devices, please check that you have correctly defined monitor block")
                break

            self.parse_monit_line()

    def parse_monit_line(self):
        """Parses a single line of the monit block"""
        devices_list = []
        dtype_outputs_list = []

        if self.validate_device_name_for_conns():
            devices_list.append(self.symbol.name)
            self.advance()

            # While not reached end of line or EOF
            while self.symbol.type not in [
                    self.scanner.SEMICOLON, self.scanner.EOF]:
                # Checking for DTYPE outputs
                if self.symbol.type == self.scanner.DOT:
                    self.advance()
                    if self.symbol.name in ["Q", "QBAR"]:
                        dtype_outputs_list.append(self.symbol.name)
                        self.advance()
                    else:
                        self.add_error(
                            ErrorCodes.INVALID_PIN,
                            "Invalid name for device output of DTYPE")
                elif self.symbol.type == self.scanner.COMMA:
                    self.advance()
                    if self.validate_device_name_for_conns():
                        devices_list.append(self.symbol.name)
                        self.advance()
            # get output devices
            output_device_ids = [self.names.query(dev) for dev in devices_list]

            # If len of ports list is same as len of device list, then we
            # have a DTYPE
            if len(dtype_outputs_list) == len(devices_list):
                dtype_mapping = {
                    "Q": self.devices.Q_ID,
                    "QBAR": self.devices.QBAR_ID}

                output_device_pin_id = dtype_mapping[dtype_outputs_list[0]]
                # remove the DTYPE Q or QBAR from the list
                dtype_outputs_list.pop(0)
            else:
                output_device_pin_id = None

            for i, output_device_id in enumerate(output_device_ids):
                error = self.monitors.make_monitor(
                    output_device_id, output_device_pin_id)
                if error != self.monitors.NO_ERROR:
                    print(
                        "----------ERROR in make_connection----------Code: ",
                        error,
                        self.monitors.MONITOR_PRESENT)

            self.advance()

        else:
            self.add_error(
                ErrorCodes.INVALID_DEVICE,
                "Device name not defined in 'devices'")
