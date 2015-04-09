__author__ = 'Gonzo'

def weakest(world, me, area):
    pass
    #build to scan for a weakest and if weakest == me then return None


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
        #strongest: done
    else: # me != strongest
        if shield_dir: # if an adequate shielf exists
            return world.GIVE, shield_dir

        elif interface:
            return world.ADV, world.vsub(interface, my_pos)
        else:
            return world.PASS,



    # else: # me != strongest
    #     if world.filter_area2(t_area, strongest): #if i can attack strongest
    #         return world.ADV, world.vsub(s_pos, my_pos)
    #     else: #if the strongest isn't in the t_area
    #         if interface