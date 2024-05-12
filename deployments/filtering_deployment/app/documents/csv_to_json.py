import csv
import json

def csv_to_json(csv_file, json_file):
    # Initialize an empty list to store the JSON objects
    json_data = []

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        # Convert each row into a JSON object
        for row in reader:
            json_data.append(row)

    # Write JSON data to file
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent=4)

# Example usage:
csv_file = 'sample.csv'     # Replace with your CSV file path
json_file = 'sample.json' # Replace with desired output JSON file path
csv_to_json(csv_file, json_file)
