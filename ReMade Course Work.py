"""This program was made for fun to remake my original coin count program with new techniques that I have learn since.
Some new features that I will be including are things like classes to improve the efficiency of the program.
"""

# importing the libraries
import csv
import math
from easygui import *


class Case:
    def __init__(self, volunt, coin, weight):
        self.volunteer = volunt
        self.coin = coin
        self.weight = weight
        self.COINS = ('1p', '2p', '5p', '10p', '20p', '50p', '£1', '£2')
        self.COIN_WEIGHT = (356, 356, 325, 325, 250, 160, 175, 120)
        self.COIN_AMOUNT = (100, 50, 100, 50, 50, 20, 20, 10)
        self.VALUES = {'1p': 0.01, '2p': 0.02, '5p': 0.05, '10p': 0.1, '20p': 0.2, '50p': 0.5, '£1': 1, '£2': 2}
        self.total = 0
        self.volunteers = []
        self.attempts = []
        self.percents = []
        self.ind = 0
        self.vol = 0
        self.percent = 0
        self.coin_weight = 0
        self.attempt = 0

    def add(self):
        self.total, self.volunteers, self.attempts, self.percents = read()
        if self.volunteer not in self.volunteers:
            msgbox('That is not a registered user', 'invalid')
            return None
        self.ind = int(self.COINS.index(self.coin))
        self.vol = int(self.volunteers.index(self.volunteer))
        self.percent = float(self.percents[self.vol])
        self.coin_weight = float(self.COIN_WEIGHT[self.ind])
        self.attempt = self.attempts[self.vol]
        if self.weight == self.coin_weight:
            msgbox('No correcting is needed', 'Correct')
            self.percents[self.vol] = ((((self.percent / 100) * self.attempt) + 1) / (self.attempt + 1)) * 100
            self.attempts[self.vol] = self.attempt + 1
            self.total = self.VALUES[self.coin] * self.COIN_AMOUNT[self.ind]
            return 'ready'
        else:
            msgbox('The bag is incorrect', 'Incorrect')
            try:
                self.percents[self.vol] = ((((self.percent / 100) * self.attempt) + 1) / self.attempt) * 100
            except ZeroDivisionError:
                self.percents[self.vol] = 0
            return 'fix'

    def fix(self):
        if self.weight // self.coin_weight != 0:
            msgbox(
                'That weight doesn\'t seem to be right for that coin. It is likely that some other coins have been '
                'jumbled up in there so will need recounting. After it has been recounted please could you re-enter it'
                'as the only thing that will be changed is the volunteers percentage',
                'incorrect'
            )


def read():
    volunt = []
    attmpt = []
    percnt = []
    with open('CoinCount.txt', 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            try:
                total = float(row[0])
                break
            except ValueError:
                pass
            volunt.append(row[0])
            attmpt.append(int(row[1]))
            percnt.append(float(row[2]))
    return total, volunt, attmpt, percnt


def write(volunteers, attempts, percents, total):
    with open('CoinCount.txt', 'w') as file:
        for i in range(0, len(volunteers)):
            file.write(f'{volunteers[i]},{str(attempts[i])},{str(percents[i])}\n')
        file.write(str(total))


while True:
    option = buttonbox('What do you want to do?',
                       'Options',
                       ['add a bag', 'view the total', 'view the volunteers', 'add a volunteer', 'stop'])
    if option == 'add a bag':
        array = multenterbox('Please fill in the info:', 'entry', ['Volunteers Name', 'Coin', 'Weight'])
        if array is None:
            msgbox('Please enter something', 'No input')
            continue
        volunteer = array[0]
        coin = array[1]
        weight = array[2]
        current_case = Case(volunteer, coin, weight)
        ready = current_case.add()
        if ready == 'ready':
            write(current_case.volunteers, current_case.attempts, current_case.percents, current_case.total)
        elif ready == 'fix':
            pass
