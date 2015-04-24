__author__ = 'Gonzo'

import random
import math

def rondo():
    return random.random()

def rando(n = 9):
    return math.floor(rondo() * (n % 10)) + 1

def r_co(n):
    r = range(n)
    return random.choice(r)

def chooser(l, n):
    copy = l[:]
    choosed = []
    for i in range(n):
        chosen = random.choice(copy)
        choosed.append(chosen)
        copy.remove(chosen)
    return choosed

def ranpos(size):
    return random.randint(0, size-1), random.randint(0, size-1)

