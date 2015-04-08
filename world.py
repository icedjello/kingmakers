import cho

class World:
    W = (-1, 0)
    E = (1, 0)
    N = (0, 1)
    S = (0, -1)
    RAD = 2
    ADV = 'advance'
    GIVE = 'give'
    PASS = 'pass'
    dirs = [N, S, E, W]
    time = 0
    def __init__(self, size = 2, initial_hp = 3):
        self.lattice = []
        self.size = size
        for x in range(size):
            self.lattice.append([])
            for y in range(size):
                self.lattice[x].append({
                    'cell_hp': initial_hp,
                    'agent_hp': initial_hp,
                    'agent': None,
                    'contesters': set()
                })

    def scan_for(self, agent):
        return [(x, y) for x in range(self.size)
                 for y in range(self.size)
                 if self.lattice[x][y]['agent'] == agent]

    def vigorize(self, (x, y)):
        self.lattice[x][y]['agent'] = (x, y)

    def vigorize_all(self):
        for x in range(self.size):
            for y in range(self.size):
                self.vigorize((x, y))

    def cell_moves(self, (x, y)):
        moves = []
        source = self.agent_at((x,y))
        for dir in self.dirs:
            tx, ty = self.vadd((x, y), dir)
            target = self.agent_at((tx, ty))
            if not self.is_desolate((tx, ty)) and source != target:
                    moves.append(((x, y), self.ADV, dir))
            if target and source != target:
                    moves.append(((x, y), self.GIVE, dir))
        moves.append(((x, y), self.PASS, ))
        return moves

    def pretty_move(self, move):
        str = self._agent_to_str(move[0]) + ' ' + move[1].ljust(8)
        if len(move) >= 3:
            str += self._dir_to_str(move[2])
        return str

    # def all_agents(self):
    #     a = set()
    #     for x in range(self.size):
    #         for y in range(self.size):
    #             hereag = self.agent_at((x, y))
    #             if hereag:
    #                 a.add(hereag)
    #     return a

    def agents_in_area(self, area):
        return set(self.agent_at(pos) for pos in area) - set([None])

    def pretty_all_agents_choices(self):
        for a in self.all_agents():
            print self._agent_to_str(a)
            for ch in self.agent_moves(a):
                print self.pretty_choice(ch)

    def pretty_choice(self, choice):
        str = ''
        for move in choice:
            str += '    ' + self.pretty_move(move)
            str += '\n'
        return str

    def _dir_to_str(self, dir):
        return {
            self.N: 'N',
            self.S: 'S',
            self.W: 'W',
            self.E: 'E'
        }[dir]

    def agent_moves(self, agent):
        return cho.cho(map(self.cell_moves, self.scan_for(agent)))

    def agent_at(self, (x, y)):
        return self.lattice[x][y]['agent']

    def contest(self, agent, (x, y)):
        self.lattice[x][y]['contesters'].add(agent)

    def damage(self, (x, y)):
        self.lattice[x][y]['agent_hp'] -= 1

    def tick(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.lattice[x][y]['agent_hp'] <= 0:
                    if self.lattice[x][y]['agent']:
                        self.lattice[x][y]['cell_hp'] -= 1
                    self.lattice[x][y]['agent_hp'] = 0
                    self.lattice[x][y]['agent'] = None
                contesters = self.lattice[x][y]['contesters']
                if len(contesters) > 0:
                    if len(contesters) > 1:
                        self.lattice[x][y]['cell_hp'] -= 1
                    else:
                        self.lattice[x][y]['agent_hp'] = self.lattice[x][y]['cell_hp']
                        self.lattice[x][y]['agent'] = list(contesters)[0]
                    self.lattice[x][y]['contesters'] = set()
        self.time += 1

    def is_desolate(self, (x, y)):
        return self.lattice[x][y]['cell_hp'] <= 0

    def is_empty(self, pos):
        return self.agent_at(pos) == None

    def advance(self, from_pos, dir):
        source = self.agent_at(from_pos)
        target_pos = self.vadd(from_pos, dir)
        target = self.agent_at(target_pos)
        if target:
            self.damage(target_pos)
        else:
            self.contest(source, target_pos)

    def give(self, (x, y)):
        self.lattice[x][y]['agent_hp'] = min(
            self.lattice[x][y]['agent_hp'] + 1,
            self.lattice[x][y]['cell_hp'])

    def do_move(self, from_pos, move):
        print 'move', move
        if move[0] == self.GIVE:
            self.give(move[1])
        elif move[0] == self.ADV:
            self.advance(from_pos, move[1])

    def _agent_to_str(self, a):
        if not a:
            return '..'
        return str(a[0])+str(a[1])

    def _cell_to_str(self, cell):
        s = ''
        a = cell['agent']
        s += self._agent_to_str(a)
        if cell['agent_hp'] == 0:
            s += '.'
        else:
            s += str(cell['agent_hp'])
        if cell['cell_hp'] == 0:
            s += '.'
        else:
            s += str(cell['cell_hp'])
        return s

    def hp_at(self, (x, y)):
        return self.lattice[x][y]['agent_hp']

    def vzero(self):
        return (0, 0)

    def vadd(self, v1, v2):
        return (v1[0] + v2[0]) % self.size, (v1[1] + v2[1]) % self.size

    def vmult(self, v1, scalar):
        return (v1[0] * scalar, v1[1] * scalar)

    def vsub(self, v1, v2):
        return self.vadd(v1, self.vmult(v2, -1))

    def sum_health(self, agent_area):
        return sum(map(self.hp_at, agent_area))

    def generate_feelers(self):
        return set(map(self.squash_feeler, list(cho.cho(([self.dirs + [(0, 0)]]) * self.RAD))))

    def squash_feeler(self, feeler):
        return reduce(self.vadd, feeler)

    def power(self, agent_area):
        return len(agent_area) * self.sum_health(agent_area)

    def filter_area(self, area, agent):
        return filter(lambda pos: self.agent_at(pos) == agent, area)

    def vision_area(self, (x, y)):
        return map(lambda feeler: self.vadd((x, y), feeler), self.generate_feelers())

    def agent_power_in_area(self, agent, area):
        return self.power(self.filter_area(area, agent))

    def strongest(self, area):
        ags = self.agents_in_area(area)
        return max(ags, key=lambda ag: self.agent_power_in_area(ag, area))

    def weakest(self, me, area):
        ags = self.agents_in_area(area) - set(me)
        if ags:
            return min(ags, key=lambda ag: self.agent_power_in_area(ag, area))

    def weakest_cell(self, my_pos, area):
        inters = self.area_intersect(self.scan_for(self.weakest(self.agent_at(my_pos), area)), self.touch_area(my_pos))
        if len(inters) > 0:
            return list(inters)[0]

    def touch_area(self, my_pos):
        return [self.vadd(my_pos, vdir) for vdir in self.dirs]

    def area_intersect(self, a, b):
        return set(a).intersection(b)

    def area_sub(self, a, b):
        return set(a) - set(b)

    def interface_with(self, cell_pos, agent_area):
        inters = self.area_intersect(self.touch_area(cell_pos), agent_area)
        if len(inters) >= 1:
            return list(inters)[0]
        else:
            return None

    def weakest_shield_pos(self, my_pos):
        return min(self.touch_area(my_pos), key=self.hp_at)

    def shield_area(self, from_pos, vdir):
        return map(lambda x: self.vadd(x, vdir),
                   self.area_sub(self.touch_area(from_pos), [self.vsub(from_pos, vdir)]))

    def best_shield(self, my_pos, enemy_area):
        weakest_pos = self.weakest_shield_pos(my_pos)
        towards_shield = self.vsub(weakest_pos, my_pos)
        shielded_area = self.shield_area(my_pos, towards_shield)
        if len(self.area_intersect(shielded_area, enemy_area)) > 0:
            return towards_shield

    def is_advanceable(self,pos):
        return self.is_empty(pos) and not self.is_desolate(pos)

    def adjacent_advanceable(self, pos):
        k = filter(self.is_advanceable, self.touch_area(pos))
        if len(k) > 0:
            return k[0]

    def kingmaker(self, my_pos):
        me = self.agent_at(my_pos)
        area = self.vision_area(my_pos)
        advanceable = self.adjacent_advanceable(my_pos)
        strongest = self.strongest(area)
        weakest_pos = self.weakest_cell(my_pos, self.touch_area(my_pos))
        enemy_area = self.filter_area(area, strongest)
        print ', kmkrs', my_pos, 'strongest', strongest, 'weakest', weakest_pos
        if advanceable:
            print '0, contest'
            return self.ADV, self.vsub(advanceable, my_pos)
        if me != strongest:
            interface = self.interface_with(my_pos, enemy_area)
            if interface:
                print '1, iface'
                return (self.ADV, self.vsub(interface, my_pos))
            else:
                shield_dir = self.best_shield(my_pos, enemy_area)
                if shield_dir:
                    print '2, shield'
                    return (self.GIVE, shield_dir)
                else:
                    print '3, stabb no shield'
                    if weakest_pos:
                        return (self.ADV, self.vsub(weakest_pos, my_pos))
        elif weakest_pos:
            print '4, stab weakest'
            return (self.ADV,  self.vsub(weakest_pos, my_pos))
        else:
            print '5, pass'
            return (self.PASS,)

    # def loop_check(self, cw):
    #     pw = []
    #     if cw == pw:
    #         return True
    #     else:
    #         return False
    #         cw = pw


    def run_all(self):
        print "Time: {}".format(self.time)
        # if loop_check():
        #     print stuff
        # else:
        for x in range(self.size):
            for y in range(self.size):
                if self.agent_at((x, y)):
                    move = self.kingmaker((x, y))
                    self.do_move((x, y), move)
        self.tick()

    def run_all_for(self, n):
        for i in range(n):
            self.run_all()
            print self

    def __str__(self):
        s = ''
        for y in range(self.size):
            for x in range(self.size):
                s += '|' + self._cell_to_str(self.lattice[x][y])
            s += '|\n'
        return s

    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    import time
    w = World()
    w.vigorize_all()
    while True:
        print w
        w.run_all()
        time.sleep(0.5)
