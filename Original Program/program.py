import csv
import math
from easygui import *

COINS = ('1p', '2p', '5p', '10p', '20p', '50p', '£1', '£2')
COIN_WEIGHTS = (356, 356, 325, 325, 250, 160, 175, 120)
COIN_AMOUNTS = (100, 50, 100, 50, 50, 20, 20, 10)
VALUES = {'1p': 0.01, '2p': 0.02, '5p': 0.05, '10p': 0.1, '20p': 0.2, '50p': 0.5, '£1': 1, '£2': 2}


def read():
    volunteers = []
    attempts = []
    percents = []
    with open('CoinCount.txt', 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            try:
                total = float(row[0])
                break
            except ValueError:
                pass
            volunteers.append(row[0])
            attempts.append(int(row[1]))
            percents.append(float(row[2]))
    return total, volunteers, attempts, percents


def sort(numbers):
    if len(numbers) == 1:
        return numbers
    else:
        mid = math.ceil(len(numbers) / 2)
        l = numbers[:mid]
        r = numbers[mid:]
        l = sort(l)
        r = sort(r)
        i = j = k = 0
        while i < len(l) and j < len(r):
            if l[i] > r[j]:
                numbers[k] = l[i]
                i += 1
            else:
                numbers[k] = r[j]
                j += 1
            k += 1
        while i < len(l):
            numbers[k] = l[i]
            i += 1
            k += 1
        while j < len(r):
            numbers[k] = r[j]
            j += 1
            k += 1
        return numbers


def add():
    array = multenterbox('Please fill in the info:', 'entry', ['Volunteers Name', 'Coin', 'Weight'])
    if array is None:
        return None
    volunteer = array[0]
    coin_type = array[1]
    weight = int(array[2])
    total, volunteers, attempts, percents = read()
    if volunteer in volunteers:
        pass
    else:
        msgbox('That is not a registered user', 'invalid')
        return None
    ind = int(COINS.index(coin_type))
    vol = int(volunteers.index(volunteer))
    percent = float(percents[vol])
    cWeight = float(COIN_WEIGHTS[ind])
    attempt = attempts[vol]
    if weight == cWeight:
        msgbox('No correcting is needed', 'correct')
        percents[vol] = ((((percent / 100) * attempt) + 1) / (attempt + 1)) * 100
        attempts[vol] = attempt + 1
        total += VALUES[coin_type] * COIN_AMOUNTS[ind]
        write(volunteers, attempts, percents, total)
    else:
        msgbox('The bag is incorrect', 'incorrect')
        try:
            percents[vol] = (((percent / 100) * attempt) / attempt + 1) * 100
        except ZeroDivisionError:
            percents[vol] = 0
        fix(ind, vol, coin_type, volunteers, attempts, percents, attempt, weight, total)


def fix(ind, vol, coinType, volunteers, attempts, percents, attempt, weight, total):
    coin_weight = float(COIN_WEIGHTS[ind] / COIN_AMOUNTS[ind])
    if weight // COIN_WEIGHTS[ind] != 0:
        msgbox(
            'That weight doesn\'t seem to be right for that coin. It is likely that some other coins have been jumbled '
            'up in there so will need recounting. After it has been recounted please could you re-enter it as the only '
            'thing that will be changed is the volunteers percentage', 'incorrect')
        attempts[vol] = attempt + 1
        write(volunteers, attempts, percents, total)
        return None
    else:
        pass
    if weight < COIN_WEIGHTS[ind]:
        i = 0
        while weight < COIN_WEIGHTS[ind]:
            weight = float(weight + coin_weight)
            i = i + 1
        i = '+' + str(i)
    elif weight > COIN_WEIGHTS[ind]:
        i = 0
        while weight > COIN_WEIGHTS[ind]:
            weight = float(weight - coin_weight)
            i = i + 1
        i = '-' + str(i)
    msgbox(f'you need to {i} coins', 'change')
    attempts[vol] = attempt + 1
    total += VALUES[coinType] * COIN_AMOUNTS[ind]
    write(volunteers, attempts, percents, total)


def write(volunteers, attempts, percents, total):
    with open('CoinCount.txt', 'w') as file:
        for i in range(0, len(volunteers)):
            file.write(f'{volunteers[i]},{str(attempts[i])},{str(percents[i])}\n')
        file.write(str(total))


def total():
    file = open('CoinCount.txt', 'r')
    csv_file = csv.reader(file, delimiter=',')
    for row in csv_file:
        try:
            total = float(row[0])
        except ValueError:
            pass
    file.close()
    msgbox(f'There has been a total of £{str(total)} collected', 'amount')


def volunt():
    total, volunteers, attempts, percents = read()
    base = {}
    for i in range(0, len(percents)):
        try:
            base[percents[i]].append([volunteers[i], attempts[i]])
        except KeyError:
            base[percents[i]] = [[volunteers[i], attempts[i]]]
    sort(percents)
    btw = buttonbox('How would you like to sort it?', 'sort', ['worst to best', 'best to worst'])
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
    textbox('Here\'s the ranking:', 'ranking', rank)


def newUser():
    total, volunteers, attempts, percents = read()
    user = enterbox('What is the name of the user you would like to add?', 'add')
    volunteers.append(user)
    attempts.append(0)
    percents.append(0.0)
    write(volunteers, attempts, percents, total)


while True:
    option = buttonbox('What do you want to do?', 'Options',
                       ['add a bag', 'view the total', 'view the volunteers', 'add a volunteer', 'stop'])
    if option == 'add a bag':
        add()
    elif option == 'view the total':
        total()
    elif option == 'view the volunteers':
        volunt()
    elif option == 'add a volunteer':
        newUser()
    elif option == 'stop':
        break
