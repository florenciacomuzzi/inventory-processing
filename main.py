# 1. Using requests or any other HTTP library, grab the file HTML from: https://bitbucket.org/cityhive/jobs/src/master/integration-eng/integration-entryfile.html
# 2. Then, parse the URL for the csv file located in the S3 bucket (as part of the script, not by hand)
# 3. Make a GET request to Amazon's S3 with the details from #2 and save the to `local_file_path`
from inventory_processing.file_utils import remove_line, remove_empty_lines, remove_nontable_lines
from inventory_processing.inventory import process_inventory, dict_read_csv
from inventory_processing.object_utils import extract_inventory_object_details
from inventory_processing.s3_helper import S3Helper

initial_html_file = 'https://bitbucket.org/cityhive/jobs/src/master/integration-eng/integration-entryfile.html'
local_file_path = 'inventory_export.csv'
output_file_path = 'processed_inventory.csv'


if __name__ == '__main__':
    s3_details = extract_inventory_object_details(initial_html_file)
    bucket = S3Helper(s3_details['bucket'], s3_details['region_code'])
    bucket.download_key_with_presigned_url(
        s3_details['object_path'], local_file_path)

    # TODO optimize
    remove_line(local_file_path, [2])  # Remove the separator line
    remove_empty_lines(local_file_path)
    remove_nontable_lines(local_file_path)

    rows = dict_read_csv(local_file_path)

    process_inventory(rows, output_file_path)

    print("Finished!")