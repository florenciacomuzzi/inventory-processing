# 1. Using requests or any other HTTP library, grab the file HTML from: https://bitbucket.org/cityhive/jobs/src/master/integration-eng/integration-entryfile.html
# 2. Then, parse the URL for the csv file located in the S3 bucket (as part of the script, not by hand)
# 3. Make a GET request to Amazon's S3 with the details from #2 and save the to `local_file_path`
import argparse
import os

from inventory_processing.api_helper import ApiHelper
from inventory_processing.file_utils import remove_line, remove_empty_lines, remove_nontable_lines
from inventory_processing.inventory import process_inventory, dict_read_csv
from inventory_processing.object_utils import extract_inventory_object_details
from inventory_processing.s3_helper import S3Helper

STORAGE_API_URL = os.environ.get('STORAGE_API_URL', 'http://localhost:3000')
SOURCE_URL = 'https://bitbucket.org/cityhive/jobs/src/master/integration-eng/integration-entryfile.html'
LOCAL_FILE = 'inventory_export.csv'
PROCESSED_FILE = 'processed_inventory.csv'

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process inventory data from S3')
    parser.add_argument('--generate_csv', 
                       action="store_true",
                       # nargs='?',
                       help='generate the CSV file with the parsed data')
    parser.add_argument('--upload', 
                       action="store_true",
                       # nargs='?',
                       help='upload the parsed data as a JSON array to the API')
    parser.add_argument('--list_uploads', 
                       action="store_true",
                       # nargs='?',
                       help='call the inventory_uploads listing endpoint and print the result')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    if args.upload and not args.generate_csv:
        raise ValueError("upload requires generate_csv")

    key_stream = None
    if args.generate_csv:
        s3_details = extract_inventory_object_details(SOURCE_URL)
        bucket = S3Helper(s3_details['bucket'], s3_details['region_code'])
        key_stream = bucket.download_key_with_presigned_url(
            s3_details['object_path'])

    if args.upload:
        # TODO optimize
        key_stream = remove_line(key_stream, [2])  # Remove the separator line
        key_stream = remove_empty_lines(key_stream)
        key_stream = remove_nontable_lines(key_stream)

        rows = dict_read_csv(key_stream)

        processed_rows = process_inventory(rows, PROCESSED_FILE)

        api_helper = ApiHelper(STORAGE_API_URL)
        api_helper.post('/inventory_units', processed_rows)

    print("Finished!")