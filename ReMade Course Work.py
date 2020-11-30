"""This program was made for fun to remake my original coin count program with new techniques that I have learn since.
Some new features that I will be including are things like classes to improve the efficiency of the program.
"""

# importing the libraries
import csv
import math
from easygui import *

# defining the constants
COINS = ('1p', '2p', '5p', '10p', '20p', '50p', '£1', '£2')
COIN_WEIGHTS = (356, 356, 325, 325, 250, 160, 175, 120)
COIN_AMOUNTS = (100, 50, 100, 50, 50, 20, 20, 10)
VALUES = {'1p': 0.01, '2p': 0.02, '5p': 0.05, '10p': 0.1, '20p': 0.2, '50p': 0.5, '£1': 1, '£2': 2}

'------------------------------- Setting the Read and Write Commands for General Purpose ------------------------------'


# read command for general use throughout the program to read in the csv file
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


# write command for general use throughout the program to write into the csv file
def write(file):
    col1 = file[0]
    col2 = file[1]
    col3 = file[2]
    end = str(file[3])
    text = ''
    for i in range(0, len(col1)):
        text = f'{text}{col1[i]}, {col2[i]}, {col3[i]}\n'
    text = text + end
    with open('CoinCount.txt', 'w') as doc:
        doc.write(text)


'------------------------------------------------- Add a bag commands -------------------------------------------------'


# class to work with a bag so you can add one to the csv file
class Bag:
    def __init__(self, inputs):
        self.name = inputs[0]
        self.coin = inputs[1]
        self.weight = int(inputs[2])
        self.file = []

    def check(self):
        global volunteers, attempts, percents, total
        if self.name not in volunteers:
            msgbox('That is not a registered user', 'invalid')
            return None
        ind = int(COINS.index(self.coin))
        vol = int(volunteers.index(self.name))
        percent = float(percents[vol])
        coin_weight = float(COIN_WEIGHTS[ind])
        attempt = attempts[vol]
        if self.weight == coin_weight:
            msgbox('No correcting is needed', 'correct')
            percents[vol] = ((((percent / 100) * attempt) + 1) / (attempt + 1)) * 100
            attempts[vol] = attempt + 1
            total += VALUES[self.coin] * COIN_AMOUNTS[ind]
            self.file = [volunteers, attempts, percents, total]
        else:
            msgbox('The bag is incorrect', 'incorrect')
            try:
                percents[vol] = (((percent / 100) * attempt) / attempt + 1) * 100
            except ZeroDivisionError:
                percents[vol] = 0
            if self.weight // COIN_WEIGHTS[ind] != 0:
                msgbox(
                    "That weight doesn't seem to be right for that coin. It is likely that some other coins have "
                    "been jumbled up in there so will need recounting. After it has been recounted please could you "
                    "re-enter it as the only thing that will be changed is the volunteers percentage",
                    'incorrect'
                )
                attempts[vol] = attempt + 1
                self.file = [volunteers, attempts, percents, total]
            else:
                single_coin = float(COIN_WEIGHTS[ind] / COIN_AMOUNTS[ind])
                i = 0
                if self.weight < COIN_WEIGHTS[ind]:
                    while self.weight < COIN_WEIGHTS[ind]:
                        self.weight = float(self.weight + single_coin)
                        i += 1
                    i = '+' + str(i)
                else:
                    while self.weight < COIN_WEIGHTS[ind]:
                        self.weight = float(self.weight - single_coin)
                        i -= 1
                    i = '+' + str(i)
                msgbox(f'You need to {i} coins', 'change')
                attempts[vol] = attempt + 1
                total += VALUES[self.coin] * COIN_AMOUNTS[ind]
                self.file = [volunteers, attempts, percents, total]


'-------------------------------------------- View the Volunteers Commands --------------------------------------------'


# command to sort the volunteers
def sort(arr):
    if len(arr) == 1:
        return arr
    else:
        mid = math.ceil(len(arr) / 2)
        l = arr[:mid]
        r = arr[mid:]
        l = sort(l)
        r = sort(r)
        i = j = k = 0
        while i != len(l) and j != len(r):
            if l[i] < r[j]:
                arr[k] = l[i]
                i += 1
            else:
                arr[k] = r[j]
                j += 1
            k += 1
        while i != len(l):
            arr[k] = l[i]
            i += 1
            k += 1
        while j != len(r):
            arr[k] = r[j]
            j += 1
            k += 1
        return arr


# command to view the volunteers
def view():
    global volunteers, attempts, percents, total
    base = {}
    for i in range(0, len(percents)):
        try:
            base[percents[i]].append([volunteers[i], attempts[i]])
        except KeyError:
            base[percents[i]] = [[volunteers[i], attempts[i]]]
    sort(percents)
    btw = buttonbox('How would you like to sort it?', 'sort', ['best to worst', 'worst to best'])
    rank = ''
    if btw == 'best to worst':
        for i in range(0, len(percents)):
            rank = rank + f'{str(i + 1)}. {base[percents[i]][0][0]} has had a  {str(percents[i])}% success rate with ' \
                          f'{base[percents[i]][0][1]} attempts\n'
            del base[percents[i]][0]
    elif btw == 'worst to best':
        for i in range(len(percents) - 1, -1, -1):
            rank = rank + f'{str(i + 1)}. {base[percents[i]][0][0]} has had a  {str(percents[i])}% success rate with ' \
                          f'{base[percents[i]][0][1]} attempts\n'
            del base[percents[i]][0]
    textbox("Here's the ranking:", 'ranking', rank)


'--------------------------------------------- Adding a Volunteer Commands --------------------------------------------'


# command to add a volunteer to the csv file
def new_user():
    global volunteers, attempts, percents, total
    user = enterbox('What is the name of the user you would like to add?', 'add')
    volunteers.append(user)
    attempts.append(0)
    percents.append(0.0)
    file = [volunteers, attempts, percents, total]
    write(file)


'---------------------------------------------------- Main Program ----------------------------------------------------'


while True:
    volunteers, attempts, percents, total = read()
    option = buttonbox(
        'What do you want to do?',
        'Options',
        ['add a bag', 'view the total', 'view the volunteers', 'add a volunteer', 'stop']
    )
    if option == 'add a bag':
        entry = multenterbox('Please fill in the info:', 'entry', ['Volunteers Name', 'Coin', 'Weight'])
        if entry is not None:
            bag = Bag(entry)
        else:
            continue
        bag.check()
        if bag.file:
            write(bag.file)
    elif option == 'view the total':
        msgbox(f'The total money collected is {str(total)}', 'total')
    elif option == 'view the volunteers':
        view()
    elif option == 'add a volunteer':
        new_user()
    elif option == 'stop':
        break
