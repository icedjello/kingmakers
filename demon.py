import world
import random
import sys

def fatpiggie():
    w = world.World(6)
    w.vigorize_all()
    for (x, y) in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        w.bias(x, y, 8)
        w.lattice[x][y]['agent'] = (2,2)
    for i in range(100):
        w.run_all()
        print w
    #w.ex_run(True)

def piggie():
    w = world.World(3)
    w.vigorize_all()
    w.bias(1, 1, 8)
    w.ex_run(True)

def duel():
    w = world.World(10)
    w.vigorize((3, 5))
    w.vigorize((6, 5))
    w.ex_run(True)

def flatplot():
    times = []
    for s in range(1, 100):
        print 'World S', s
        w = world.World(s)
        w.vigorize_all()
        w.ex_run(True)
        times.append(w.time)
    print times

def lavarain():
    size = 10
    w = world.World(size)
    w.vigorize_all()
    to_go = True
    while to_go:
        print 'before lava'
        print w
        to_go = w.run_all(True)
        x, y = random.randint(1, size-1), random.randint(1, size-1)
        w.damage((x, y))
        print 'after lava'
        print w
        to_go = True

def flatland():
    w = world.World(3, 3)
    w.vigorize_all()
    w.ex_run(True)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        exec(sys.argv[1] + '()')
    else:
        print 'Please run with:'
        print 'python demon.py <experiment-name>'
