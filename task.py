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
    with open(input_file) as read_file:
        #load all data for ranking processing 
        file_data = [item for item in csv.DictReader(read_file)]

    ranking_worker = Ranking(data=file_data)
    ranking = ranking_worker.generate_ranking()

    with open(output_file, 'w+',  newline='') as written_file:
        field_names = ['Place','Team','Score']
        writer = csv.DictWriter(written_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(ranking)


if __name__ == "__main__":
    entrypoint()
