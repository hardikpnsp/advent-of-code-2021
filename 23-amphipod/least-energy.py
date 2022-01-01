from collections import deque
from typing import Optional, List, Union


class Amphipod:
    def __init__(self, symbol, positionx, positiony=0):
        self.symbol = symbol
        self.positionx = positionx
        self.positiony = positiony
        self.energy = self.set_energy()

    def move(self, posx, posy):
        steps = posx + self.positionx + abs(self.positiony - posy)
        self.positiony = posy
        self.positionx = posx
        return steps * self.energy

    def destination(self, sideroom_positions):
        return sideroom_positions[ord(self.symbol) - ord("A")]

    def is_in_hallway(self):
        if self.positionx == 0:
            return True
        else:
            return False

    def path(self, posx, posy):
        p = []
        for i in range(self.positionx - 1, -1, -1):
            p.append((i, self.positiony))

        step = -1 if posy < self.positiony else 1
        for i in range(self.positiony + step, posy + step, step):
            p.append((0, i))

        for i in range(1, posx + 1):
            p.append((i, posy))

        return p

    def is_move_possible(self, burrow, posx, posy):
        if posx == self.positionx and posy == self.positiony:
            return False
        for x, y in self.path(posx, posy):
            if burrow[x][y]:
                return False
        return True

    def next_positions(self, burrow, hallway_positions, sideroom_positions):
        if self.is_at_destination(burrow, sideroom_positions):
            return []

        positions = []
        y = self.destination(sideroom_positions)

        def check_burrow_symbols(i, y):
            for j in range(i+1, len(burrow)):
                if not (burrow[j][y] and burrow[j][y].symbol == self.symbol):
                    return False
            return True

        # greedy
        for i in range(len(burrow)-1, 0, -1):
            if self.is_move_possible(burrow, i, y) and check_burrow_symbols(i, y):
                positions.append((i, y))
                return positions

        # not greedy
        if not self.is_in_hallway():
            for i in hallway_positions:
                if self.is_move_possible(burrow, 0, i):
                    positions.append((0, i))

        return positions

    def set_energy(self):
        e = [1, 10, 100, 1000]
        return e[ord(self.symbol) - ord("A")]

    def is_at_destination(self, burrow, sideroom_positions):
        def check_burrow_symbols(i, y):
            for j in range(i+1, len(burrow)):
                if not (burrow[j][y] and burrow[j][y].symbol == self.symbol):
                    return False
            return True

        if self.destination(sideroom_positions) == self.positiony:
            return check_burrow_symbols(self.positionx, self.positiony)
        return False


class Game:
    def __init__(self, hallway_len=11, sideroom_len=2, sideroom_positions: Optional[List[int]] = None):
        self.min_energy = 300000
        self.hallway_len = hallway_len
        self.sideroom_len = sideroom_len
        if sideroom_positions is None:
            sideroom_positions = [2, 4, 6, 8]
        self.sideroom_positions = sideroom_positions

        self.burrow: List[List[Union[Optional[Amphipod], str]]] = [["#" for _ in range(hallway_len)] for _ in
                                                                   range(sideroom_len + 1)]
        for i in range(hallway_len):
            self.burrow[0][i] = None

        for p in sideroom_positions:
            for j in range(1, sideroom_len+1):
                self.burrow[j][p] = None

        self.amphipods: deque[Optional[Amphipod]] = deque()
        self.energy = 0
        self.hallway_positions = list(filter(lambda x: False if x in sideroom_positions else True, range(hallway_len)))
        self.explored = {}

    def move(self, posx, posy, new_posx, new_posy):
        energy = self.burrow[posx][posy].move(new_posx, new_posy)
        self.burrow[new_posx][new_posy] = self.burrow[posx][posy]
        self.burrow[posx][posy] = None
        return energy

    def add_amphipod(self, symbol, positionx: int, positiony: int = 0):
        amphipod = Amphipod(symbol, positionx, positiony)
        self.amphipods.append(amphipod)
        self.burrow[positionx][positiony] = amphipod

    def has_reached_solution(self):
        for amphipod in self.amphipods:
            if not amphipod.is_at_destination(self.burrow, self.sideroom_positions):
                return False
        return True

    def find_min_energy(self):
        # print(self.__repr__())
        game_state = self.game_state()
        if game_state in self.explored:
            if self.energy < self.explored[game_state]:
                self.explored[game_state] = self.energy
            else:
                return
        else:
            self.explored[game_state] = self.energy

        if self.energy >= self.min_energy:
            return
        elif self.has_reached_solution():
            self.min_energy = min(self.energy, self.min_energy)
            print(f"New minimum energy found {self.energy}")
            return
        else:
            for amphipod in self.amphipods:
                next_positions = amphipod.next_positions(self.burrow, self.hallway_positions, self.sideroom_positions)
                for new_posx, new_posy in next_positions:
                    posx, posy = amphipod.positionx, amphipod.positiony
                    energy = self.move(posx, posy, new_posx, new_posy)
                    self.energy += energy
                    self.find_min_energy()
                    self.move(new_posx, new_posy, posx, posy)
                    self.energy -= energy

    def __repr__(self):
        result = [["#" for _ in range(self.hallway_len)] for _ in range(len(self.burrow))]
        # set siderooms
        for i in self.sideroom_positions:
            for j in range(len(self.burrow)):
                cell = self.burrow[j][i]
                result[j][i] = cell.symbol if cell else "."

        # set hallway
        for i in range(len(self.burrow[0])):
            amphipod = self.burrow[0][i]
            if amphipod:
                result[0][i] = amphipod.symbol
            else:
                result[0][i] = "."

        return "\n".join(["".join(row) for row in result])

    def game_state(self):
        return tuple([(amphipod.positionx, amphipod.positiony) for amphipod in self.amphipods])


def main():
    g = Game()
    g.add_amphipod("C", 1, 2)
    g.add_amphipod("B", 2, 2)
    g.add_amphipod("A", 1, 4)
    g.add_amphipod("A", 2, 4)
    g.add_amphipod("B", 1, 6)
    g.add_amphipod("D", 2, 6)
    g.add_amphipod("D", 1, 8)
    g.add_amphipod("C", 2, 8)
    print(g)
    g.find_min_energy()
    print(f"Part1: {g.min_energy}")

    g = Game(sideroom_len=4)
    g.add_amphipod("C", 1, 2)
    g.add_amphipod("D", 2, 2)
    g.add_amphipod("D", 3, 2)
    g.add_amphipod("B", 4, 2)
    g.add_amphipod("A", 1, 4)
    g.add_amphipod("C", 2, 4)
    g.add_amphipod("B", 3, 4)
    g.add_amphipod("A", 4, 4)
    g.add_amphipod("B", 1, 6)
    g.add_amphipod("B", 2, 6)
    g.add_amphipod("A", 3, 6)
    g.add_amphipod("D", 4, 6)
    g.add_amphipod("D", 1, 8)
    g.add_amphipod("A", 2, 8)
    g.add_amphipod("C", 3, 8)
    g.add_amphipod("C", 4, 8)
    print(g)
    g.find_min_energy()
    print(f"Part2: {g.min_energy}")


if __name__ == "__main__":
    main()
