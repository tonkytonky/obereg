ENEMY = '!!'
DEFENDER = '{}'
KING = '**'
THRONE = '*'
EXIT = '>>'
EMPTY = '-'


class Field:
    def __init__(self, i, j, figure=None):
        self.i = i
        self.j = j
        self.figure = figure


class PlainField(Field):
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '-'


class ThroneField(Field):
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '**'


class ExitField(Field):
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '>>'


class Figure:
    def __init__(self, move_limit=None):
        self.possible_fields = []
        self.possible_moves = []
        self.move_limit = move_limit

    def get_possible_moves(self, board, field):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            i, j = field.i, field.j
            while True:
                i += modifier[0]
                j += modifier[1]

                is_i_in_board = 0 <= i + modifier[0] < 9
                is_j_in_board = 0 <= j + modifier[1] < 9
                if board[i][j].figure or not is_i_in_board or not is_j_in_board:
                    break
                elif self.move_limit and self.move_limit == len(self.possible_moves):
                    break
                elif type(board[i][j]) not in self.possible_fields:
                    continue
                else:
                    self.possible_moves.append((i, j))


class AttackerFigure(Figure):
    def __init__(self):
        super(AttackerFigure).__init__()
        self.possible_fields.extend([PlainField])

    def __str__(self):
        return '!!'


class DefenderFigure(Figure):
    def __init__(self):
        super(DefenderFigure).__init__()
        self.possible_fields.extend([PlainField])

    def __str__(self):
        return '{}'


class KingFigure(Figure):
    def __init__(self):
        super(KingFigure).__init__()
        self.possible_fields.extend([PlainField, ThroneField, ExitField])

    def __str__(self):
        return '**'



class King:
    def __init__(self, i, j, move_limit):
        self.i = i
        self.j = j
        self.possible_moves = []
        self.move_limit = move_limit

    def __str__(self):
        return KING

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            move_possible = True
            moves_counter = 0
            i, j = self.i, self.j
            while move_possible and 0 <= i + modifier[0] < 9 and 0 <= j + modifier[1] < 9:
                i += modifier[0]
                j += modifier[1]
                if board[i][j] in (EMPTY, THRONE, EXIT) and moves_counter <= self.move_limit:
                    self.possible_moves.append((i, j))
                else:
                    move_possible = False


board = [
    [ExitField(0, 0), PlainField(0, 1), PlainField(0, 2), PlainField(0, 3, Enemy)],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

board = [
    [EXIT,        EMPTY, EMPTY, Enemy(0, 3), Enemy(0, 4), Enemy(0, 5), EMPTY, EMPTY, EXIT],
    [EMPTY,       EMPTY, EMPTY, EMPTY, EMPTY, Enemy(1, 4), EMPTY, EMPTY, EMPTY],
    [EMPTY,       EMPTY, EMPTY, EMPTY, Defender(2, 4), EMPTY, EMPTY, EMPTY, EMPTY],
    [Enemy(3, 0), EMPTY, EMPTY, EMPTY, Defender(3, 4), EMPTY, EMPTY, EMPTY, Enemy(3, 8)],
    [Enemy(4, 0), Enemy(4, 1), Defender(4, 2), Defender(4, 3), King(4, 4, move_limit=3), Defender(4, 5), Defender(4, 6), Enemy(4, 7), Enemy(4, 8)],
    [Enemy(5, 0), EMPTY, EMPTY, EMPTY, Defender(5, 4), EMPTY, EMPTY, EMPTY, Enemy(5, 8)],
    [EMPTY,       EMPTY, EMPTY, EMPTY, Defender(6, 4), EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY,       EMPTY, EMPTY, EMPTY, EMPTY, Enemy(7, 4), EMPTY, EMPTY, EMPTY],
    [EXIT,        EMPTY, EMPTY, Enemy(8, 3), Enemy(8, 4), Enemy(8, 5), EMPTY, EMPTY, EXIT],
]



def fill_board(soldiers, board):
    for soldier in soldiers:
        board[soldier.i][soldier.j] = soldier


def get_possible_moves(soldiers):
    for soldier in soldiers:
        soldier.get_possible_moves(board)


def print_board(board):
    for line in board:
        print('\t'.join(str(field) for field in line))





# 1 Расставить фигуры
fill_board(defenders + enemies, board)

print_board(board)

# 2 Рассчитать возможные ходы
get_possible_moves(defenders + enemies)


# 3 Сделать ход
def make_move():
    print('Human turn')
    from_i, from_j = [int(coord) for coord in input('input from coordinates: ').split(' ')]

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


make_move()

print('Defenders turn')
from_i, from_j = (int(coord) for coord in input('input from coordinates: '))
to_i, to_j = (int(coord) for coord in input('input to coordinates: '))

# 4 Съесть фигуры
