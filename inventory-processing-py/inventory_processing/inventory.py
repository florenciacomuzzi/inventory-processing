import collections
import csv
from datetime import datetime
from io import StringIO
from typing import Union, TextIO
import requests


def dict_read_csv(stream: Union[str, TextIO, StringIO, requests.Response], delimiter='|'):
    """
    Read CSV data from a stream and return as a list of dictionaries.
    
    Args:
        stream: Input stream (file path, TextIO, StringIO, or requests.Response)
        delimiter: Character used to separate fields in the CSV

    Returns:
        list: List of dictionaries containing the CSV data
    """
    rows = []
    
    # Handle different types of input
    if isinstance(stream, str):
        # If it's a string, treat it as a file path
        with open(stream, "r") as file:
            lines = file.readlines()
    elif isinstance(stream, requests.Response):
        # If it's a Response object, decode the content
        lines = stream.content.decode('utf-8').splitlines(keepends=True)
    else:
        # For TextIO and StringIO, use readlines
        lines = stream.readlines()

    # Process the header line
    keys = lines[0].strip().split(delimiter)

    # Handle duplicate keys
    key_counts = {}
    dups = {}
    for pos in range(len(keys)):
        key = keys[pos]
        if key in key_counts:
            if key in dups:
                dups[key].append(pos)
            else:
                dups[key] = [pos]
            key_counts[key] += 1
        else:
            key_counts[key] = 1

    # Collect positions of duplicate keys
    dups_pos = []
    if len(dups) > 0:
        for key, positions in dups.items():
            dups_pos = dups_pos + positions

    # Create list of deduplicated keys
    dedup_keys = []
    for pos, key in enumerate(keys):
        if pos not in dups_pos:
            dedup_keys.append(key)

    # Process each data line
    for line in lines[1:]:
        values = line.strip().split(delimiter)

        # Filter out values corresponding to duplicate keys
        dedup_values = []
        for pos, value in enumerate(values):
            if pos not in dups_pos:
                dedup_values.append(value)

        # Create dictionary for this row
        data = dict(zip(dedup_keys, dedup_values))

        # Ensure required fields exist
        if 'Price' not in data:
            data['Price'] = None
        if 'In_Stock' not in data:
            data['In_Stock'] = None
        if 'Dept_ID' not in data:
            data['Dept_ID'] = None

        rows.append(data)

    return rows


def process_inventory(inventory_data, output_file):
    """Process inventory data according to business logic.

    Args:
        inventory_data (list): List of dictionaries containing inventory data.
        output_file (str): Path to the output file.

    Returns:
        list: List of processed inventory data.
    """
    # Track ItemNum occurrences
    item_num_counts = collections.defaultdict(int)
    for row in inventory_data:
        item_num_counts[row['ItemNum']] += 1

    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['upc', 'price', 'quantity', 'department_id',
                                                     'internal_id', 'name', 'properties', 'tags'])
        writer.writeheader()
        new_rows = []
        for row in inventory_data:
            # The output should only contain item that were sold during 2020
            # TODO which column to use?
            dt = datetime.strptime(row['Date_Created'], "%Y-%m-%d %H:%M:%S.%f")
            if dt.year != 2020:
                continue

            if len(row['ItemNum']) > 5 and row['ItemNum'].isdigit():
                internal_id = None
            else:
                internal_id = f"biz_id_{row['ItemNum']}"

            # WARNING changes type
            price = float(row['Price'])
            cost = float(row['Cost'])
            if cost != 0:
                markup = ((price - cost) / cost) * 100
                if markup > 30:
                    price = round(price * 1.07, 2)
                else:
                    price = round(price * 1.09, 2)
            else:
                price = round(price, 2)
                markup = 0  # Set markup to 0 when cost is 0

            name = row['ItemName'] + row['ItemName_Extra'] # TODO remove spaces?

            # Clean up properties
            properties = {
                'department': row['Dept_ID'] if row['Dept_ID'] != 'NONE' else None,
                'vendor': row['Vendor_Number'] if row['Vendor_Number'] != 'NONE' else None,
                'description': row['Description'] if row['Description'] != 'NULL' else None
            }

            quantity = 0
            in_stock = row['In_Stock']
            in_stock = float(in_stock)
            in_stock = int(in_stock)
            if in_stock > 0:
                quantity = in_stock

            # Clean up department_id
            department_id = row['Dept_ID'] if row['Dept_ID'] != 'NONE' else None

            # Clean up internal_id
            if internal_id and internal_id.startswith('biz_id_'):
                internal_id = internal_id.replace('biz_id_', '')

            # Add tags based on conditions
            tags = []
            if item_num_counts[row['ItemNum']] > 1:
                tags.append('duplicate_sku')
            if markup > 30:
                tags.append('high_margin')
            elif markup < 30 and cost != 0:  # Only add low_margin if we have a valid cost
                tags.append('low_margin')

            # Ensure data types match Mongoid's expectations
            new_row = {
                'upc': str(row['ItemNum']),  # String
                'price': float(price),  # BigDecimal
                'quantity': int(quantity),  # Integer
                'department_id': str(department_id) if department_id else None,  # String
                'internal_id': str(internal_id) if internal_id else None,  # String
                'name': str(name),  # String
                'properties': properties,  # Object
                'tags': tags,  # Array
            }

            new_rows.append(new_row)

            writer.writerow(new_row)

    return new_rows
