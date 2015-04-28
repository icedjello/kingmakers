import world
import sys

def fatpiggy():
    w = world.World(6)
    w.vigorize_all()
    for (x, y) in [(2, 2), (2, 3), (3, 2), (3, 3)]:
        w.bias(x, y, 8)
        w.lattice[x][y]['agent'] = (2,2)
    for i in range(100):
        w.run_all()
        print w
    #w.ex_run(True)

def tilegame():
    w = world.World(3)
    w.vigorize_all()
    for i in range(9):
        x, y = i % 3, i // 3
        w.bias(x, y, i + 1)
    w.ex_run(True)

def piggy():
    w = world.World(3)
    w.vigorize_all()
    w.bias(1, 1, 8)
    w.ex_run(True)

def piggy_war():
    w = world.World(3)
    w.vigorize_all()
    w.bias(0, 0, 8)
    w.bias(2, 2, 1)
    w.ex_run(True)

def weak_piggy():
    w = world.World(3)
    w.vigorize_all()
    w.bias(1, 1, 1)
    w.ex_run(True)

def duel():
    w = world.World(10)
    # w.vigorize((3, 5))
    # w.vigorize((6, 5))

    # w.vigorize((0, 0))
    # w.vigorize((9, 9))

    w.vigorize((5, 5))
    w.vigorize((0, 0))
    w.ex_run(True)

def cowboys():
    w = world.World(10)
    w.vigorize((5, 4))
    w.vigorize((4, 4))
    w.ex_run(True)

def truel():
    w = world.World(10)
    w.vigorize((0, 0))
    w.vigorize((7, 7))
    w.vigorize((3, 4))
    w.ex_run(True)

def drawtape(w, y, h):
    for x in range(10):
        w.lattice[x][y]['agent'] = (1, y)
        w.bias(x, y, h)

def tape():
    w = world.World(10)
    w.vigorize_all()
    drawtape(w, 4, 1)
    w.ex_run(True)

def weak_tab():
    w = world.World(10)
    w.vigorize_all()
    h = 1
    y = 4
    for x in range(3, 7):
        w.lattice[x][y]['agent'] = (4, y)
        w.bias(x, y, h)
    w.ex_run(True)

def strong_tab():
    w = world.World(10)
    w.vigorize_all()
    h = 8
    y = 4
    for x in range(3, 7):
        w.lattice[x][y]['agent'] = (4, y)
        w.bias(x, y, h)
    w.ex_run(True)

def stripes():
    w = world.World(10)
    w.vigorize_all()
    h = 9
    drawtape(w, 0, h)
    drawtape(w, 2, h)
    drawtape(w, 4, h)
    drawtape(w, 6, h)
    drawtape(w, 8, h)
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

def tinyflatland():
    w = world.World(3, 3)
    w.vigorize_all()
    w.ex_run(True)

def flatland():
    w = world.World(9, 9)
    w.vigorize_all()
    w.ex_run(True)

def crazyflatland():
    w = world.World(20, 20)
    w.vigorize_all()
    w.ex_run(True)

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        exec(sys.argv[1] + '()')
    else:
        print 'Please run with:'
        print 'python demon.py <experiment-name>'
