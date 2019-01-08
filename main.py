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
    def __init__(self, coordinate, move_limit=None):
        self.coordinate = coordinate
        self.move_limit = move_limit
        self.possible_cells = []
        self.danger_cells = []
        self.possible_moves = []
        self.opposite_type = None
        self.active = True

    def get_possible_moves(self, board):
        self.possible_moves = []
        for modifier in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            i, j = self.coordinate
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

    def check_neighbours(self, board, both_lines=False):
        blocks = []

        left_right_cells = (-1, 0), (1, 0)
        top_bottom_cells = (0, 1), (0, -1)

        for one_end, other_end in (left_right_cells, top_bottom_cells):
            one_end_cell = self.coordinate[0] + one_end[0], self.coordinate[1] + one_end[1]
            other_end_cell = self.coordinate[0] + other_end[0], self.coordinate[1] + other_end[1]

            is_one_end_cell_on_board = 0 <= one_end_cell[0] < 9 and 0 <= one_end_cell[1] < 9
            is_other_end_cell_on_board = 0 <= other_end_cell[0] < 9 and 0 <= other_end_cell[1] < 9

            if is_one_end_cell_on_board and is_other_end_cell_on_board:
                is_blocked_one_end = self._check_cell(
                    board[one_end_cell[0]][one_end_cell[1]], self.danger_cells, self.opposite_type)
                is_blocked_other_end = self._check_cell(
                    board[other_end_cell[0]][other_end_cell[1]], self.danger_cells, self.opposite_type)

                if is_blocked_one_end and is_blocked_other_end:
                    blocks.append(True)

        if both_lines:
            self.active = all(blocks)
        else:
            self.active = any(blocks)

    @staticmethod
    def _check_cell(cell, danger_cells, opposite_type):
        is_danger_cell = type(cell) in danger_cells
        is_enemy_on_cell = cell.figure and type(cell.figure) == opposite_type
        return is_danger_cell or is_enemy_on_cell


class AttackerFigure(Figure):
    """Атакующий солдат"""
    def __init__(self, coordinate, move_limit=None):
        super().__init__(coordinate, move_limit)
        self.possible_cells.extend([PlainCell])
        self.danger_cells.extend([ExitCell, ThroneCell])
        self.opposite_type = DefenderFigure

    def __str__(self):
        return '!!'

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate


class DefenderFigure(Figure):
    """Защищающийся абстрактный"""
    def __init__(self, coordinate, move_limit=None):
        super().__init__(coordinate, move_limit)
        self.opposite_type = AttackerFigure


class DefenderFigureSoldier(DefenderFigure):
    """Защищающийся солдат"""
    def __init__(self, coordinate, move_limit=None):
        super().__init__(coordinate, move_limit)
        self.possible_cells.extend([PlainCell])
        self.danger_cells.extend([ExitCell, ThroneCell])

    def __str__(self):
        return '{}'

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate


class DefenderFigureKing(DefenderFigure):
    """Защищающийся князь"""
    def __init__(self, coordinate, move_limit=None):
        super().__init__(coordinate, move_limit)
        self.possible_cells.extend([PlainCell, ThroneCell, ExitCell])

    def __str__(self):
        return '**'

    def set_coordinate(self, coordinate):
        self.coordinate = coordinate
        if self.coordinate in ((4, 4), (4, 3), (3, 4), (4, 5), (5, 4)):
            self.danger_cells.extend([ThroneCell])
        else:
            self.danger_cells.extend([ExitCell])

    def check_neighbours(self, board, both_lines=False):
        if self.coordinate in ((4, 4), (4, 3), (3, 4), (4, 5), (5, 4)):
            super().check_neighbours(board, both_lines=True)
        else:
            super().check_neighbours(board, both_lines=False)


# Функции
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
    board[to_i][to_j].figure.set_coordinates((to_i, to_j))
    board[from_i][from_j].figure = None


def check_board(figure_type, board):
    if figure_type == AttackerFigure:
        for attacker in attackers:
            attacker.check_neighbours(board)

    elif figure_type == DefenderFigureSoldier:
        king.check_neighbours(board)
        for defender in defenders:
            defender.check_neighbours(board)


attackers = [
    AttackerFigure((0, 3)),
    AttackerFigure((0, 4)),
    AttackerFigure((0, 5)),
    AttackerFigure((1, 4)),
    AttackerFigure((3, 0)),
    AttackerFigure((3, 8)),
    AttackerFigure((4, 0)),
    AttackerFigure((4, 1)),
    AttackerFigure((4, 7)),
    AttackerFigure((4, 8)),
    AttackerFigure((5, 0)),
    AttackerFigure((5, 8)),
    AttackerFigure((7, 4)),
    AttackerFigure((8, 3)),
    AttackerFigure((8, 4)),
    AttackerFigure((8, 5)),
]

defenders = [
    DefenderFigureSoldier((2, 4)),
    DefenderFigureSoldier((3, 4)),
    DefenderFigureSoldier((4, 2)),
    DefenderFigureSoldier((4, 3)),
    DefenderFigureSoldier((4, 5)),
    DefenderFigureSoldier((4, 6)),
    DefenderFigureSoldier((5, 4)),
    DefenderFigureSoldier((6, 4)),
]

king = DefenderFigureKing((4, 4), move_limit=3)

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
    check_board(DefenderFigureSoldier, board)
    # todo проверить условия выигрыша
    # todo запустить функцию оценки
    # todo включить условие выигрыша в функцию оцеки ??
