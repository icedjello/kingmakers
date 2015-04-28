
def kingmaker(world, my_pos):
    me = world.agent_at(my_pos)
    t_area = world.touch_area(my_pos)
    v_area = world.vision_area(my_pos)
    empty = world.adjacent_advanceable(my_pos)
    strongest = world.strongest(v_area)
    weakest = world.weakest(me, t_area)
    w_pos = world.weakest_cell(my_pos, t_area)
    #s_pos = world.weakest_cell(my_pos, t_area)
    e_area = world.filter_area2(v_area, strongest)
    interface = world.interface_with(my_pos, e_area)
    shield_dir = world.best_shield(my_pos, e_area)

    if empty:
        return world.ADV, world.vsub(empty, my_pos)
    elif me == strongest:
        if weakest:
            return world.ADV, world.vsub(w_pos, my_pos)
        else:
            return world.PASS,
    else: # me != strongest
        # if shield_dir: # if an adequate shield exists
        #     return world.GIVE, shield_dir
        # elif interface:
        if interface: # if an adequate shield exists
            return world.ADV, world.vsub(interface, my_pos)
        elif shield_dir:
            return world.GIVE, shield_dir
        else:
            return world.PASS,

# def kingmaker(self, my_pos):
    #     me = self.agent_at(my_pos)
    #     area = self.vision_area(my_pos)
    #     advanceable = self.adjacent_advanceable(my_pos)
    #     strongest = self.strongest(area)
    #     weakest_pos = self.weakest_cell(my_pos, self.touch_area(my_pos))
    #     enemy_area = self.filter_area(area, strongest)
    #     # print ', kmkrs', my_pos, 'strongest', strongest, 'weakest', weakest_pos
    #     if advanceable:
    #         # print '0, contest'
    #         return self.ADV, self.vsub(advanceable, my_pos)
    #     if me != strongest:
    #         interface = self.interface_with(my_pos, enemy_area)
    #         # can_i_attach_str = bool(interface)
    #         if interface:
    #             # print '1, iface'
    #             return (self.ADV, self.vsub(interface, my_pos))
    #         else:
    #             shield_dir = self.best_shield(my_pos, enemy_area)
    #             if shield_dir:
    #                 # print '2, shield'
    #                 return (self.GIVE, shield_dir)
    #             else:
    #                 # print '3, stabb no shield'
    #                 if weakest_pos:
    #                     return (self.ADV, self.vsub(weakest_pos, my_pos))
    #     elif weakest_pos:
    #         # print '4, stab weakest'
    #         return (self.ADV,  self.vsub(weakest_pos, my_pos))
    #     else:
    #         # print '5, pass'
    #         return (self.PASS,)

    # def loop_check(self, cw):
    #     pw = []
    #     if cw == pw:
    #         return True
    #     else:
    #         return False
    #         cw = pw
