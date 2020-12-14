"""This program was made for fun to remake my original coin count program with new techniques that I have learn since.
Some new features that I will be including are things like classes and decorators to improve the efficiency of the
program.
THIS IS NOW THE VERSION THAT WILL BE SUBMITTED AS THE COURSE WORK
"""

# importing the libraries
from easygui import *
from filemanager import read, new_user
from bag import Bag
from rankings import Viewer


# defining the constants
COINS = ('1p', '2p', '5p', '10p', '20p', '50p', '£1', '£2')
COIN_WEIGHTS = (356, 356, 325, 325, 250, 160, 175, 120)
COIN_AMOUNTS = (100, 50, 100, 50, 50, 20, 20, 10)
VALUES = {'1p': 0.01, '2p': 0.02, '5p': 0.05, '10p': 0.1, '20p': 0.2, '50p': 0.5, '£1': 1, '£2': 2}

# defining the variables
volunteers = []
attempts = []
percents = []
total = 0.0

'---------------------------------------------------- Main Program ----------------------------------------------------'


def main():
    global volunteers, attempts, percents, total
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
        elif option == 'view the total':
            msgbox(f'The total money collected is {str(total)}', 'total')
        elif option == 'view the volunteers':
            volunteer = Viewer(percents)
            for each in range(0, len(percents)):
                try:
                    volunteer.base[percents[each]].append([volunteers[each], attempts[each]])
                except KeyError:
                    volunteer.base[percents[each]] = [[volunteers[each], attempts[each]]]
            volunteer.percents = volunteer.sort(volunteer.percents)
            print(volunteer.base)
            for each in volunteer.base:
                swaps = True
                while swaps:
                    swaps = False
                    for log in range(0, len(volunteer.base[each][0]) - 1):
                        if volunteer.base[each][log][1] < volunteer.base[each][log + 1][1]:
                            temp = volunteer.base[each][log]
                            volunteer.base[each][log] = volunteer.base[each][log + 1]
                            volunteer.base[each][log + 1] = temp
                            swaps = True
            volunteer.btw = buttonbox('How would you like to sort it?', 'sort', ['best to worst', 'worst to best'])
            textbox("Here's the ranking:", 'ranking', str(volunteer))
        elif option == 'add a volunteer':
            user = enterbox('What is the name of the user you would like to add?', 'add')
            new_user(user)
        elif option == 'stop':
            break


if __name__ == "__main__":
    main()
