"""Модуль находит решение заданного поля и выбрасиывает исключение,
если решения не существует"""

import argparse
import classes
import copy
import pickle
import queue
import sys
from multiprocessing import Pool


def solve(field_to_solve):
    """Метод находит решение"""
    if field_to_solve.cells_with_number is None or field_to_solve.areas:
        raise ValueError
    cells_without_numbers = select_cells_zones_without_numbers(field_to_solve)
    with Pool(5) as p:
        for area in cells_without_numbers:
            a = p.apply_async(task_for_worker,
                              args=(field_to_solve, area,
                                    max(field_to_solve
                                        .cells_with_number.values()) +
                                    1)).get()
            if a is None:
                print(area)
            for c in a.cells:
                field_to_solve.cells[c.layer][c.place] = c
        total_areas = select_areas(field_to_solve)
    if total_areas is None:
        raise ValueError("We can't solve")
    field_to_solve.set_areas(total_areas)
    return field_to_solve


def task_for_worker(f, area, n):
    for figure in get_next_figure(area, set(), 0, n):
        areas = select_areas(f)
        if areas is not None:
            return figure


def select_cells_zones_without_numbers(f: classes.Field):
    """Метод возвращает все связные области пустых клеток в порядке 
    возрастания размеров области"""
    cells_without_number = []
    visited = set()
    n = f.n
    for i in range(n):
        for j in range(i * 2 + 1):
            cell = f.cells[i][j]
            if cell.number == 0 and cell not in visited:
                cells_without_number.append(select_area(visited, f, cell))
    cells_without_number_sorted = sorted(cells_without_number,
                                         key=lambda area: len(area),
                                         reverse=True)
    return cells_without_number_sorted


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
                continue
            number = cell.number
            current_area = classes.Area()
            empty_neibs = 0
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
                    if new_cell.number == 0:
                        empty_neibs += 1
                    if new_cell.number == number:
                        current_area.add_cell(new_cell)
                        visited_cells.add(new_cell)
                        open_area = True
            if ((len(current_area) == number or
                 empty_neibs > 0 and
                 len(current_area) + empty_neibs <= number) and
                    check_if_ok(areas, set(f.cells_with_number.keys()),
                                current_area.cells)):
                areas.append(current_area)
            else:
                return None
    return areas


def select_area(visited, f, cell):
    """Метод выбирает связную область пустых клеток"""
    area = classes.Area()
    n = f.n
    area.add_cell(cell)
    cells_for_check = queue.Queue()
    cells_for_check.put(cell)
    visited.add(cell)
    while not cells_for_check.empty():
        c = cells_for_check.get()
        x = c.layer
        y = c.place
        for di, dj in classes.direction_dictionary.values():
            if (x + di < 0 or x + di >= n or
                    y + dj < 0 or y + dj >= 2 * (x + di) + 1):
                continue
            new_cell = f.cells[x + di][y + dj]
            if new_cell in visited:
                continue
            if new_cell.number == 0:
                area.add_cell(new_cell)
                visited.add(new_cell)
                cells_for_check.put(new_cell)
    return area


def get_next_figure(area, cells_with_number, x, n):
    """Метод расставляет цифры в пустых клетках"""
    if len(area) <= x:
        yield area
    elif area.cells[x] in cells_with_number:
        yield from get_next_figure(area, cells_with_number, x + 1, n)
    else:
        cell = area.cells[x]
        cells_with_number.add(cell)
        for index in range(1, n):
            cell.set_number(index)
            yield from get_next_figure(area,
                                       copy.deepcopy(cells_with_number), 
                                       x + 1, n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Находит решение
    заданного поля и выбрасиывает исключение, если решения не существует,
    на вход принимает головоломку''')
    field = pickle.loads(sys.stdin.read().encode())
    sys.stdout.buffer.write(pickle.dumps(solve(field), 0))
