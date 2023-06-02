class ErrorCodes:
    INVALID_CHARACTER = "InvalidCharacter"
    INVALID_NAME = "InvalidName"
    INVALID_NUMBER = "InvalidNumber"
    INVALID_HEADER = "InvalidHeader"
    MISSING_HEADER = "MissingHeader"
    INVALID_PIN = "InvalidPin"
    MISSING_DOT = "MissingDot"
    MISSING_I = "MissingI"
    MISSING_PORT = "MissingPort"
    MISSING_REQUIRED_PARAMETER = "MissingRequiredParameter"
    NAME_DEFINED = "NameDefined"
    SYNTAX_ERROR = "SyntaxError"
    INVALID_LOGIC_GATE = "InvalidLogicGate"
    INVALID_DEVICE = "InvalidDevice"
    OVERFLOW_ERROR = "OverflowError"
    DEVICE_ERROR = "DeviceError"
    INVALID_INPUTS = "InputsError"

    description = {
        INVALID_CHARACTER: "This character is not allowed in the definition file.",
        INVALID_NAME: """"
        The name used is either a reserved word or is not a valid name for a device.
        Names must start with a letter and can only contain letters, numbers. Logic gates symbols must be in upper case.
        """,
        INVALID_NUMBER: "Invalid number",
        INVALID_HEADER: "Missing bracket in the header definition",
        MISSING_HEADER: "Missing header definition within the square brackets",
        INVALID_PIN: "Not a valid pin",
        MISSING_DOT: "Missing dot to show connections or output of dtype",
        MISSING_I: "Missing I before the input port number",
        MISSING_PORT: "Missing port for either the input or output",
        MISSING_REQUIRED_PARAMETER: "Missing a parameter that needs to be defined",
        NAME_DEFINED: "Name is already assigned to another gate",
        SYNTAX_ERROR: "General syntax error, i.e check for missing brackets, semicolon etc.",
        INVALID_LOGIC_GATE: "Logic gate is not valid",
        INVALID_DEVICE: "The device hasn't been defined in the [devices] block",
        OVERFLOW_ERROR: "Loops too many times",
        DEVICE_ERROR: "Error when making the device",
        INVALID_INPUTS: "The inputs should be within the range 1-16 and dtype inputs should be CLK, DATA, Q, QBAR, SET, CLEAR"}


class Error(SyntaxError):

    """Exception raised for errors in the input.

    Attributes
    ----------
    message : str
        explanation of the error
    """

    def __init__(
            self,
            line_number,
            line_content,
            char_number,
            error_code,
            message,
    ):
        """Initialise ScannerError with the message."""
        self.error_code = error_code
        self.message = message
        self.line_number = line_number
        self.line_content = line_content
        self.char_number = char_number

        self.description = ErrorCodes.description.get(
            error_code)

        self.error_message = f"Error - {error_code}: {message}" + "\n" + \
            f"Line {self.line_number + 1} Char {self.char_number + 1}:\n{self.line_content}" + \
            " " * (self.char_number) + "^" + "\n"
        if self.description:
            self.error_message += "Description: " + self.description + "\n"

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return self.error_message
