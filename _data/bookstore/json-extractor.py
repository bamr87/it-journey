import os
import json
import csv

# Specify the root folder containing subdirectories and JSON files
root_folder = 'C:\\Users\\amrab\\github\\it-journey\\_data\\bookstore\\test'
output_csv_file = 'combined_output.csv'

# Initialize a list to store the combined data
combined_data = []

# Function to extract relevant data from JSON and add to the combined_data list
def extract_data(json_path):
    with open(json_path, 'r', encoding='utf-8', errors='replace') as json_file:
        data = json.load(json_file)

    if "entities" in data and isinstance(data["entities"], list):
        entities = data["entities"]

        for entity in entities:
            if entity.get("type") == "book_title" or entity.get("type") == "book_author":
                combined_data.append({
                    "JSON_file": os.path.basename(json_path),
                    "type": entity.get("type"),
                    "mentionText": entity.get("mentionText")
                })

# Iterate through subdirectories and files
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.json'):
            json_path = os.path.join(dirpath, filename)
            extract_data(json_path)

# Prepare data for transposed CSV
transposed_data = {}
for item in combined_data:
    json_filename = item.pop("JSON_file")
    if json_filename not in transposed_data:
        transposed_data[json_filename] = []
    transposed_data[json_filename].append(item)

# Write the transposed data to the output CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    field_names = ["JSON_file", "type", "mentionText"]
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for json_filename, items in transposed_data.items():
        for item in items:
            item["JSON_file"] = json_filename
            writer.writerow(item)

print("Combined and transposed CSV file creation completed.")
