import collections
import csv
from datetime import datetime


def dict_read_csv(file, delimiter='|'):
    rows = []
    with open(file, "r") as file:
        lines = file.readlines()
        keys = lines[0].strip().split(delimiter)  # Read the header line to get keys

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

        dups_pos = []
        if len(dups) > 0:
            for key, positions in dups.items():
                dups_pos = dups_pos + positions

        dedup_keys = []
        for pos, key in enumerate(keys):
            if pos not in dups_pos:
                dedup_keys.append(key)

        for line in lines[1:]:
            values = line.strip().split(delimiter)

            dedup_values = []
            for pos, value in enumerate(values):
                if pos not in dups_pos:
                    dedup_values.append(value)

            data = dict(zip(dedup_keys, dedup_values))

            if 'Price' not in data:
                data['Price'] = None
            if 'In_Stock' not in data:
                data['In_Stock'] = None
            if 'Dept_ID' not in data:
                data['Dept_ID'] = None
            rows.append(data)
    return rows


def process_inventory(inventory_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=['upc', 'price', 'quantity', 'department_id',
                                                     'internal_id', 'name', 'properties'])
        writer.writeheader()
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

            name = row['ItemName'] + row['ItemName_Extra'] # TODO remove spaces?

            properties = {
                'department': row['Dept_ID'],
                'vendor': row['Vendor_Number'],
                'description': row['Description']
            }

            writer.writerow({
                'upc': row['ItemNum'],
                'price': price,
                'quantity': row['In_Stock'],
                'department_id': row['Dept_ID'],
                'internal_id': internal_id,
                'name': name,
                'properties': properties
            })
