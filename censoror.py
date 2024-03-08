import sys
import os
import assignment1.fileprocessor
import assignment1.argparser


def main():
    # Call the function to parse the arguments
    args = assignment1.argparser.parse_arguments()
    # Call the main function from fileprocessor.py and pass the arguments
    assignment1.fileprocessor.main(args)


if __name__ == "__main__":
    main()
