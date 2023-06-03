import os
from i18n import Translate

t = Translate("errors")


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
        INVALID_CHARACTER: t("description.INVALID_CHARACTER"),
        INVALID_NAME: t("description.INVALID_NAME"),
        INVALID_NUMBER: t("description.INVALID_NUMBER"),
        INVALID_HEADER: t("description.INVALID_HEADER"),
        MISSING_HEADER: t("description.MISSING_HEADER"),
        INVALID_PIN: t("description.INVALID_PIN"),
        MISSING_DOT: t("description.MISSING_DOT"),
        MISSING_I: t("description.MISSING_I"),
        MISSING_PORT: t("description.MISSING_PORT"),
        MISSING_REQUIRED_PARAMETER: t("description.MISSING_REQUIRED_PARAMETER"),
        NAME_DEFINED: t("description.NAME_DEFINED"),
        SYNTAX_ERROR: t("description.SYNTAX_ERROR"),
        INVALID_LOGIC_GATE: t("description.INVALID_LOGIC_GATE"),
        INVALID_DEVICE: t("description.INVALID_DEVICE"),
        OVERFLOW_ERROR: t("description.OVERFLOW_ERROR"),
        DEVICE_ERROR: t("description.DEVICE_ERROR"),
        INVALID_INPUTS: t("description.INVALID_INPUTS")}


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
