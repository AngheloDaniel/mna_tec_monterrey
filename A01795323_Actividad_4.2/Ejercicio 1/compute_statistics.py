"""Module that computes statistics of a list of numbers extracted from a file"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_SOURCE_DIR = "p1"
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, "output", "StatisticsResults.txt")


def get_numbers_from_file(file_name):
    """Opens a given file name to process the data and extract numeric values."""
    numbers = []
    file_path = '/'.join((FILE_SOURCE_DIR, file_name))

    try:
        with open(file_path, 'r', encoding="UTF-8") as file:
            print(f"Collecting numbers from file {file_name}")
            for record in file:
                try:
                    numbers.append(float(record.strip()))
                except ValueError:
                    print(f"\nInvalid value:{record}, trying to fix the data issue...")
                    fixed_value = get_float_value(record)

                    if fixed_value is not None:
                        numbers.append(fixed_value)
                        print(f"...{record} was converted to {fixed_value}")

    except FileNotFoundError:
        print(f"File {file_name} not found at {FILE_SOURCE_DIR} directory")
        sys.exit(1)

    print("\nCollecting numbers from file process has finished")
    return numbers


def get_float_value(record):
    """Attempts to extract a valid float value from a record."""
    try:
        record = record.replace(',', '.')
        record = record.replace(';', '.')

        digits_from_string = ''.join(c for c in record if c.isdigit() or c == '.')
        return float(digits_from_string)
    except ValueError:
        print(f"Error: {record} can't be converted to float")
        return None


def compute_mean(numbers):
    """Calculates the mean of a list of numbers."""
    return sum(numbers) / len(numbers)


def compute_median(numbers):
    """Calculates the median of a list of numbers."""
    sorted_list = sorted(numbers)
    list_len = len(sorted_list)
    mid_value = list_len // 2

    if list_len % 2 == 0:
        return (sorted_list[mid_value - 1] + sorted_list[mid_value]) / 2

    return sorted_list[mid_value]


def compute_mode(numbers):
    """Calculates the mode(s) of a list of numbers."""
    frequency = {}

    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1

    max_freq = max(frequency.values())
    modes = [num for num, count in frequency.items() if count == max_freq]

    return modes


def compute_variance(numbers, mean):
    """Calculates the sample variance of a list of numbers."""
    list_len = len(numbers)
    return sum((x - mean) ** 2 for x in numbers) / (list_len - 1) if list_len > 1 else 0


def compute_standard_deviation(numbers, mean):
    """Calculates the standard deviation of a list of numbers."""
    return (sum((x - mean) ** 2 for x in numbers) / len(numbers)) ** 0.5


def get_file_name_from_params():
    """Retrieves the file name from command-line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
        sys.exit(1)

    return sys.argv[1]


def create_file_with_statistics(output_filename, statistics):
    """Writes the computed statistics to a file."""
    with open(output_filename, 'w', encoding="UTF-8") as file:
        file.write(statistics)


def main():
    """Main function to orchestrate reading, computation, and output of statistics."""
    start_time = time.time()

    file_name = get_file_name_from_params()
    numbers = get_numbers_from_file(file_name)

    if not numbers:
        print("The file does not contain valid numbers")
        sys.exit(1)

    print("\nStarting the calculation of the statistics\n")

    mean = compute_mean(numbers)
    median = compute_median(numbers)
    mode = compute_mode(numbers)
    variance = compute_variance(numbers, mean)
    standard_deviation = compute_standard_deviation(numbers, mean)

    elapsed_time = time.time() - start_time

    statistics = (f"::Results::\n\n"
                  f"Count: {len(numbers)} records\n"
                  f"Mean: {mean}\n"
                  f"Median: {median}\n"
                  f"Mode: {mode[0]}\n"
                  f"Standard Deviation: {standard_deviation}\n"
                  f"Variance: {variance}\n"
                  f"\nElapsed Time: {elapsed_time:.8f} seconds")

    print(statistics)

    create_file_with_statistics(OUTPUT_FILE_PATH, statistics)
    print(f"\nStatistics exported to file: {OUTPUT_FILE_PATH}")


if __name__ == '__main__':
    main()
