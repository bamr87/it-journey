import csv
from collections import defaultdict

# Specify the combined CSV file and output cleaned CSV file
combined_csv_file = 'combined_output.csv'
cleaned_csv_file = 'cleaned_output.csv'

# Dictionary to store book titles and authors
book_data = defaultdict(dict)

# Read the combined CSV file and populate the book_data dictionary
with open(combined_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        json_file = row["JSON_file"]
        mention_type = row["type"]
        mention_text = row["mentionText"]
        if mention_type == "book_title":
            book_data[json_file]["title"] = mention_text
        elif mention_type == "book_author":
            book_data[json_file]["author"] = mention_text

# Write the cleaned records to the output CSV file
with open(cleaned_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    field_names = ["JSON_file", "title", "author"]
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for json_file, data in book_data.items():
        writer.writerow({"JSON_file": json_file, "title": data.get("title", ""), "author": data.get("author", "")})

print("Cleaned CSV file creation completed.")
