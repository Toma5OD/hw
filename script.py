import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Search for lines matching a regular expression in one or more files.')
    parser.add_argument('-r', '--regex', required=True, help='Regular expression to match.')
    parser.add_argument('-f', '--files', nargs='*', help='File(s) to search. Reads from STDIN if omitted.')
    parser.add_argument('-u', '--underscore', action='store_true', help='Print "^" under the matching text.')
    parser.add_argument('-c', '--color', action='store_true', help='Highlight matching text.')
    parser.add_argument('-m', '--machine', action='store_true', help='Generate machine readable output: file_name:no_line:start_pos:matched_text.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    print(args)  # Temporary, to demonstrate argument parsing works.
