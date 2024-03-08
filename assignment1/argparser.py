import argparse
import glob
import re
import os
import sys


# Define a function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Censor sensitive information from files."
    )
    parser.add_argument(
        "--input",
        action="append",
        required=True,
        type=str,
        help="Input file pattern(s) to process. Can be specified multiple times.",
    )
    parser.add_argument(
        "--names", required=True, action="store_true", help="Flag to censor names."
    )
    parser.add_argument(
        "--dates",
        required=True,
        action="store_true",
        help="Flag to censor dates. Will also censor times.",
    )
    parser.add_argument(
        "--phones",
        required=True,
        action="store_true",
        help="Flag to censor different phone number formats.",
    )
    parser.add_argument(
        "--address",
        required=True,
        action="store_true",
        help="Flag to censor addresses.",
    )
    parser.add_argument(
        "--email",
        action="store_true",
        help="Flag to censor email addresses.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=str,
        help="Output directory to write censored files. Make sure it exists.",
    )
    parser.add_argument(
        "--stats",
        required=True,
        type=str,
        help="File to write statistics. Use 'stdout' or 'stderr' to print to console, or specify a file path.",
    )
    return parser.parse_args()
