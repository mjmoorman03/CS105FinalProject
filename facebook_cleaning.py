import csv
import sys

# Get the filename from the command line argument
filename = sys.argv[1]

# Clean and split the concentrations
def clean_concentrations(row):
    concentrations = row[4].split(';')
    row[4] = concentrations[0].strip()
    if len(concentrations) > 1:
        row.append(concentrations[1].strip())
    else:
        row.append('')
    return row

# Read the CSV file and clean the rows
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    rows = [clean_concentrations(row) for row in reader]

# Rename the columns
header = rows[0]
header[5] = 'Concentration 2'
header[4] = 'Concentration 1'

# Write the cleaned rows to a new CSV file
output_filename = f"{filename.split('.')[0]}_cleaned.csv"
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows[1:])