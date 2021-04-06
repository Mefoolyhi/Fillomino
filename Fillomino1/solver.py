"""Модуль находит решение заданного поля и выбрасиывает исключение,
если решения не существует"""

import classes
import argparse
import pickle
import sys
import copy


def solve(field_to_solve):
    """Метод находит решение"""
    if field_to_solve.cells_with_number is None or field_to_solve.areas:
        raise ValueError
    cells_with_number = set(field_to_solve.cells_with_number.keys())
    for f in get_next_figure(field_to_solve, cells_with_number, 0, 0):
        areas = select_areas(f)
        if areas is not None:
            f.set_areas(areas)
            return f
    raise ValueError("We can't solve")


def select_areas(f):
    """Метод выделяет зоны на поле, если это возможно"""
    n = f.n
    areas = []
    visited_cells = set()
    for i in range(n):
        for j in range(i * 2 + 1):
            cell = f.cells[i][j]
            if cell in visited_cells:
                continue
            visited_cells.add(cell)
            if cell.number == 0:
                raise ValueError
            number = cell.number
            current_area = classes.Area()
            current_area.add_cell(cell)
            open_area = True
            index = 0
            while open_area and index < len(current_area.cells):
                x = current_area.cells[index].layer
                y = current_area.cells[index].place
                index += 1
                open_area = False
                for di, dj in classes.direction_dictionary.values():
                    if (x + di < 0 or x + di >= n or
                            y + dj < 0 or y + dj >= 2 * (x + di) + 1):
                        continue
                    new_cell = f.cells[x + di][y + dj]
                    if new_cell in visited_cells:
                        continue
                    if new_cell.number == number:
                        current_area.add_cell(new_cell)
                        visited_cells.add(new_cell)
                        open_area = True
            if (len(current_area) == number and
                    check_if_ok(areas, set(f.cells_with_number.keys()),
                                current_area.cells)):
                areas.append(current_area)
            else:
                return None
    return areas


def check_if_ok(areas, cells_with_number, figure):
    """Метод проверяет не конфликтует ли зона figure
    с другими уже установленными зонами"""
    for area in areas:
        cells = set(area.cells)
        for cell in figure:
            if cell in cells:
                return False
    count = 0
    for cell in figure:
        if cell in cells_with_number:
            count += 1
    if count == 0:
        return False
    return True


def get_next_figure(board, cells_with_number, x, y):
    """Метод расставляет цифры в пустых клетках"""
    n = board.n
    if x >= n:
        yield board
    else:
        i, j = x, y
        j += 1
        if j >= 2 * i + 1:
            i += 1
            j = 0
        if board.cells[x][y] in cells_with_number:
            yield from get_next_figure(board, cells_with_number, i, j)
        else:
            for index in range(1, n * n):
                board_copy = copy.deepcopy(board)
                board_copy.cells[x][y].set_number(index)
                yield from get_next_figure(board_copy, cells_with_number, i, j)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Находит решение
    заданного поля и выбрасиывает исключение, если решения не существует, 
    на вход принимает головоломку''')
    field = pickle.loads(sys.stdin.read().encode())
    sys.stdout.buffer.write(pickle.dumps(solve(field), 0))
