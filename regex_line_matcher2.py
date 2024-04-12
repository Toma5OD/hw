import argparse
import sys
import re

# Base class for handling input and searches
class RegexSearcher:
    def __init__(self, regex, input_sources=None):
        self.regex = re.compile(regex)
        self.input_sources = input_sources or [sys.stdin]  # Default to STDIN

    def process_inputs(self):
        for source in self.input_sources:
            if source == sys.stdin:
                self.read_from_stdin()
            else:
                self.read_from_file(source)

    def read_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.process_file(file, filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

    def read_from_stdin(self):
        self.process_file(sys.stdin, "STDIN")

    def process_file(self, file, filename):
        for line_num, line in enumerate(file, start=1):
            line = line.rstrip('\n').replace('\t', '    ')  # Replace tabs with spaces
            self.search_line(line, filename, line_num)

    def search_line(self, line, filename, line_num):
        matches = list(self.regex.finditer(line))
        if matches:
            self.output_line(line, filename, line_num, matches)

    def output_line(self):
        # Default implementation, should be overridden
        pass

# Subclass for machine-readable output
class MachineReadable(RegexSearcher):
    def __init__(self, regex, input_sources=None):
        super().__init__(regex, input_sources)
        self.label_printed = False

    def output_line(self, line, filename, line_num, matches):
        if not self.label_printed:
            print("Machine-readable output:")
            self.label_printed = True
        for match in matches:
            start = match.start()
            print(f"{filename}:{line_num}:{start}:{match.group()}")

#   Subclass for underscore output
class Underscore(RegexSearcher):
    def __init__(self, regex, input_sources=None):
        super().__init__(regex, input_sources)
        self.label_printed = False

    def output_line(self, line, filename, line_num, matches):
        if not self.label_printed:
            print("Underscored output:")
            self.label_printed = True
        prefix = f"{filename if filename else 'STDIN'}:{line_num}: "
        line_stripped = line.rstrip('\n')
        underscores = [' '] * (len(prefix) + len(line_stripped))
        for match in matches:
            start = match.start() + len(prefix)
            end = match.end() + len(prefix)
            for i in range(start, end):
                underscores[i] = '^'
        print(f"{prefix}{line_stripped}")
        print(''.join(underscores))

# Subclass for color-highlighted output
class ColorHighlight(RegexSearcher):
    def __init__(self, regex, input_sources=None):
        super().__init__(regex, input_sources)
        self.label_printed = False

    def output_line(self, line, filename, line_num, matches):
        if not self.label_printed:
            print("Color-highlighted output:")
            self.label_printed = True
        highlighted_line = line
        offset = 0
        for match in matches:
            start = match.start() + offset
            end = match.end() + offset
            match_text = match.group()
            highlighted_line = (highlighted_line[:start] +
                                f"\033[31m{match_text}\033[0m" +
                                highlighted_line[end:])
            offset += len(f"\033[31m{match_text}\033[0m") - len(match_text)
        print(f"{filename}:{line_num}: {highlighted_line}")

# Subclass for combined color-highlighted and underscore output
class CombinedColorUnderscore(RegexSearcher):
    def __init__(self, regex, input_sources=None):
        super().__init__(regex, input_sources)
        self.label_printed = False

    def output_line(self, line, filename, line_num, matches):
        if not self.label_printed:
            print("Combined color-highlighted and underscored output:")
            self.label_printed = True
        prefix = f"{filename if filename else 'STDIN'}:{line_num}: "
        line_stripped = line.rstrip('\n')
        highlighted_line = line_stripped
        underscores = [' '] * len(line_stripped)
        offset = 0
        for match in matches:
            start, end = match.span()
            match_text = match.group()
            start_color = start + offset
            end_color = start_color + len(f"\033[31m{match_text}\033[0m")
            highlighted_line = (highlighted_line[:start_color] + f"\033[31m{match_text}\033[0m" +
                                highlighted_line[start_color + len(match_text):])
            offset += len(f"\033[31m{match_text}\033[0m") - len(match_text)
            for i in range(start, end):
                if i < len(underscores):
                    underscores[i] = '^'
        print(f"{prefix}{highlighted_line}")
        print(' ' * len(prefix) + ''.join(underscores))

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Search for lines matching a regular expression in one or more files.')
    parser.add_argument('-r', '--regex', required=True, help='Regular expression to match.')
    parser.add_argument('-f', '--files', nargs='*', help='File(s) to search. Reads from STDIN if omitted.')
    parser.add_argument('-u', '--underscore', action='store_true', help='Print "^" under the matching text.')
    parser.add_argument('-c', '--color', action='store_true', help='Highlight matching text.')
    parser.add_argument('-m', '--machine', action='store_true', help='Generate machine readable output.')
    return parser.parse_args()

# Main function to execute based on arguments
if __name__ == '__main__':
    args = parse_arguments()
    input_sources = args.files if args.files else [sys.stdin]

    # Define multiple searcher instances if needed
    searchers = []

    # Always include machine-readable if specified
    if args.machine:
        searchers.append(MachineReadable(args.regex, input_sources))

    # If both -u and -c are specified, handle them with the combined output class
    if args.underscore and args.color:
        searchers.append(CombinedColorUnderscore(args.regex, input_sources))
    else:
        # Handle underscore output separately if only -u is specified
        if args.underscore:
            searchers.append(Underscore(args.regex, input_sources))

        # Handle color output separately if only -c is specified
        if args.color:
            searchers.append(ColorHighlight(args.regex, input_sources))

    # No format specified, raise an error
    if not searchers:
        raise ValueError("At least one output format must be specified.")

    # Process input through all specified formatters
    for searcher in searchers:
        searcher.process_inputs()
