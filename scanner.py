"""Read the circuit definition file and translate the characters into symbols.

Used in the Logic Simulator project to read the characters in the definition
file and translate them into symbols that are usable by the parser.

Classes
-------
Scanner - reads definition file and translates characters into symbols.
Symbol - encapsulates a symbol and stores its properties.
"""


class Symbol:

    """Encapsulate a symbol and store its properties.

    Parameters
    ----------
    No parameters.

    Public methods
    --------------
    No public methods.
    """

    def __init__(self):
        """Initialise symbol properties."""
        self.type = None
        self.id = None


class Scanner:

    """Read circuit definition file and translate the characters into symbols.

    Once supplied with the path to a valid definition file, the scanner
    translates the sequence of characters in the definition file into symbols
    that the parser can use. It also skips over comments and irrelevant
    formatting characters, such as spaces and line breaks.

    Parameters
    ----------
    path: path to the circuit definition file.
    names: instance of the names.Names() class.

    Public methods
    -------------
    get_symbol(self): Translates the next sequence of characters into a symbol
                      and returns the symbol.
    """

    def __init__(self, path, names):
        """Open specified file and initialise reserved words and IDs."""
        self.names = names
        self.symbol_list = [self.HEADING, self.KEYWORD, self.NUMBER, self.NAME,
                                self.EQUAL, self.DOT, self.COMMA, self.SEMICOLON,
                                self.OPEN_SQUARE, self.CLOSE_SQUARE, self.OPEN_BRACKET, self.CLOSE_BRACKET,
                                self.HASHTAG, self.EOF] = range(14)
        self.headings_list = ["[devices]", "[conns]", "[monit]"]
        [self.DEVICES_ID, self.CONNS_ID, self.MONIT_ID] = self.names.lookup(self.headings_list)
        self.keywords_list = ["="]
        self.ignore = ["#"]
        self.stopping_list = [self.SEMICOLON, self.EOF]
        self.current_character = ""
        self.current_line = 0
        self.error_count = 0
        
    def get_symbol(self):
        """Translate the next sequence of characters into a symbol."""

        symbol = Symbol()
        self.skip_spaces() # current character now not whitespace

        if self.current_character.isalpha():
            name_string = self.get_name()
            self.name_string = name_string[0]


            if name_string in self.keywords_list:
                symbol.type = self.KEYWORD
            else:
                symbol.type = self.NAME
            [symbol.id] = self.names.lookup([name_string])


        elif self.current_character.isdigit():
            symbol.id = self.get_number()
            symbol.type = self.NUMBER
            print(symbol.id[0], end = '')

        elif self.current_character == "=":  # punctuation
            symbol.type = self.EQUALS
            self.advance()

        elif self.current_character == ",":
            symbol.type = self.COMMA
            self.advance()

        elif self.current_character == ".":
            symbol.type = self.DOT
            self.advance()

        elif self.current_character == ";":
            symbol.type = self.SEMICOLON
            self.advance()
            print(";")
        
        elif self.current_character == "#":
            symbol.type = self.COMMA
            self.advance()

        elif self.current_character == "{":
            symbol.type = self.CURLY_OPEN
            self.advance()
            print("{", end = '')

        elif self.current_character == "}":
            symbol.type = self.CURLY_CLOSE
            self.advance()
            print("}")

        elif self.current_character == "-":
            symbol.type = self.MINUS
            self.advance()
            self.error(SyntaxError, "Negative symbls not allowed")

        elif self.current_character == "":  # end of file
            symbol.type = self.EOF

        else:  # not a valid character
            self.advance()
        return symbol
    
    def get_name(self):
        # Want to find the name that comes next in input_file
        # Return the name and the next character that is non-alphanumeric
        name = self.current_character
        while True:
            self.current_character = self.advance()
            if self.current_character.isalnum():
                name = name + self.current_character
            else:
                return [name, self.current_character]

    def get_number(self):
        number = self.current_character
        while True:
            self.current_character = self.advance()
            if number.isdigit():
                number += self.current_character
            else:
                return [number, self.current_character]
            
    def skip_spaces(self):
        while self.current_character.isspace():
            self.current_character = self.advance()

    def advance(self):
        if self.read_string:
            try:
                self.current_character = self.input_file[self.count_character]
            except IndexError:
                self.current_character = ""
                return self.current_character
            self.count_character += 1
        else:
            self.current_character = self.input_file.read(1)

        self.character_number += 1

        if self.current_character == '\n':
            self.current_line += 1
            self.character_number = self.word_number = 0

        return self.current_character

    def error(self, error_type):
        self.error_count += 1
        if error_type == self.NO_NUMBER:
            print("Expected a number")
        if error_type == self.NO_EQUALS:
            print("Expected a equal sign")

