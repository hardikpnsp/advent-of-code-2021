from typing import Dict, List
import re

class BingoBoard():
    def __init__(self, board: List[List[int]]):
        self.freeze: bool = False
        self.board: List[List[int]] = board
        self.check: List[List[int]] = [[0 for _ in range(5)] for _ in range(5)]
        self.num_map: Dict[int, tuple] = {}
        for i, row in enumerate(board):
            for j, num in enumerate(row):
                self.num_map[num] = (i, j)

    def __repr__(self) -> str:
        board = "\n".join([" ".join(map(str, row)) for row in self.board])
        start = "\n----------------\n"
        return start + board + start

    def check_bingo(self):
        bingo_rows = any(filter(lambda x: x == 5, [sum(row) for row in self.check]))
        cols = []
        for i in range(5):
            cols.append([self.check[j][i] for j in range(5)])

        bingo_cols = any(filter(lambda x: x == 5, [sum(col) for col in cols]))
        return bingo_cols or bingo_rows

    def call(self, number: int):
        if self.freeze:
            return False

        if number in self.num_map:
            i, j = self.num_map[number]
            self.check[i][j] = 1

        self.freeze = self.check_bingo()
        return self.freeze

    def sum_of_unmarked_numbers(self):
        add = 0
        for i in range(5):
            for j in range(5):
                if self.check[i][j] == 0:
                    add += self.board[i][j]
        return add


def read_input():
    boards: List[BingoBoard] = []
    numbers: List[int] =[]
    with open('./input.txt') as f:
        numbers = list(map(int, f.readline().split(",")))
        while(f.readline()):
            board = []
            for i in range(5):
                board.append(list(map(int, re.split(r"\s+", f.readline().strip()))))
            boards.append(BingoBoard(board))

    return (numbers, boards)

def first_win(numbers: List[int], boards: List[BingoBoard]):
    for number in numbers:
        for board in boards:
            if board.call(number):
                return board.sum_of_unmarked_numbers() * number

def last_win(numbers: List[int], boards: List[BingoBoard]):
    last_score = 0
    for number in numbers:
        for board in boards:
            if board.call(number):
                last_score = board.sum_of_unmarked_numbers() * number

    return last_score

if __name__ == "__main__":
    numbers, boards = read_input()
    # print(first_win(numbers, boards))
    print(last_win(numbers, boards))