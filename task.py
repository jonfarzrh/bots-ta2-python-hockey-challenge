import argparse
import csv

from src.ranking import Ranking


def entrypoint() -> None:
    """Main entry point for the hockey ranker CLI.

    Raises:
        FileNotFoundError: If the input_file argument points to a file that does not exist.
        TypeError: If the input_file argument points to a non-file (eg, a directory).
    """
    parser = argparse.ArgumentParser(
        description="CLI to rank teams from a list of game results"
    )
    parser.add_argument("input_file", help="Location of input CSV")
    parser.add_argument("output_file", help="Location to write output CSV")

    # Parse out the input file
    args = parser.parse_args()

    # Here are your two arguments: the input CSV and the output CSV
    input_file = args.input_file
    output_file = args.output_file

    #read the file as stream
    with open(input_file) as f:
        #load all data for ranking processing 
        file_data = [item for item in csv.DictReader(f)]

    my_ranking = Ranking(data=file_data)
    my_ranking.generate_ranking()


if __name__ == "__main__":
    entrypoint()
