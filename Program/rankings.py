"""
Script containing the volunteer class to view volunteers
"""

import math


class Viewer:
    def __init__(self, key):
        self.base = {}
        self.percents = key
        self.btw = ''
        self.rank = []

    def __str__(self):
        for i in range(0, len(self.percents)):
            self.rank.append(
                f'{str(i + 1)}. {self.base[self.percents[i]][0][0]} has had a {str(self.percents[i])}% success rate '
                f'with {self.base[self.percents[i]][0][1]} attempts\n'
            )
            del self.base[self.percents[i]][0]
        if self.btw == 'worst to best':
            self.rank = self.rank[::-1]
        self.rank = ''.join(self.rank)
        return self.rank

    def sort(self, arr):
        if len(arr) == 1:
            return arr
        else:
            mid = math.ceil(len(arr) / 2)
            l = arr[:mid]
            r = arr[mid:]
            l = self.sort(l)
            r = self.sort(r)
            i = j = k = 0
            while i != len(l) and j != len(r):
                if l[i] > r[j]:
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
