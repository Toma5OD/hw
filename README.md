# Regex Line Matcher

A Python script designed to search through files or standard input (STDIN) for lines that match a specified regular expression and print the matches with various formatting options.

## Goals of the Script

- **Regex Search**: Implement a Python script to search for lines that match a specified regular expression (`-r` or `--regex`) within one or more files (`-f` or `--files`).
- **STDIN Support**: Allow using Standard Input (STDIN) as an alternative input source when no file is specified, enhancing flexibility for data input.
- **ASCII Input**: Handle input assuming it's in ASCII format, simplifying the encoding considerations.
- **Match Output**: For each line that contains a match, output the line itself, prefixed with the file name and the line number to easily identify the match's location.
- **Output Formatting Options**: Provide optional formatting for matches through mutually exclusive parameters:
  - `-u` or `--underscore`: Add a caret (`^`) under the matching text.
  - `-c` or `--color`: Highlight the matching text for visual emphasis. (Note: Terminal must support ANSI color codes.)
  - `-m` or `--machine`: Generate output in a machine-readable format specified as `file_name:no_line:start_pos:matched_text`, facilitating the use of output by other programs or scripts.
- **Multiple Matches Handling**: Support identifying and formatting multiple matches within a single line, ensuring that all occurrences are captured and displayed without overlap.
- **PEP8 Compliance**: Ensure the script is written following the PEP8 coding guidelines to promote readability and maintainability of the code.
- **Documentation and Error Handling**: Include comprehensive documentation within the script and implement robust error handling for a smooth and understandable user experience.
- **OOP and Design Patterns**: While developing, attempt to utilize Object-Oriented Programming (OOP) principles to encapsulate the differences between output formats efficiently. Additionally, document the design pattern(s) used in the script's development to clarify the architectural choices.

## Folder Layout

Below is an image illustrating the layout of the `public` folder, showcasing where each file is located within the directory:

![Folder Layout](/public/layout.png)

## File Descriptions

- **oop_regex_line_matcher.py**: This is the main script and the most recent version, which utilizes Object-Oriented Programming principles. It searches for lines in text files that match a specified regular expression. This script represents an advanced iteration with improved modularity and flexibility.

- **regex_line_matcher.py**: A previous version of the script that may not fully utilize Object-Oriented Programming principles. It serves as an earlier iteration for searching lines that match specified regular expressions in text files. The script can read from files listed in command arguments or from Standard Input (STDIN) if no files are specified.

- **text.txt**: A test text file used to demonstrate and test the functionality of the main script, `oop_regex_line_matcher.py`. This file is relatively small, making it ideal for quick demonstrations and validations.

- **text2.txt**: Another test text file, serving a similar purpose. This file is used to validate functionalities in different versions of the script, including the earlier `regex_line_matcher.py`.

## Features Implemented

- **Regular Expression Matching**: Uses a user-defined regex pattern to search for matches within the content of files or STDIN.
- **Flexible Input Options**: Searches in one or multiple files specified by the user or reads from STDIN if no file is provided.
- **Output Formatting Options**:
  - **Underscore**: Prints a caret (`^`) under the matching text.
  - **Color**: Highlights the matching text in the terminal.
  - **Machine Readable**: Generates output in a format suitable for machine parsing: `file_name:no_line:start_pos:matched_text`.
  - **Combined Color and Underscore**: Provides an option to highlight matching text and print carets under the matching sections simultaneously.
- **Support for Multiple Matches**: Capable of identifying and formatting multiple matches within a single line, without overlapping.
- **PEP8 Compliant**: The code structure adheres to the PEP8 coding guidelines, ensuring readability and maintainability.
- **Error Handling**: Includes basic error management for file access issues and provides user feedback for missing arguments.
- **Documentation**: Inline comments and method descriptions are provided to explain the functionality and usage of the classes and functions.

### Design Pattern Used

- **Strategy Pattern**: The script employs the strategy pattern through the use of different output formatting classes that inherit from a common base. This design allows for flexible and interchangeable output behaviors depending on user options without altering the core logic of input processing and regex matching.

## Usage

To use the script, navigate to the directory containing `oop_regex_line_matcher.py` and run the following command in the terminal:

```bash
python oop_regex_line_matcher.py -r "YOUR_REGEX" -f text2.txt ... [OPTIONS]
```

### Options

- `-r` or `--regex`: **Required**. The regular expression pattern to search for.
- `-f` or `--files`: Optional. The file(s) to search through. If omitted, the script reads from STDIN.
- `-u` or `--underscore`: Optional. Adds a caret (`^`) underneath the matching text.
- `-c` or `--color`: Optional. Highlights the matching text. Terminal must support ANSI color codes.
- `-m` or `--machine`: Optional. Outputs the matches in a machine-readable format.

### Examples

Search for digits in `text2.txt` and highlight them:

```bash
python oop_regex_line_matcher.py -r "\d+" -f text.txt --color
```

Read from STDIN and generate machine-readable output for matches:

```bash
cat text.txt | python oop_regex_line_matcher.py -r "\d+" --machine
```

## Implementation Details

The script employs the `argparse` module for command-line argument parsing and the `re` module for regex matching, adhering to recommended practices for Python scripting. The choice of output formatting demonstrates a simple yet effective application of conditional logic to provide user-friendly and versatile output customization based on user commands. This approach not only makes the script highly adaptable to different use cases but also showcases efficient programming techniques in Python.

## License

This script is made available under the MIT License, which allows for wide use, modification, distribution, and private or commercial purposes. The MIT License is one of the most permissive and straightforward licenses available, ensuring that the script remains free and open-source, with minimal restrictions on its usage. This approach encourages innovation and collaboration by allowing users and developers to build upon the work without complex legal barriers.
