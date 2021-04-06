"""Модуль получает на вход поле и одно или несколько его решений, а также
параметр ascii (для отрисовки в ASCII Art стиле) или colored (для
отрисовки в виде закрашенных символами зон) и отрисовывает заданное поле и
все его заданные решения в заданном стиле (по умолчанию стиль - ASCII Art)"""


import classes
import argparse
import pickle
import sys


def draw_field_ascii(f):
    """Метод изображает поле в формате ASCII Art"""
    n = f.n
    max_numbers_count = len(str(n * n))
    max_length = ((n - 1) * 2 + 1) * (max_numbers_count + 1) + 1
    for i in range(f.n):
        layer = f.cells[i]
        output = []
        for cell in layer:
            if cell.place % 2 == 0:
                output.append("/")
            else:
                output.append("\\")
            if cell.number != 0:
                output.append(str(cell.number).rjust(max_numbers_count))
            else:
                output.append('_'.rjust(max_numbers_count))
        output.append("\\")
        print(''.join(output).center(max_length))
    print()


def draw_field_with_symbols(f):
    """Модуль изображает поле в стиле закрашенных символами зон"""
    n = f.n
    max_numbers_count = len(str(n * n)) + 1
    max_length = ((n - 1) * 2 + 1) * max_numbers_count
    for i in range(f.n):
        layer = f.cells[i]
        output = []
        for cell in layer:
            if cell in f.cells_with_number.keys():
                output.append(str(f.cells_with_number[cell])
                              .rjust(max_numbers_count))
            else:
                output.append("-".rjust(max_numbers_count))
        print(''.join(output).center(max_length))
    print()


def draw_symbols_in_areas(f):
    """Метод изображает решение, раскрашивая зоны символами"""
    n = f.n
    max_length = (n - 1) * 2 + 1
    symbols = ['*', '$', '@', '#', '&']
    cells = dict()
    areas_near_symbols = dict()
    areas = f.areas
    for area in areas:
        for cell in area.cells:
            cells[cell] = area

    for i in range(n):
        output = []
        for j in range(2 * i + 1):
            cell = classes.Cell(i, j)
            area = cells[cell]
            if area.background is None:
                prohibited_indexes = areas_near_symbols.get(area, None)
                if prohibited_indexes is None:
                    area.background = symbols[0]
                    mark_prohibited_symbols(n, area, areas_near_symbols, cells)
                else:
                    for s in symbols:
                        if s not in prohibited_indexes:
                            area.background = s
                            mark_prohibited_symbols(n, area,
                                                    areas_near_symbols, cells)
                            break
            output.append(area.background)
        print(''.join(output).center(max_length))
    print()


def mark_prohibited_symbols(n, area, areas_near_symbols, cells):
    for cell in area.cells:
        for value in classes.direction_dictionary.values():
            new_layer = cell.layer + value[0]
            new_place = cell.place + value[1]
            if 0 <= new_layer < n and 0 <= new_place < 2 * new_layer + 1:
                new_cell = classes.Cell(new_layer, new_place)
                new_area = cells[new_cell]
                if new_area != area:
                    if areas_near_symbols.get(new_area, None) is None:
                        areas_near_symbols[new_area] = set()
                    areas_near_symbols[new_area].add(area.background)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Визуализирует заданное
    поле и заданные решения в заданном формате''')
    parser.add_argument('--format', '-f', type=str,
                        choices=['ascii', 'colored'], default='ascii',
                        help='Формат отображения')
    args = parser.parse_args()
    field = pickle.loads(sys.stdin.read().encode())
    if args.format == "ascii":
        draw_field_ascii(field)
    elif field.areas:
        draw_symbols_in_areas(field)
    else:
        draw_field_with_symbols(field)
