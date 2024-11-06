# sort_test_file.py
import argparse
from datetime import datetime

from sorter import Sorter


def sort_file(input_path: str, output_path: str):
    print(f"Sorting started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sorter = Sorter()
    sorter.sort_file(input_path, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Sort a large text file using external merge sort')
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Input file path')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file path')

    args = parser.parse_args()
    sort_file(args.input, args.output)


if __name__ == "__main__":
    main()
