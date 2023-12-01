import csv
import sys

# Usage: python3 survey_cleaning.py <filename.csv>
# Some help provided by Codeium

# Get the filename from the command line argument
filename = sys.argv[1]

# Remove start and end quotes from a string
def remove_quotes(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s

# Clean and rename the columns
def clean_row(row):
    for i in range(len(row)):
        row[i] = remove_quotes(row[i])
    row[6] = row[6].replace(" House", "")
    return row

# Read the CSV file and clean the rows
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)
    rows = [clean_row(row) for row in reader]

# Rename the columns
header = rows[0]
header[1] = "Concentration 1"
header[2] = "Concentration 2"
header[5] = "Year"

# Write the cleaned rows to a new CSV file
output_filename = f"{filename.split('.')[0]}_cleaned.csv"
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows[1:])