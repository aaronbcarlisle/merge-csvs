
import os
import pandas
import logging

from pathlib import Path


def merge_csvs_in_dir(csv_dir, recursive=False, pattern=None, save=True, overwrite=False):

    if not os.path.isdir(csv_dir):
        logging.warning(f"'{csv_dir}' does not exist!")
        return

    pattern = pattern or "*.csv"

    # use pathlib to glob for csv files
    csv_path = Path(csv_dir)
    csv_files = list(csv_path.rglob(pattern) if recursive else csv_path.glob(pattern))

    # remove the merged csv file from the list of csv files to merge
    csv_file_path = csv_path.joinpath(f"{csv_path.name}_merged.csv")
    if csv_file_path in csv_files:
        csv_files.remove(csv_file_path)

    # ensure not to include first index column (used for header data)
    csv_data = map(lambda x: pandas.read_csv(x, index_col=1), csv_files)
    merged_csv = pandas.concat(csv_data)

    if save:
        # use pandas to write out the merged csv
        merged_csv.to_csv(csv_file_path)
        logging.info(f"Saved merged csv as '{csv_file_path}'.")

    return merged_csv  # return the content


if __name__ == "__main__":
    test_csv_dir = Path.cwd().parent.joinpath("test_csvs")
    merged_test_csv = merge_csvs_in_dir(test_csv_dir, overwrite=True)
