import unittest
import world

class TestWorld(unittest.TestCase):
    # def test_hp_at(self):
    #     w = world.World(4, 3)
    #     w.vigorize((1,1))
    #     self.assertEquals(3, w.hp_at((1,1)))
    #
    # def test_count_agent(self):
    #     w = world.World()
    #     w.vigorize((0,0))
    #     w.advance((0,0), w.E)
    #     w.tick()
    #     self.assertEquals(2, w.count_cells((0,0)))
    #
    # def test_sum_health(self):
    #     w = world.World(4,3)
    #     w.vigorize((0,0))
    #     w.advance((0,0), w.E)
    #     w.tick()
    #     self.assertEquals(6, w.sum_health((0,0)))

    def test_kill_neighbour(self):
        w = world.World()
        w.vigorize((0, 0))
        w.vigorize((1, 0))
        self.assertEquals((w.ADV, w.E), w.kingmaker((0, 0)))

if __name__ == '__main__':
    unittest.main()