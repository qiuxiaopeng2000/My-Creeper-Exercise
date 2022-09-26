import csv

def tabluate(tables: list, file_name: str) -> None:
    file_name += ".csv"
    with open(file_name, 'w+', newline='') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerows(tables)