# Logic Simulator Team 19

## Running the program

On the DPO ensure you have `anaconda` running.
To run the program, simply run the following command in the terminal:

```
python logisim.py <path-to-circuit-file>
```

To run with a specific language (on Linux), specify the LANG environment variable:

```
LANG=<lang>.utf8 python logisim.py <path-to-circuit-file>
```

Where `<lang>` is one of the following:

- `en_US`, `en_GB` for English
- `fr_FR` for French
- `es_ES` for Spanish
- `ru_RU` for Russian

By default, the program will run in English.

Example files can be found in the `example_files` directory.

## Deviations from PEP8

We are following most of the PEP8 guidelines, but we have made a few exceptions:

- E501: We have allowed lines to be up to 120 characters long, instead of the recommended 79 characters. This is because we have a lot of long lines in our code, and we feel that it is more readable to allow longer lines.
- F401: We have allowed unused imports as it does not affect the functionality of the program.
- F841: We have allowed unused variables as it does not affect the functionality of the program and they are used for debugging purposes.
- W503: We have allowed line breaks before binary operators as it is more readable to have the operator on the next line.
