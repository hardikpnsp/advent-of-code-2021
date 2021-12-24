from collections import defaultdict


def highest_point(y_max):
    return ((y_max - 1) * y_max) // 2


def running_sum(x):
    return (x * (x + 1)) // 2


def lower_bound_x(x1, x2):
    # lowest n such that n * (n + 1) // 2 >= x1
    n = 1
    # can do binary search
    while n < x2:
        if running_sum(n) >= x1:
            return n
        else:
            n += 1


def find_step_x(xval, x1, x2):
    xpos = 0
    step = 0
    result = []
    # can do binary search
    while xpos <= x2 and xval > 0:
        if xpos >= x1 and xpos <= x2:
            result.append(step)
        xpos += xval
        if xval > 0:
            xval -= 1
        elif xval < 0:
            xval += 1
        step += 1

    return result


def find_step_y(yval, y1, y2):
    # y1 and y2 are always negative according to the input
    step = 0
    if yval > 0:
        step = (2 * yval) + 1
        yval = -yval - 1

    ypos = 0

    result = []
    # can do binary search
    while ypos >= y1:
        if ypos >= y1 and ypos <= y2:
            result.append(step)

        ypos += yval
        yval -= 1
        step += 1
    return result


def find_step_x_stable(xval, x1, x2):
    xpos = 0
    step = 0
    while xpos <= x2:
        if xpos >= x1 and xpos <= x2 and xval == 0:
            return step
        else:
            xpos += xval
            if xval > 0:
                xval -= 1
            elif xval < 0:
                xval += 1
            step += 1

    return -1


if __name__ == "__main__":
    # target area: x=111..161, y=-154..-101
    hp = highest_point(154)
    print(f"Highest Point: {hp}")

    # target area: x=20..30, y=-10..-5
    x1 = 111
    x2 = 161
    y1 = -154
    y2 = -101

    val_x_low = lower_bound_x(x1, x2)
    val_x_high = x2
    val_y_low = y1
    val_y_high = -y1 - 1

    print(
        f"xlow: {val_x_low} -> xhigh: {val_x_high} -> ylow: {val_y_low} -> yhigh: {val_y_high}"
    )

    xsteps = defaultdict(list)

    for xval in range(val_x_low, val_x_high + 1):
        steps = find_step_x(xval, x1, x2)
        for step in steps:
            xsteps[step].append(xval)

    print(xsteps)

    xstable = defaultdict(list)

    for xval in range(val_x_low, val_x_high + 1):
        step = find_step_x_stable(xval, x1, x2)
        if step > 0:
            xstable[step].append(xval)

    print(xstable)

    ysteps = defaultdict(list)

    for yval in range(val_y_low, val_y_high + 1):
        steps = find_step_y(yval, y1, y2)
        for step in steps:
            ysteps[step].append(yval)

    print(ysteps)

    xstable_y = set()
    for steps in xstable.keys():
        for x in xstable[steps]:
            for y_step in filter(lambda k: k >= steps, ysteps.keys()):
                for y in ysteps[y_step]:
                    xstable_y.add((x, y))

    x_y = set()

    for steps in xsteps.keys():
        for x in xsteps[steps]:
            for y in ysteps[steps]:
                x_y.add((x, y))


    result = xstable_y.union(x_y)
    print(len(result))

    # answer = {
    #     (23, -10),
    #     (25, -9),
    #     (27, -5),
    #     (29, -6),
    #     (22, -6),
    #     (21, -7),
    #     (9, 0),
    #     (27, -7),
    #     (24, -5),
    #     (25, -7),
    #     (26, -6),
    #     (25, -5),
    #     (6, 8),
    #     (11, -2),
    #     (20, -5),
    #     (29, -10),
    #     (6, 3),
    #     (28, -7),
    #     (8, 0),
    #     (30, -6),
    #     (29, -8),
    #     (20, -10),
    #     (6, 7),
    #     (6, 4),
    #     (6, 1),
    #     (14, -4),
    #     (21, -6),
    #     (26, -10),
    #     (7, -1),
    #     (7, 7),
    #     (8, -1),
    #     (21, -9),
    #     (6, 2),
    #     (20, -7),
    #     (30, -10),
    #     (14, -3),
    #     (20, -8),
    #     (13, -2),
    #     (7, 3),
    #     (28, -8),
    #     (29, -9),
    #     (15, -3),
    #     (22, -5),
    #     (26, -8),
    #     (25, -8),
    #     (25, -6),
    #     (15, -4),
    #     (9, -2),
    #     (15, -2),
    #     (12, -2),
    #     (28, -9),
    #     (12, -3),
    #     (24, -6),
    #     (23, -7),
    #     (25, -10),
    #     (7, 8),
    #     (11, -3),
    #     (26, -7),
    #     (7, 1),
    #     (23, -9),
    #     (6, 0),
    #     (22, -10),
    #     (27, -6),
    #     (8, 1),
    #     (22, -8),
    #     (13, -4),
    #     (7, 6),
    #     (28, -6),
    #     (11, -4),
    #     (12, -4),
    #     (26, -9),
    #     (7, 4),
    #     (24, -10),
    #     (23, -8),
    #     (30, -8),
    #     (7, 0),
    #     (9, -1),
    #     (10, -1),
    #     (26, -5),
    #     (22, -9),
    #     (6, 5),
    #     (7, 5),
    #     (23, -6),
    #     (28, -10),
    #     (10, -2),
    #     (11, -1),
    #     (20, -9),
    #     (14, -2),
    #     (29, -7),
    #     (13, -3),
    #     (23, -5),
    #     (24, -8),
    #     (27, -9),
    #     (30, -7),
    #     (28, -5),
    #     (21, -10),
    #     (7, 9),
    #     (6, 6),
    #     (21, -5),
    #     (27, -10),
    #     (7, 2),
    #     (30, -9),
    #     (21, -8),
    #     (22, -7),
    #     (24, -9),
    #     (20, -6),
    #     (6, 9),
    #     (29, -5),
    #     (8, -2),
    #     (27, -8),
    #     (30, -5),
    #     (24, -7),
    # }

    # print(answer - result)
    # print(result - answer)