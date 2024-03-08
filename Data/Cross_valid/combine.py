import csv
column_names = ['path', 'filename', 'NC', 'MCI', 'DE', 'COG', 'AD', 'PD', 'FTD', 'VD', 'DLB', 'PDD', 'ADD', 'ALL', 'OTHER']

def read_csv_dict(content, csv_table):
    with open(csv_table, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            content.append(row)

content = []
csv_path = '../dataset_data/ADNI1.csv'
read_csv_dict(content, csv_path)

with open('all.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(column_names)
    for row in content:
        if row['NC'] == '1':
            row['ALL'] = '0'
        elif row['MCI'] == '1':
            row['ALL'] = '1'
        elif row['AD'] == '1':
            row['ALL'] = '2'
        elif row['ADD'] == '0':
            row['ALL'] = '3'
        spamwriter.writerow([row[col_name] if col_name in row else '' for col_name in column_names])