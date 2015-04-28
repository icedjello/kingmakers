import unittest
import world

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.w = world.World(10)
        self.v = world.World(10)
        self.v.vigorize_all()
        self.ags = world.World(10)
        self.ags.vigorize((3, 2))
        self.ags.lattice[3][2]['agent_hp'] = 5
        self.ags.vigorize((2, 3))
        self.ags.lattice[2][3]['agent_hp'] = 3
        self.ags.vigorize((3, 3))
        self.ags.vigorize((3, 4))
        self.ags.lattice[3][4]['agent_hp'] = 1
        self.ags.vigorize((4, 2))
        self.ags.lattice[4][2]['agent_hp'] = 9
        self.fat = world.World(10)
        self.fat.vigorize((3, 3))
        self.fat.vigorize((2, 3))
        self.fat.advance((2, 3), self.fat.N)
        self.fat.tick()
        self.fat.advance((2, 2), self.fat.E)
        self.fat.tick()
        self.fat.damage((3, 2))
        self.fat.damage((3, 2))
        self.fat.tick()

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

    def test_agent_at(self):
        self.assertEquals((0, 0), self.v.agent_at((0, 0)))

    def test_vision_area(self):
        s = {(3, 1),
             (2, 2), (3, 2), (4, 2),
             (1, 3), (2, 3), (3, 3), (4, 3), (5, 3),
             (2, 4), (3, 4), (4, 4),
             (3, 5)}
        self.assertEquals(s, self.w.vision_area((3, 3)))

    def test_adjacent_advanceable(self):
        self.w.vigorize((1, 1))
        self.w.lattice[1][0]['cell_hp'] = 0
        self.w.lattice[0][1]['cell_hp'] = 0
        self.w.lattice[1][2]['cell_hp'] = 0
        self.assertEquals((2, 1), self.w.adjacent_advanceable((1, 1)))

    def test_strongest(self):
        self.assertEquals((4, 2), self.ags.strongest(self.ags.vision_area((3, 3))))

    def test_weakest(self):
        self.assertEquals((3, 4), self.ags.weakest((3, 3), self.ags.vision_area((3, 3))))

    def test_weakest_cell(self):
        weakest_pos = self.fat.weakest_cell((3, 3), self.fat.touch_area((3, 3)))
        self.assertEquals((3, 2), weakest_pos)

    def test_filter_area(self):
        self.w.vigorize((2, 2))
        self.assertEquals({(2, 2)}, self.w.filter_area2({(2, 2), (3, 2)}, (2, 2)))

    def test_interface_with(self):
        self.w.vigorize((1, 3))
        self.w.advance((1, 3), self.w.E)
        self.w.tick()
        self.w.vigorize((3, 3))
        self.assertEquals((2, 3), self.w.interface_with((3, 3), self.w.scan_for((1, 3))))

    def test_none_interface_with(self):
        self.w.vigorize((1, 3))
        self.w.vigorize((3, 3))
        self.assertEquals(None, self.w.interface_with((3, 3), self.w.scan_for((1, 3))))

    def test_best_shield(self):
        self.w.vigorize((1, 3))
        self.w.lattice[1][3]['agent_hp'] = 5
        self.w.vigorize((2, 3))
        self.w.vigorize((3, 3))
        self.assertEquals((2, 3), self.w.best_shield((3, 3), self.w.scan_for((1, 3))))

    def test_is_desolate(self):
        self.w.vigorize((2, 2))
        self.w.lattice[2][2]['cell_hp'] = 0
        self.assertEquals(True, self.w.is_desolate((2, 2)))

    def test_no_best_shield(self):
        self.w.vigorize((1, 3))
        self.w.vigorize((3, 3))
        self.w.lattice[2][3]['cell_hp'] = 0
        self.assertEquals(None, self.w.best_shield((3, 3), self.w.scan_for((1, 3))))


    def test_touch_area(self):
        s = {(0, 1), (2, 1), (1, 0), (1, 2)}
        self.assertEquals(s, self.w.touch_area((1, 1)))

    # def test_kill_neighbour(self):
    #     self.w.vigorize((0, 0))
    #     self.w.vigorize((1, 0))
    #     self.assertEquals((self.w.ADV, self.w.E), self.w.kingmaker((0, 0)))

if __name__ == '__main__':
    unittest.main()