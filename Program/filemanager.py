"""
Script containing functions that are used to write to the files
"""

import csv


def writer(func):
    def wrapper(*args, **kwargs):
        col1, col2, col3, end = func(*args, **kwargs)
        text = ''
        for i in range(0, len(col1)):
            text = f'{text}{col1[i]}, {col2[i]}, {col3[i]}\n'
        text = text + str(end)
        with open('CoinCount.txt', 'w') as doc:
            doc.write(text)

    return wrapper


def read():
    col1 = []
    col2 = []
    col3 = []
    with open('CoinCount.txt', 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            try:
                end = float(row[0])
                break
            except ValueError:
                pass
            col1.append(row[0])
            col2.append(int(row[1]))
            col3.append(float(row[2]))
    return col1, col2, col3, end


@writer
def new_user(volunt):
    volunteers, attempts, percents, total = read()
    volunteers.append(volunt)
    attempts.append(0)
    percents.append(0.0)
    file = [volunteers, attempts, percents, total]
    return file
