class ErrorCodes:
    INVALID_CHARACTER = "InvalidCharacter"
    INVALID_NAME = "InvalidName"
    INVALID_NUMBER = "InvalidNumber"

    description = {
        INVALID_CHARACTER: "This character is not allowed in the definition file.", INVALID_NAME: """
        The name used is either a reserved word or is not a valid name for a device.
        Names must start with a letter and can only contain letters, numbers. Logic gates symbols must be in upper case.
        """, INVALID_NUMBER: "Invalid number", }


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
            message):
        """Initialise ScannerError with the message."""
        self.error_code = error_code
        self.message = message
        self.line_number = line_number
        self.line_content = line_content
        self.char_number = char_number

        self.error_message = f"Error - {error_code}: {message}" + "\n" + \
            f"Line {self.line_number} Char {self.char_number}:\n{self.line_content}" + "\n" + \
            " " * (self.char_number) + "^" + "\n" + \
            "Description: " + ErrorCodes.description[error_code] + "\n"

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return self.error_message
