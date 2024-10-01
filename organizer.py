import csv
import re

def normalize_call_number(call_number):
    """
    Normalize the call number for sorting.
    Breaks down the call number into separate components for proper sorting.

    :param call_number: The call number string
    
    :returns: A tuple representing the sorted parts of the call number
    """
    parts = call_number.split()
    
    # Split the first part (letters and number)
    # First group: Letters (e.g. HM, QH)
    # Second group: Number (e.g. 538, 581.2)
    match = re.match(r"([A-Z]+)(\d+(?:\.\d+)?)", parts[0])
    
    if match:
        letter_part = match.group(1)
        number_part = float(match.group(2))
    else:
        letter_part = parts[0]
        number_part = 0

    # Handle the rest of the parts
    additional_parts = parts[1:]
    
    # Return a tuple that Python can sort naturally
    return (letter_part, number_part) + tuple(additional_parts)


def read_csv(filename):
    """
    Reads the CSV file and returns a list of tuples (barcode, call number).

    :param filename: Path to the CSV file
    
    :returns: List of tuples (barcode, call number)
    """
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        data = [(rows[0], rows[1]) for rows in reader]
    return data


def sort_books_by_call_number(data):
    """
    Sorts the books by call number using the Library of Congress classification system.

    :param data: List of tuples (barcode, call number)
    
    :returns: Sorted list by call number
    """
    return sorted(data, key=lambda x: normalize_call_number(x[1]))


def write_csv(filename, data):
    """
    Writes the sorted list to a new CSV file.

    :param filename: Path to the output CSV file
    :param data: List of tuples (barcode, call number)
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def main(input_file, output_file):
    # Read data from CSV
    books = read_csv(input_file)
    
    # Sort books by call number
    sorted_books = sort_books_by_call_number(books)
    
    # Write the sorted list to a new CSV file
    write_csv(output_file, sorted_books)


if __name__ == "__main__":
    # Example usage
    input_file = './example/zeresha.csv'  # Replace with your actual input file
    output_file = './example/sorted_books.csv'  # Output file for sorted results

    main(input_file, output_file)
