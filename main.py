import os
import csv
from concurrent.futures import ThreadPoolExecutor
from scholarly import scholarly

def fetch_publications(scholar_id):
    """Fetch publications for a given Scholar ID."""
    try:
        author = scholarly.search_author_id(scholar_id)
        author = scholarly.fill(author)  # Fetch author details
        publications = []

        for pub in author['publications']:
            # Extract basic publication info
            title = pub.get('bib', {}).get('title', 'N/A')
            year = pub.get('bib', {}).get('pub_year', 'N/A')
            citation_count = pub.get('num_citations', 0)

            publications.append({
                'title': title,
                'year': year,
                'citation_count': citation_count
            })

        return publications

    except Exception as e:
        print(f"Error fetching data for Scholar ID {scholar_id}: {e}")
        return None


def save_to_csv(publications, name, department):
    """Save publications to a CSV file in department-based folder."""
    folder_path = os.path.join("Generated", department)
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, f"{name}.csv")

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Year", "Citation Count"])  # Header
        for pub in publications:
            writer.writerow([pub['title'], pub['year'], pub['citation_count']])

    print(f"File saved: {file_path}")


def process_faculty(faculty):
    """Process a single faculty member."""
    number, name, scholar_id, department = faculty
    print(f"Processing: {name} (Scholar ID: {scholar_id}, Department: {department})")
    publications = fetch_publications(scholar_id)
    if publications:
        save_to_csv(publications, name, department)


def main():
    input_file = "faculty.csv"  # Input file containing faculty data

    # Read faculty details from the CSV file
    faculty_list = []
    with open(input_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            faculty_list.append(row)

    # Process faculty members in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(process_faculty, faculty_list)


if __name__ == "__main__":
    main()
