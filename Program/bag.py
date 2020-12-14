"""
script containing the bag script to manage the bags
"""

import filemanager
from easygui import *

COINS = ('1p', '2p', '5p', '10p', '20p', '50p', '£1', '£2')
COIN_WEIGHTS = (356, 356, 325, 325, 250, 160, 175, 120)
COIN_AMOUNTS = (100, 50, 100, 50, 50, 20, 20, 10)
VALUES = {'1p': 0.01, '2p': 0.02, '5p': 0.05, '10p': 0.1, '20p': 0.2, '50p': 0.5, '£1': 1, '£2': 2}


# class to work with a bag so you can add one to the csv file
class Bag:
    def __init__(self, inputs):
        self.name = inputs[0]
        self.coin = inputs[1]
        self.weight = float(inputs[2])
        self.file = []

    @filemanager.writer
    def check(self):
        volunteers, attempts, percents, total = filemanager.read()
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
            return self.file
        else:
            msgbox('The bag is incorrect', 'incorrect')
            try:
                percents[vol] = (((percent / 100) * attempt) / attempt + 1) * 100
            except ZeroDivisionError:
                percents[vol] = 0
            msgbox(f'{self.weight // COIN_WEIGHTS[ind]}, {self.weight}, {COIN_WEIGHTS[ind]}', 'test')
            if self.weight % COIN_WEIGHTS[ind] != 0:
                msgbox(
                    "That weight doesn't seem to be right for that coin. It is likely that some other coins have "
                    "been jumbled up in there so will need recounting. After it has been recounted please could you "
                    "re-enter it as the only thing that will be changed is the volunteers percentage",
                    'incorrect'
                )
                attempts[vol] = attempt + 1
                self.file = [volunteers, attempts, percents, total]
                return self.file
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
                return self.file
