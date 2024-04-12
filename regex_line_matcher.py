import argparse
import sys
import re

# Function to parse command-line arguments
# Technically, this function is not PEP8 compliant as it exceeds the 79-character limit.
# However, it is more readable in this format.
# Adhearance to PEP8 can be achieved by breaking the lines into multiple lines.
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

    line_stripped = line.rstrip('\n')
    prefix = f"{filename if filename else 'STDIN'}:{line_num}: "

    output_generated = False

    # Machine-readable output
    if args.machine:
        print("Machine-readable output:")
        for match in matches:
            start, _ = match.span()
            print(f"{prefix}{start}:{match.group()}")
        output_generated = True


    highlighted_line = line_stripped
    if args.color:
        if output_generated:  # Check before color-specific output
            print()  # Separate from previous output only if it was generated
        if not args.underscore:  # Print if not combined with underscore
            print("Color-highlighted output:")
        offset = 0
        for match in matches:
            start, end = match.span()
            start += offset
            end += offset
            matched_text = match.group()
            highlighted_line = highlighted_line[:start] + f"\033[31m{matched_text}\033[0m" + highlighted_line[end:]
            offset += len(f"\033[31m{matched_text}\033[0m") - len(matched_text)
        output_generated = True

    # Prepare underscores for matched text
    underscore_str = ''
    if args.underscore:
        underscores = [' '] * len(line_stripped)
        for match in matches:
            start, end = match.span()
            for i in range(start, end):
                underscores[i] = '^'
        underscore_str = ''.join(underscores)
        # Print underscore output message
        if not args.color:  # Avoid printing message if color is shown
            print("Underscored output:")
        
    # Output handling
    if args.color or args.underscore:
        if args.color and args.underscore:  # Combined output
            print("Combined color-highlighted and underscored output:")
        print(prefix + (highlighted_line if args.color else line_stripped))
        if args.underscore:
            print(' ' * len(prefix) + underscore_str)
        output_generated = True

    # Default output when no specific format is requested
    if not any([args.machine, args.color, args.underscore]) and output_generated:
        print("Default output:")  # Separate from previous output if applicable
        print(prefix + line_stripped)

def read_and_search(args):
    regex = re.compile(args.regex)
    filename = ''  # Use an empty string to represent STDIN although STDIN is added to the prefix in the search_in_line function
    if args.files:
        for filename in args.files:
            try:
                with open(filename, 'r') as file:
                    for line_num, line in enumerate(file, start=1):
                        search_in_line(line, regex, filename, line_num, args)
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
    else:
        # When reading from STDIN, filename is left as an empty string.
        for line_num, line in enumerate(sys.stdin, start=1):
            search_in_line(line, regex, filename, line_num, args)

if __name__ == '__main__':
    args = parse_arguments()
    read_and_search(args)