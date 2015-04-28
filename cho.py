
def cho(lists):
    for elem in lists[0]:
        if len(lists) == 1:
            yield (elem,)
        else:
            for subcho in cho(lists[1:]):
                yield (elem,) + subcho