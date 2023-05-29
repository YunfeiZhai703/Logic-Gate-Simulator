class ErrorCodes:
    INVALID_CHARACTER = "InvalidCharacter"
    INVALID_NAME = "InvalidName"
    INVALID_NUMBER = "InvalidNumber"
    INVALID_HEADER = "InvalidHeader"
    MISSING_HEADER = "MissingHeader"
    MISSING_DOT = "MissingDot"
    MISSING_I = "MissingI"
    MISSING_PORT = "MissingPort"
    NAME_DEFINED = "NameDefined"
    SYNTAX_ERROR = "SyntaxError"
    INVALID_LOGIC_GATE = "InvalidLogicGate"
    INVALID_DEVICE = "InvalidDevice"
    OVERFLOW_ERROR = "OverflowError"

    description = {
        INVALID_CHARACTER: "This character is not allowed in the definition file.",
        INVALID_NAME: """
        The name used is either a reserved word or is not a valid name for a device.
        Names must start with a letter and can only contain letters, numbers. Logic gates symbols must be in upper case.
        """,
        INVALID_NUMBER: "Invalid number",
        INVALID_HEADER: "Missing bracket in the header definition.",
        MISSING_HEADER: "Missing header definition."}


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
            f"Line {self.line_number + 1} Char {self.char_number + 1}:\n{self.line_content}" + "\n" + \
            " " * (self.char_number) + "^" + "\n"
        if self.description:
            self.error_message += "Description: " + self.description + "\n"

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return self.error_message
