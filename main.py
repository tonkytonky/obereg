# Клетки поля
class Cell:
    """Абстрактная"""
    def __init__(self, figure=None):
        self.figure = figure


class PlainCell(Cell):
    """Обычная"""
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '-'


class ExitCell(Cell):
    """Выход"""
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '>>'


class ThroneCell(Cell):
    """Трон"""
    def __str__(self):
        if self.figure:
            return str(self.figure)
        else:
            return '**'


# Фигуры
class Figure:
    """Абстрактная"""
    def __init__(self, i, j, move_limit=None):
        self.i = i
        self.j = j
        self.move_limit = move_limit
        self.possible_cells = []
        self.possible_moves = []

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            i, j = self.i, self.j
            while True:
                i += modifier[0]
                j += modifier[1]
                cell_on_board = 0 <= i < 9 and 0 <= j < 9
                if board[i][j].figure or not cell_on_board:
                    break
                elif self.move_limit and self.move_limit == len(self.possible_moves):
                    break
                elif type(board[i][j]) not in self.possible_cells:
                    continue
                else:
                    self.possible_moves.append((i, j))

    def set_coordinates(self, i, j):
        self.i = i
        self.j = j


class AttackerFigure(Figure):
    """Атакующий"""
    def __init__(self, i, j):
        super().__init__(i, j)
        self.possible_cells.extend([PlainCell])

    def __str__(self):
        return '!!'


class DefenderFigure(Figure):
    """Защищающийся абстрактная"""
    pass


class DefenderFigureSoldier(DefenderFigure):
    """Защищающийся солдат"""
    def __init__(self, i, j):
        super().__init__(i, j)
        self.possible_cells.extend([PlainCell])

    def __str__(self):
        return '{}'


class DefenderFigureKing(DefenderFigure):
    """Защищающийся князь"""
    def __init__(self, i, j, move_limit):
        super().__init__(i, j, move_limit)
        self.possible_cells.extend([PlainCell, ThroneCell, ExitCell])

    def __str__(self):
        return '**'


def print_board(board):
    for row in board:
        print('\t'.join(str(cell) for cell in row))


def get_all_possible_moves(figures, board):
    for figure in figures:
        figure.get_possible_moves(board)


def make_move():
    print('Human turn')

    from_i, from_j = [int(coord) for coord in input('input from coordinates: ').split(' ')]
    cell_on_board = 0 <= from_i < 9 and 0 <= from_j < 9
    cell_has_figure = board[from_i][from_j].figure
    figure_has_moves = board[from_i][from_j].figure.possible_moves
    while not cell_on_board or not cell_has_figure or not figure_has_moves:
        print('Repeat input..')
        from_i, from_j = [int(coord) for coord in input('input from coordinates: ').split()]

    to_i, to_j = [int(coord) for coord in input('input to coordinates: ').split()]
    cell_on_board = 0 <= to_i < 9 and 0 <= to_j < 9
    cell_in_possible_moves = (to_i, to_j) in board[from_i][from_j].figure.possible_moves
    while not cell_on_board or not cell_in_possible_moves:
        print('Repeat input..')
        to_i, to_j = [int(coord) for coord in input('input to coordinates: ').split()]

    board[to_i][to_j].figure = board[from_i][from_j].figure
    board[to_i][to_j].figure.set_coordinates(to_i, to_j)
    board[from_i][from_j].figure = None


def check_board(figure_type, board):
    if figure_type == AttackerFigure:
        for attacker in attackers:
            check_figure(attacker, board)
    elif figure_type == DefenderFigureSoldier:
        check_king(king)
        for defender in defenders:
            check_figure(defender, board)


def check_figure(figure, board):
    if type(figure) == AttackerFigure:
        opposite_type = DefenderFigure
    elif type(figure) == DefenderFigure:
        opposite_type = AttackerFigure
    else:
        raise AssertionError('`figure` should be either `AttackerFigure` or `DefenderFigure` type')

    for one_end, other_end in (((-1, 0), (1, 0)), ((0, 1), (0, -1))):
        one_end_cell = figure.i + one_end[0], figure.j + one_end[1]
        other_end_cell = figure.i + other_end[0], figure.j + other_end[1]

        one_end_cell_on_board = 0 <= one_end_cell[0] < 9 and 0 <= one_end_cell[1] < 9
        other_end_cell_on_board = 0 <= other_end_cell[0] < 9 and 0 <= other_end_cell[1] < 9

        if one_end_cell_on_board and other_end_cell_on_board:
            blocked_one_end = check_cell(board[one_end_cell[0]][one_end_cell[1]], opposite_type)
            blocked_other_end = check_cell(board[other_end_cell[0]][other_end_cell[1]], opposite_type)

            if blocked_one_end and blocked_other_end:
                # delete figure
                return


def check_cell(cell, opposite_type):
    return type(cell) == ExitCell or type(cell) == ThroneCell or (cell.figure and type(cell.figure) == opposite_type)


def check_king(king):
    pass

attackers = [
    AttackerFigure(0, 3),
    AttackerFigure(0, 4),
    AttackerFigure(0, 5),
    AttackerFigure(1, 4),
    AttackerFigure(3, 0),
    AttackerFigure(3, 8),
    AttackerFigure(4, 0),
    AttackerFigure(4, 1),
    AttackerFigure(4, 7),
    AttackerFigure(4, 8),
    AttackerFigure(5, 0),
    AttackerFigure(5, 8),
    AttackerFigure(7, 4),
    AttackerFigure(8, 3),
    AttackerFigure(8, 4),
    AttackerFigure(8, 5),
]

defenders = [
    DefenderFigureSoldier(2, 4),
    DefenderFigureSoldier(3, 4),
    DefenderFigureSoldier(4, 2),
    DefenderFigureSoldier(4, 3),
    DefenderFigureSoldier(4, 5),
    DefenderFigureSoldier(4, 6),
    DefenderFigureSoldier(5, 4),
    DefenderFigureSoldier(6, 4),
]

king = DefenderFigureKing(4, 4, move_limit=3)

board = [
    [ExitCell(), PlainCell(), PlainCell(), PlainCell(attackers[0]), PlainCell(attackers[1]), PlainCell(attackers[2]), PlainCell(), PlainCell(), ExitCell()],
    [PlainCell(), PlainCell(), PlainCell(), PlainCell(), PlainCell(attackers[3]), PlainCell(), PlainCell(), PlainCell(), PlainCell()],
    [PlainCell(), PlainCell(), PlainCell(), PlainCell(), PlainCell(defenders[0]), PlainCell(), PlainCell(), PlainCell(), PlainCell()],
    [PlainCell(attackers[4]), PlainCell(), PlainCell(), PlainCell(), PlainCell(defenders[1]), PlainCell(), PlainCell(), PlainCell(), PlainCell(attackers[5])],
    [PlainCell(attackers[6]), PlainCell(attackers[7]), PlainCell(defenders[2]), PlainCell(defenders[3]), ThroneCell(king), PlainCell(defenders[4]), PlainCell(defenders[5]), PlainCell(attackers[8]), PlainCell(attackers[9])],
    [PlainCell(attackers[10]), PlainCell(), PlainCell(), PlainCell(), PlainCell(defenders[6]), PlainCell(), PlainCell(), PlainCell(), PlainCell(attackers[11])],
    [PlainCell(), PlainCell(), PlainCell(), PlainCell(), PlainCell(defenders[7]), PlainCell(), PlainCell(), PlainCell(), PlainCell()],
    [PlainCell(), PlainCell(), PlainCell(), PlainCell(), PlainCell(attackers[12]), PlainCell(), PlainCell(), PlainCell(), PlainCell()],
    [ExitCell(), PlainCell(), PlainCell(), PlainCell(attackers[13]), PlainCell(attackers[14]), PlainCell(attackers[15]), PlainCell(), PlainCell(), ExitCell()],
]


if __name__ == '__main__':
    # 1 Расставить фигуры
    print_board(board)

    # 2 Рассчитать возможные ходы
    get_all_possible_moves(attackers + defenders + [king], board)

    # 3 Сделать ход
    make_move()

    # 4 Съесть фигуры
    check_board(board)
    # todo проверить условия выигрыша
    # todo запустить функцию оценки
    # todo включить условие выигрыша в функцию оцеки ??
