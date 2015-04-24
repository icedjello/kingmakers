import world
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

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        exec(sys.argv[1] + '()')
    else:
        print 'Please run with:'
        print 'python demon.py <experiment-name>'
