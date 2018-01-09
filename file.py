import csv

def read_from_file(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        headers = reader.next()
        for row in reader:
            item = row
            data.append(item)
    return data
