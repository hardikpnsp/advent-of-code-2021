from functools import cache


def deterministic_dice():
    i = 1
    while True:
        yield i
        i += 1
        if i > 100:
            i = 1


def take_turn(score, pos, dice):
    move = 0
    for _ in range(3):
        move += next(dice)

    move = move % 10
    pos += move
    if pos > 10:
        pos -= 10
    score += pos

    return score, pos


def practice_game(p1_pos, p2_pos):
    p1_score = 0
    p2_score = 0
    total_dice_rolls = 0
    turn = True
    dice = deterministic_dice()
    while p1_score < 1000 and p2_score < 1000:
        if turn:
            p1_score, p1_pos = take_turn(p1_score, p1_pos, dice)
            turn = False
        else:
            p2_score, p2_pos = take_turn(p2_score, p2_pos, dice)
            turn = True

        total_dice_rolls += 3

    if p1_score > p2_score:
        print(f"Part1: Player 1 won, output: {p2_score * total_dice_rolls}")
    else:
        print(f"Part1: Player 2 won, output: {p1_score * total_dice_rolls}")


def take_turn_dirac_dice(pos, score):
    possible_moves = [3, 4, 5, 4, 5, 6, 5, 6, 7, 4, 5, 6, 5, 6, 7, 6, 7, 8, 5, 6, 7, 6, 7, 8, 7, 8, 9]
    result = []
    for move in possible_moves:
        p = pos + move
        if p > 10:
            p -= 10
        s = score + p
        result.append((p, s))
    return result


@cache
def game(p1_pos, p2_pos, p1_score=0, p2_score=0, turn=True):
    if p1_score >= 21:
        return 1, 0
    elif p2_score >= 21:
        return 0, 1

    g = (p1_pos, p2_pos, p1_score, p2_score, turn)
    p1_wins = 0
    p2_wins = 0

    p1pos, p2pos, p1score, p2score, turn = g
    if turn:
        possible_position_scores = take_turn_dirac_dice(p1pos, p1score)
        for p, s in possible_position_scores:
            p1wins, p2wins = game(p, p2pos, s, p2score, False)
            p1_wins += p1wins
            p2_wins += p2wins
    else:
        possible_position_scores = take_turn_dirac_dice(p2pos, p2score)
        for p, s in possible_position_scores:
            p1wins, p2wins = game(p1pos, p, p1score, s, True)
            p1_wins += p1wins
            p2_wins += p2wins

    return p1_wins, p2_wins


if __name__ == "__main__":
    practice_game(p1_pos=4, p2_pos=2)
    p1_wins, p2_wins = game(p1_pos=4, p2_pos=2)
    if p1_wins > p2_wins:
        print(f"Part2: p1 wins = {p1_wins}")
    else:
        print(f"Part2: p2 wins = {p2_wins}")
