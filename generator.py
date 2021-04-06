"""Модуль генерирует поля заданного размера. Параметром задается число
частей, на которое разбивается сторона равностороннего треугольного поля"""

import random
import classes
import argparse
import pickle
import sys


def generate_field(n):
    """Метод генерирует треугольное поле размера n*n и возвращает
    само поле и одно из решений головоломки на этом поле"""
    field = classes.Field(n)
    areas = []
    visited_cells = set()
    cells_in_area = 0
    cells_with_neibs = dict()
    for t in range(n):
        for s in range(t * 2 + 1):
            cell = field.cells[t][s]
            if cell not in visited_cells:
                area = classes.Area()
                m = random.randint(2, max((n - 2) * (n - 2), n, n * n -
                                          cells_in_area))
                while (cells_with_neibs.get(cell, None) and
                       m in cells_with_neibs[cell]):
                    min_m = min(cells_with_neibs[cell])
                    max_m = max(cells_with_neibs[cell])
                    if min_m > 1:
                        m = min_m - 1
                    elif max_m < n * n - cells_in_area - 1:
                        m = max_m + 1
                    else:
                        return generate_field(n)
                area.add_cell(cell)
                visited_cells.add(cell)
                c = cell
                for j in range(m - 1):
                    direction = random.randint(0,
                                               len(classes
                                                   .direction_dictionary) - 1)
                    new_layer = (classes.direction_dictionary[direction][0] +
                                 c.layer)
                    new_place = (classes.direction_dictionary[direction][1] +
                                 c.place)
                    attempts = 1
                    while (0 > new_layer or new_layer >= n or
                           0 > new_place or new_place >= new_layer * 2 + 1 or
                           (0 <= new_layer < n and
                            0 <= new_place < new_layer * 2 + 1 and
                            (field.cells[new_layer][new_place] in
                             visited_cells or
                             (cells_with_neibs.get(classes.Cell(
                                 new_layer, new_place), None) and
                             m in cells_with_neibs[classes.Cell(
                                         new_layer, new_place)])))):
                        direction = (direction + 1) % len(
                            classes.direction_dictionary)
                        attempts += 1
                        current_delta = classes.direction_dictionary[direction]
                        new_layer = (current_delta[0] +
                                     c.layer)
                        new_place = (current_delta[1] +
                                     c.place)
                        if attempts == len(classes.direction_dictionary) + 1:
                            m = len(area.cells)
                            while area.cells:
                                deleting = False
                                for cell in area.cells:
                                    if (cells_with_neibs.get(cell, None) and
                                            m in cells_with_neibs[cell]):
                                        visited_cells.remove(area.cells[-1])
                                        area.cells.pop()
                                        m -= 1
                                        deleting = True
                                        break
                                if not deleting:
                                    break
                            break
                    if m == 0:
                        return generate_field(n)
                    if attempts == len(classes.direction_dictionary) + 1:
                        break
                    c = field.cells[new_layer][new_place]
                    area.add_cell(c)
                    visited_cells.add(c)
                cells_in_area += m
                for cell in area.cells:
                    for value in classes.direction_dictionary.values():
                        new_cell = classes.Cell(cell.layer + value[0],
                                                cell.place + value[1])
                        if (0 <= new_cell.layer < n and
                                0 <= new_cell.place < new_cell.layer * 2 + 1):
                            if cells_with_neibs.get(new_cell, None) is None:
                                cells_with_neibs[new_cell] = set()
                            cells_with_neibs[new_cell].add(m)
                areas.append(area)

    cells_with_number = dict()
    for area in areas:
        numbers_count = random.randint(1, max(len(area.cells) - 1, 1))
        for i in range(numbers_count):
            index = random.randint(0, len(area.cells) - 1)
            while area.cells[index] in area.cells_with_number:
                index = (index + 1) % len(area.cells)
            area.set_cells_with_number(index)
            cells_with_number[area.cells[index]] = len(area.cells)
            area.cells[index].set_number(len(area.cells))
    field.sets_cells_with_number(cells_with_number)
    return field, areas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Генерирует
    равносторонние треугольные поля для головоломки Fillomino''')
    parser.add_argument('--size', '-n', type=int,
                        help='Количество частей, на которое разбивается'
                             ' сторона')
    parser.add_argument('--solution', '-s', type=str, default='solve.txt',
                        help='Путь к файлу, куда сохраняется оригинальное '
                             'решение найденного поля')
    args = parser.parse_args()
    generated_field, answer = generate_field(int(args.size))
    sys.stdout.buffer.write(pickle.dumps(generated_field, 0))
    generated_field.set_areas(answer)
    with open(args.solution, 'wb') as f:
        pickle.dump(generated_field, f, 0)
