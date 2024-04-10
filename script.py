import argparse
import sys
import re

def parse_arguments():
    parser = argparse.ArgumentParser(description='Search for lines matching a regular expression in one or more files.')
    parser.add_argument('-r', '--regex', required=True, help='Regular expression to match.')
    parser.add_argument('-f', '--files', nargs='*', help='File(s) to search. Reads from STDIN if omitted.')
    parser.add_argument('-u', '--underscore', action='store_true', help='Print "^" under the matching text.')
    parser.add_argument('-c', '--color', action='store_true', help='Highlight matching text.')
    parser.add_argument('-m', '--machine', action='store_true', help='Generate machine readable output: file_name:no_line:start_pos:matched_text.')

    return parser.parse_args()

def search_in_line(line, regex, filename='', line_num=1, args=None):
    matches = list(re.finditer(regex, line))
    if not matches:
        return  # No matches, skip this line

    line_stripped = line.rstrip('\n')  # Remove newline for consistent handling
    prefix = f"{filename}:{line_num}: "  # Prefix to print before the line content

    if args.color:
        # Prepare the line with color highlights
        highlighted_line = line_stripped
        offset = 0
        for match in matches:
            start, end = match.span()
            start += offset
            end += offset
            matched_text = match.group()
            # Insert ANSI color codes
            highlighted_line = highlighted_line[:start] + f"\033[31m{matched_text}\033[0m" + highlighted_line[end:]
            # Adjust offset for added ANSI code lengths
            offset += len(f"\033[31m{matched_text}\033[0m") - len(matched_text)

    if args.underscore:
        # Prepare underscores for the matched text
        underscores = [' '] * len(line_stripped)
        for match in matches:
            start, end = match.span()
            for i in range(start, end):
                underscores[i] = '^'
        underscore_str = ''.join(underscores)

    # Printing logic
    if args.color:
        print(prefix + highlighted_line)
        if args.underscore:
            # Print underscores on a new line if both color and underscore are selected
            print(' ' * len(prefix) + underscore_str)
    elif args.underscore:
        # Print line and underscores if only underscore option is selected
        print(prefix + line_stripped)
        print(' ' * len(prefix) + underscore_str)
    else:
        # Default print statement if no special flags are used
        print(prefix + line_stripped)

def read_and_search(args):
    regex = re.compile(args.regex)
    if args.files:
        for filename in args.files:
            try:
                with open(filename, 'r') as file:
                    for line_num, line in enumerate(file, start=1):
                        search_in_line(line, regex, filename, line_num, args)
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
    else:
        for line_num, line in enumerate(sys.stdin, start=1):
            search_in_line(line, regex, line_num=line_num, args=args)

if __name__ == '__main__':
    args = parse_arguments()
    read_and_search(args)