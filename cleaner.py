import csv

def to_csv(from_path: str, to_path: str) -> None:
    with open(from_path, 'r') as txt_file:
        next(txt_file)
        columns = txt_file.readline().split()
        next(txt_file)
        with open(to_path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(columns)
            while next(txt_file, "EOF") != "EOF":
                csv_writer.writerow(txt_file.readline().split())