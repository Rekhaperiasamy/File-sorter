import argparse
from datetime import datetime

from generator import Generator


def generate_test_file(size_gb: float, output_path: str):
    print(f"Starting file generation at {
          datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target size: {size_gb}GB")
    generator = Generator()
    target_bytes = int(size_gb * 1024 * 1024 * 1024)
    generator.generate_file(target_bytes, output_path)


def main():
    parser = argparse.ArgumentParser(
        description='Generate a test file of specified size')
    parser.add_argument('-s', '--size', type=float, required=True,
                        help='Size of the file to generate in GB')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file path')

    args = parser.parse_args()
    generate_test_file(args.size, args.output)


if __name__ == "__main__":
    main()
