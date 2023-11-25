import csv
import requests
from difflib import get_close_matches

# Specify the cleaned CSV file and output verified CSV file
cleaned_csv_file = 'cleaned_output.csv'
verified_csv_file = 'verified_output.csv'

# Function to verify book title and author using the Open Library API
def verify_with_open_library(title, author):
    api_url = f'http://openlibrary.org/search.json?title={title}&author={author}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data.get('num_found', 0) > 0:
            # Get details of the first matching book
            first_book = data['docs'][0]
            corrected_title = first_book.get('title', title)
            corrected_author = first_book.get('author_name', [author])[0]
            return corrected_title, corrected_author
    return None, None

# Function to get ISBN based on verified title
def get_isbn(title):
    api_url = f'http://openlibrary.org/search.json?title={title}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data.get('num_found', 0) > 0:
            # Get details of the first matching book
            first_book = data['docs'][0]
            identifiers = first_book.get('isbn', [])
            return identifiers[0] if identifiers else "ISBN Not Found"
    return "ISBN Not Found"

# Read the cleaned CSV file and verify titles and authors
with open(cleaned_csv_file, 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    
    # Open the verified CSV file for writing
    with open(verified_csv_file, 'w', newline='', encoding='utf-8') as verified_csv:
        field_names = ["JSON_file", "title", "author", "title_verified", "author_verified", "isbn"]
        writer = csv.DictWriter(verified_csv, fieldnames=field_names)
        writer.writeheader()

        for row in reader:
            json_file = row["JSON_file"]
            title = row["title"]
            author = row["author"]
            
            # Verify the title and author using the Open Library API
            corrected_title, corrected_author = verify_with_open_library(title, author)
            
            # If no match is found, use difflib to get the closest matches
            if corrected_title is None:
                closest_titles = get_close_matches(title, [book.strip() for book in row["title"].split(",")])
                corrected_title = closest_titles[0] if closest_titles else "Not Found"
            
            if corrected_author is None:
                closest_authors = get_close_matches(author, [author.strip() for author in row["author"].split(",")])
                corrected_author = closest_authors[0] if closest_authors else "Not Found"
            
            # Get ISBN based on the verified title
            isbn = get_isbn(corrected_title)
            
            # Write the verified data to the output CSV file
            writer.writerow({
                "JSON_file": json_file,
                "title": title,
                "author": author,
                "title_verified": corrected_title,
                "author_verified": corrected_author,
                "isbn": isbn
            })

print("Verified CSV file creation completed.")
