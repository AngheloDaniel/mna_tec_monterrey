"""Module get a list of number from a file and convert them to binary and hexadecimal base"""

import sys
import time
import os

FILE_SOURCE_DIR = "p2"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, "output", "ConversionResults.txt")


def get_numbers_from_file(file_name):
    """Opens a given file name to process the data and extract numeric values."""
    numbers = []
    file_path = os.path.join(FILE_SOURCE_DIR, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print(f"Collecting numbers from file {file_name}")
            for record in file:
                try:
                    numbers.append(int(record.strip()))
                except ValueError:
                    print(f"\nInvalid value: {record}, skipping...")
    except FileNotFoundError:
        print(f"File {file_name} not found at {FILE_SOURCE_DIR} directory")
        sys.exit(1)
    print("\nCollecting numbers from file process has finished")
    return numbers


def decimal_to_binary(number):
    """Converts a decimal number to binary using basic algorithm."""
    if number == 0:
        return "0"
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number //= 2
    return binary


def decimal_to_hexadecimal(number):
    """Converts a decimal number to hexadecimal using basic algorithm."""
    if number == 0:
        return "0"
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    while number > 0:
        remainder = number % 16
        hexadecimal = hex_chars[remainder] + hexadecimal
        number //= 16
    return hexadecimal


def get_file_name_from_params():
    """Retrieves the file name from command-line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python convert_numbers.py fileWithData.txt")
        sys.exit(1)
    return sys.argv[1]


def create_file_with_results(output_filename, results):
    """Writes the computed conversions to a file."""
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(results)


def main():
    """Main function to orchestrate reading, conversion, and output."""
    start_time = time.time()
    file_name = get_file_name_from_params()
    numbers = get_numbers_from_file(file_name)
    if not numbers:
        print("Error: No valid numbers found in the file.")
        sys.exit(1)
    print("\nStarting number conversions\n")
    results = ":: Conversion Results ::\n\n"
    for number in numbers:
        binary = decimal_to_binary(number)
        hexadecimal = decimal_to_hexadecimal(number)
        results += f"Decimal: {number} | Binary: {binary} | Hexadecimal: {hexadecimal}\n"
    elapsed_time = time.time() - start_time
    results += f"\nElapsed Time: {elapsed_time:.8f} seconds"
    print(results)
    create_file_with_results(OUTPUT_FILE_PATH, results)
    print(f"\nConversions exported to file: {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    main()
