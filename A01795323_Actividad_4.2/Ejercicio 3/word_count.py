"""This script identifies the distinct words from a file and the frequency of them"""

import sys
import time

FILE_SOURCE_DIR = "p3"
OUTPUT_FILE_PATH = "../output/WordCountResults.txt"


def get_words_from_file(file_name):
    """Opens a given file name to process the data and extract words."""
    words = []
    file_path = '/'.join((FILE_SOURCE_DIR, file_name))
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            print(f"Collecting words from file {file_name}")
            for line in file:
                words.extend(process_line(line))
    except FileNotFoundError:
        print(f"File {file_name} not found at {FILE_SOURCE_DIR} directory")
        sys.exit(1)
    print("\nCollecting words from file process has finished")
    return words


def process_line(line):
    """Processes a line to extract words, removing non-alphabetic characters."""
    processed_line = "".join(c.lower() if c.isalnum() or c.isspace() else " " for c in line)
    return processed_line.split()


def compute_word_frequencies(words):
    """Computes the frequency of each distinct word."""
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def get_file_name_from_params():
    """Retrieves the file name from command-line arguments."""
    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)
    return sys.argv[1]


def create_file_with_word_counts(output_filename, word_counts, elapsed_time):
    """Writes the computed word frequencies to a file."""
    output_file = '/'.join((FILE_SOURCE_DIR, output_filename))
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(":: Word Frequency Results ::\n\n")
        for word, count in sorted(word_counts.items()):
            file.write(f"{word}: {count}\n")
        file.write(f"\nElapsed Time: {elapsed_time:.8f} seconds\n")


def main():
    """Main function to orchestrate reading, computation, and output of word counts."""
    start_time = time.time()
    file_name = get_file_name_from_params()
    words = get_words_from_file(file_name)
    if not words:
        print("Error: No valid words found in the file.")
        sys.exit(1)
    print("\nStarting word frequency calculations\n")
    word_counts = compute_word_frequencies(words)
    elapsed_time = time.time() - start_time
    print(":: Word Frequency Results ::\n")
    for word, count in sorted(word_counts.items()):
        print(f"{word}: {count}")
    print(f"\nElapsed Time: {elapsed_time:.8f} seconds")
    create_file_with_word_counts(OUTPUT_FILE_PATH, word_counts, elapsed_time)
    print(f"\nWord frequency results exported to file: {OUTPUT_FILE_PATH}")


if __name__ == "__main__":
    main()
