class Enemy:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.possible_moves = []

    def __repr__(self):
        return 'E'

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            move_possible = True
            i, j = self.i, self.j
            while move_possible and 0 <= i + modifier[0] < 9 and 0 <= j + modifier[1] < 9:
                i += modifier[0]
                j += modifier[1]
                if board[i][j] == '*':
                    continue
                if not board[i][j]:
                    self.possible_moves.append((i, j))
                else:
                    move_possible = False


class Defender:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.possible_moves = []

    def __repr__(self):
        return 'D'

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            move_possible = True
            i, j = self.i, self.j
            while move_possible and 0 <= i + modifier[0] < 9 and 0 <= j + modifier[1] < 9:
                i += modifier[0]
                j += modifier[1]
                if board[i][j] == '*':
                    continue
                if not board[i][j]:
                    self.possible_moves.append((i, j))
                else:
                    move_possible = False


class King:
    def __init__(self, i, j, move_limit):
        self.i = i
        self.j = j
        self.possible_moves = []
        self.move_limit = move_limit

    def __repr__(self):
        return 'K'

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            move_possible = True
            moves_counter = 0
            i, j = self.i, self.j
            while move_possible and 0 <= i + modifier[0] < 9 and 0 <= j + modifier[1] < 9:
                i += modifier[0]
                j += modifier[1]
                if board[i][j] in (0, '*', '-') and moves_counter <= self.move_limit:
                    self.possible_moves.append((i, j))
                else:
                    move_possible = False


board = [
    ['-', 0, 0, 0, 0, 0, 0, 0, '-'],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, '*', 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ['-', 0, 0, 0, 0, 0, 0, 0, '-'],
]


def fill_board(soldiers, board):
    for soldier in soldiers:
        board[soldier.i][soldier.j] = soldier


def get_possible_moves(soldiers):
    for soldier in soldiers:
        soldier.get_possible_moves(board)


defenders = [
    Defender(2, 4),
    Defender(3, 4),
    Defender(4, 2),
    Defender(4, 3),
    Defender(4, 5),
    Defender(4, 6),
    Defender(5, 4),
    Defender(6, 4),
    King(4, 4, move_limit=3),
]

enemies = [
    Enemy(0, 3),
    Enemy(0, 4),
    Enemy(0, 5),
    Enemy(1, 4),
    Enemy(3, 0),
    Enemy(3, 8),
    Enemy(4, 0),
    Enemy(4, 1),
    Enemy(4, 7),
    Enemy(4, 8),
    Enemy(5, 0),
    Enemy(7, 8),
    Enemy(7, 4),
    Enemy(8, 3),
    Enemy(8, 4),
    Enemy(8, 5),
]

# 1 Расставить фигуры
fill_board(defenders + enemies, board)

for line in board:
    print(line)

# 2 Рассчитать возможные ходы
get_possible_moves(defenders + enemies)

# 3 Сделать ход
print('Enemies turn')
inputed = input('input from coordinates: ')
from_i, from_j = [int(coord) for coord in inputed.split()]
field_on_board = 0 <= from_i < 9 and 0 <= from_j < 9
field_has_figure = type(board[from_i][from_j]) in (Defender, King, Enemy)
figure_has_moves = board[from_i][from_j].possible_moves

while not field_on_board and not field_has_figure and not figure_has_moves:
    print('Repeat input..')
    from_i, from_j = (int(coord) for coord in input('input from coordinates: ').split())

to_i, to_j = (int(coord) for coord in input('input to coordinates: ').split())
field_on_board = 0 <= to_i < 9 and 0 <= to_j < 9
while not field_on_board and (to_i, to_j) not in board[from_i][from_j].possible_moves:
    print('Repeat input..')
    to_i, to_j = (int(coord) for coord in input('input to coordinates: ').split())


board[to_i][to_j] = board[from_i][from_j]
board[from_i][from_j] = 0

print('Defenders turn')
from_i, from_j = (int(coord) for coord in input('input from coordinates: '))
to_i, to_j = (int(coord) for coord in input('input to coordinates: '))


