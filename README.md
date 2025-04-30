# Inventory Digestion Exercise

The exercise is divided to two main pieces:

1.    Inventory data extraction and transformation - written in Python (see `integration-exercise.py` as entry point)
2.    Inventory data storage and validation API - written in Ruby on Rails

## Note

1. Rather than using pandas/numpy, use Python's builtin packages.
2. The `.py` script uses `csv.reader`, you should probably switch it to `DictReader`.

## Extraction and Transformation
1.  ✅ Make a GET request to Amazon S3 with the details from the python script and save the
    content into a file locally: https://docs.aws.amazon.com/AmazonS3/latest/userguide/RESTAPI.html
2.  ✅ The script outputs the content to the console, change it so that the output
    will be written to a CSV file.
3.  ✅ Add a department column to the export, there's a column in the import that
    contains that information.
4.  ✅ If the UPC column contains something other than a string of numbers at a
    length that is greater than 5, we'd want to instead, leave that column blank
    in the export, and populate a column called "internal_id" that will contain
    the ID of the record from the original file prefixed by "biz_id_".
5.  ✅ Increase the price by 7% if the original has more than 30% margin over the
    cost, otherwise increase the price by 9%. Round the final result to the 2nd
    decimal point.
6.  ✅ Add a name column to the output that is a concatenation of the item and
    itemextra columns
7.  ✅ The output should only contain item that were sold during 2020
8.  ✅ Add a properties column to the output that will contain a JSON of a dict
    containing the department, vendor and description
9.  Add a tags field to the output that will contain the following tags:
    * ✅ `duplicate_sku` if the input file contains the same ItemNum for multiple rows.
    * `high_margin` if the margin on the item is more than 30%
    * `low_margin` if the margin on the item is less than 30%
10. ✅ Instead of saving the file locally and then parsing it, add another flow to the script that passes the downloaded content directly to the CSV parser.

## Storage and Validation API

1. ✅ Create a new Ruby on Rails API project that uses the `Mongoid` gem as the ORM module instead of `ActiveRecord`
2. ✅ The app should have a single model in it - the `InventoryUnit` model that represent a single row of inventory data along with information that will be relevant for record keeping: 
    * Creation time of the record
    * Batch identifier that is shared between all items created as part of the same API call
3. ✅ Expose two endpoints:
    * `POST inventory_uploads.json` that receives a parsed JSON from the python code and creates InventoryUnits from it
    * `GET inventory_uploads.json` that will return a JSON where each element is has:
        * `batch_id` the shared ID between all the inventory units created by the same API call
        * `number_of_units` the total number of units in that batch
        * `average_price` the average price of the units
        * `total_quantity` the sum of all quantities across the inventory units in that batch
4. Update the python code such that it receives one of 3 inputs: 
    * ✅ `generate_csv` will generate the CSV file with the parsed data
    * ✅ `upload` will upload the parsed data as a JSON array to the API
    * ✅ `list_uploads` will call the inventory_uploads listing endpoint and print the result

## Running the Application

### Using Docker Compose

1. Make sure you have Docker and Docker Compose installed on your system
2. Start the services:
   ```bash
   docker compose up -d
   ```
   This will start:
   - MongoDB database
   - Rails API server (accessible at http://localhost:3000)

### Running the Python Script

The Python script can be run with different commands depending on what you want to do:

1. Generate a CSV file with the processed data:
   ```bash
   python inventory-processing-py/integration-exercise.py --generate_csv
   ```

2. Upload the processed data to the API:
   ```bash
   python inventory-processing-py/integration-exercise.py --generate_csv --upload
   ```

3. List all inventory uploads:
   ```bash
   python inventory-processing-py/integration-exercise.py --list_uploads
   ```

Note: Make sure the Rails API server is running (via Docker Compose) when using the `--upload` or `--list_uploads` commands.

### Environment Variables

You can customize the behavior of the Python script by setting these environment variables:
- `STORAGE_API_URL`: The URL of the Rails API (default: http://localhost:3000)
- `SOURCE_URL`: The URL of the source HTML file (default: https://bitbucket.org/cityhive/jobs/src/master/integration-eng/integration-entryfile.html)
- `PROCESSED_FILE_PATH`: Path where the processed CSV will be saved (default: processed_inventory.csv)
- `SAVE_SOURCE_DATA`: Set to 'true' to save the raw stream from S3 to a file (default: false)
- `SOURCE_DATA_PATH`: Path where the raw stream will be saved if SAVE_RAW_STREAM is true (default: raw_inventory.csv)

Example usage:
```bash
export SAVE_SOURCE_DATA=true
export SOURCE_DATA_PATH=my_raw_data.csv
python inventory-processing-py/integration-exercise.py --generate_csv
```

## Constraints
This project was timeboxed to ~2 days.


## Potential Improvements

### Python Application

1. **Data Processing Optimization**
   - Reduce the number of times the source data is read by implementing a single-pass processing approach
   - Implement streaming processing for large datasets to reduce memory usage
   - Use generators and iterators for more efficient data handling
   - Cache intermediate results when possible to avoid redundant calculations

2. **Code Structure and Abstraction**
   - Create dedicated classes for data transformation and validation
   - Implement a proper data pipeline pattern with clear separation of concerns
   - Add type hints and docstrings for better code maintainability
   - Create reusable components for common operations (e.g., price calculations, data validation)

3. **Error Handling and Logging**
   - Implement comprehensive error handling for network requests and file operations
   - Add detailed logging for debugging and monitoring
   - Create custom exceptions for specific error cases
   - Add retry mechanisms for network operations

4. **Testing and Quality**
   - Add unit tests for data transformation logic
   - Implement integration tests for API interactions
   - Add performance benchmarks for data processing
   - Include code coverage reporting

### Ruby on Rails Application

1. **Code Organization**
   - Implement service objects for business logic
   - Use form objects for data validation
   - Create dedicated serializers for API responses
   - Implement proper error handling with custom error classes

2. **Performance Optimization**
   - Add database indexes for frequently queried fields
   - Implement caching for frequently accessed data
   - Use batch processing for large data imports
   - Optimize MongoDB queries with proper indexing
   - Optimize order of model fields for faster queries

3. **API Enhancements**
   - Add pagination for the inventory uploads listing
   - Implement filtering and sorting capabilities
   - Add versioning to the API
   - Include more detailed statistics in the response

4. **Testing and Documentation**
   - Add comprehensive test coverage
   - Implement API documentation using tools like Swagger/OpenAPI
   - Add performance tests
   - Include examples in the documentation

5. **Monitoring and Maintenance**
   - Add health check endpoints
   - Implement proper logging and monitoring
   - Add metrics collection for performance tracking
   - Create maintenance tasks for data cleanup

These improvements would enhance the maintainability, performance, and reliability of both applications while making them more production-ready.

