"""This program calculates the total sales from a list in json format."""

import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE_PATH = os.path.join(BASE_DIR, "SalesResults.txt")


def get_prices_from_file(file_path):
    """Get list of prices from a file in json format."""
    file_content = read_json_file(file_path)
    return convert_json_to_dict(file_content, "title")


def read_json_file(file_path):
    """Reads a file in json format."""
    try:
        with open(file_path, 'r', encoding="UTF-8") as json_file:
            return json.load(json_file)
    except ValueError:
        print(f"Decoding JSON file {file_path} has failed")
        sys.exit(1)


def convert_json_to_dict(json_content, key):
    """Converts a json object to a dictionary."""
    response = {}
    for row in json_content:
        dict_key = row[key]
        response[dict_key] = row
    return response


def get_file_path(filename):
    """Gets the file path of the provided file name."""
    main_directory = "data_source"
    path = ""
    if not filename:
        print("File name was not provided")
        sys.exit(1)
    if "TC1" in filename:
        path = f"{main_directory}/TC1/{filename}"
    elif "TC2" in filename:
        path = f"{main_directory}/TC2/{filename}"
    elif "TC3" in filename:
        path = f"{main_directory}/TC3/{filename}"
    return path


def read_filename_from_params(index):
    """Reads a file name by index from the command-line arguments."""
    if len(sys.argv) != 3:
        print("Invalid program call"
              "\nExample of usage: "
              "python compute_sales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)
    return sys.argv[index]


def get_total_cost(prices, sales):
    """Calculates the total cost of sales"""
    total = 0
    print("::Details of sales::\n")
    for sale in sales:
        qty = process_qty(validate_field(sale, "Quantity"))
        product = validate_field(sale, "Product")
        price_record = validate_field(prices, product)
        price = process_price(validate_field(price_record, "price"))
        if qty and product and price:
            print(f"Compute Qty: {qty} of product: \"{product}\" "
                  f"at price: ${price}")
            total += (qty * price)
        else:
            print(f"Invalid record: Qty = {qty}, Price = {price}, "
                  f"Product: {product}")
    print("\n")
    return total


def process_qty(qty):
    """Returns a valid quantity of int type"""
    if not qty:
        return False
    return int(qty)


def process_price(price):
    """Returns a valid price of float type"""
    if not price:
        return False
    return float(price)


def create_file_with_results(filename, results):
    """Writes the results to a file."""
    try:
        with open(filename, 'w', encoding="UTF-8") as file:
            file.write(results)
    except (FileNotFoundError, PermissionError, OSError):
        print("Error create the results file")
        sys.exit(1)


def validate_field(obj, field_name):
    """Validates that a dictionary contains a given key"""
    if not obj:
        print("Error: Dictionary provided doesn't exist")
        return False
    if field_name in obj:
        return obj[field_name]

    print(f"Error: {field_name} not found in Dictionary")
    return False


def main():
    """Main method to orchestrate reading, calculation and output of sales"""
    start_time = time.time()
    prices_file_name = read_filename_from_params(1)
    sales_file_name = read_filename_from_params(2)
    prices = get_prices_from_file(get_file_path(prices_file_name))
    sales = read_json_file(get_file_path(sales_file_name))
    total_cost = get_total_cost(prices, sales)
    elapsed_time = time.time() - start_time
    sales_results = (f"Total cost for all sales: ${total_cost:.2f}"
                     f"\nElapsed Time: {elapsed_time:.8f} seconds")

    print(sales_results)
    create_file_with_results(OUTPUT_FILE_PATH, sales_results)
    print(f"Results exported to file {OUTPUT_FILE_PATH}")


if __name__ == '__main__':
    main()
