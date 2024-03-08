import argparse
import glob
import re
import os
import sys
from assignment1.argparser import parse_arguments
from assignment1.censor_content import censor_content
import json
from pprint import pformat
import spacy
import en_core_web_trf


def main(args):

    # Construct entire file paths from args.input, args.output
    abspathsIP = [os.path.abspath(path) for path in args.input]
    abspathsOP = os.path.abspath(args.output)
    if args.stats != "stderr" and args.stats != "stdout":
        abspathsST = os.path.abspath(args.stats)

    # Initialize a list to store all file paths
    all_file_paths = []
    # Loop through each input pattern and find all files that match the pattern
    for input_pattern in abspathsIP:
        file_paths = glob.glob(input_pattern)
        # If no files are found, exit the program
        if not file_paths:
            sys.exit(f"No files found using pattern: {input_pattern}")

        # Add the found file paths to the list of all file paths
        all_file_paths.extend(file_paths)

    # Load the en_core_web_trf model
    nlp = en_core_web_trf.load()

    # Intuitive label mapping for the entities
    label_mapping = {
        "NORP": "Nationalities or Religious or Political Groups",
        "GPE": "Geopolitical Entities",
        "FAC": "Facilities",
        "ORG": "Organizations",
        "PERSON": "Persons",
        "LOC": "Locations",
        "PRODUCT": "Products",
        "EVENT": "Events",
        "WORK_OF_ART": "Art Works",
        "LAW": "Laws",
        "LANGUAGE": "Languages",
        "DATE": "Dates",
        "TIME": "Times",
        "PERCENT": "Percentages",
        "MONEY": "Monetary Values",
        "QUANTITY": "Quantities",
        "ORDINAL": "Ordinal Numbers",
        "CARDINAL": "Cardinal Numbers",
        "PHONE": "Phone Numbers",
        "EMAIL": "Email IDs",
    }

    # If stats file exists, delete it
    if os.path.exists(args.stats):
        os.remove(args.stats)

    # Loop through each file path to censor the content
    # and write the censored content to a new file
    # Also, write the statistics to a file
    for path in all_file_paths:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            censored_content, stats_output = censor_content(content, nlp, label_mapping)
            # Save censored content with .censored extension
            output_path = os.path.join(
                args.output, os.path.basename(path) + ".censored"
            )
            with open(output_path, "w", encoding="utf-8") as outfile:
                outfile.write(censored_content)

        json_output = json.dumps(stats_output)
        prettyStats = pformat(stats_output)
        fileMode = (
            "w"
            if not os.path.exists(args.stats) or args.stats in ["stderr", "stdout"]
            else "a"
        )

        # If stats is stderr or stdout, print the stats to console
        if args.stats == "stderr":
            sys.stderr.write(f"Filename: {os.path.basename(path)}\n")
            sys.stderr.write("Censored Content Stats: \n")
            sys.stderr.write(prettyStats)
            sys.stderr.write("\n\n")

        elif args.stats == "stdout":
            sys.stdout.write(f"Filename: {os.path.basename(path)}\n")
            sys.stdout.write("Censored Content Stats: \n")
            sys.stdout.write(prettyStats)
            sys.stdout.write("\n\n")

        # If stats is a file, write the stats to the file
        else:
            with open(abspathsST, fileMode, encoding="utf-8") as statsfile:
                statsfile.write(f"Filename: {os.path.basename(path)}\n")
                statsfile.write("Censored Content Stats: \n")
                statsfile.write(prettyStats)
                statsfile.write("\n\n")


if __name__ == "__main__":
    main()
