import unittest
import generator
import solver
import classes
import drawer


class TestGenerator(unittest.TestCase):
    """Класс тестирует модуль generator"""

    def test_generator(self):
        """Метод тестирует метод generate_field"""
        ns = [2, 3, 5, 6, 7, 10, 11, 13]
        for n in ns:
            field, areas = generator.generate_field(n)
            GeneralTestMethods().check_if_validate(areas, field)
            drawer.draw_field_ascii(field)
            drawer.draw_field_with_symbols(field)
            field.set_areas(areas)
            drawer.draw_field_ascii(field)
            drawer.draw_symbols_in_areas(field)


class TestSolver(unittest.TestCase):
    """Класс тестирует модуль solver"""

    def test_get_next_figure(self):
        """Метод тетсирует метод get_next_figure"""
        field = classes.Field(2)
        field.sets_cells_with_number({classes.Cell(0, 0): 1,
                                      classes.Cell(1, 0): 3})
        fields = list(solver.get_next_figure(field, {classes.Cell(0, 0),
                                                     classes.Cell(1, 0)},
                                             0, 0))
        self.assertEqual(9, len(fields))

    def test_solver(self):
        """Метод тестирует метод solve"""
        tests = [classes.Field(2), classes.Field(3)]
        tests[0].sets_cells_with_number({classes.Cell(0, 0): 3,
                                         classes.Cell(1, 0): 3,
                                         classes.Cell(1, 2): 1})
        tests[1].sets_cells_with_number({classes.Cell(0, 0): 4,
                                         classes.Cell(1, 1): 4,
                                         classes.Cell(2, 2): 4,
                                         classes.Cell(1, 0): 1,
                                         classes.Cell(2, 3): 3,
                                         classes.Cell(2, 4): 3,
                                         classes.Cell(2, 0): 1})
        for field in tests:
            drawer.draw_field_ascii(field)
            drawer.draw_field_with_symbols(field)
            field = solver.solve(field)
            GeneralTestMethods().check_if_validate(field.areas, field)
            drawer.draw_field_ascii(field)
            drawer.draw_symbols_in_areas(field)

    def test_select_areas(self):
        """Метод тестирует метод select_areas"""
        field = classes.Field(3)
        field.sets_cells_with_number({classes.Cell(0, 0): 1,
                                      classes.Cell(1, 0): 2,
                                      classes.Cell(1, 1): 4,
                                      classes.Cell(1, 2): 4,
                                      classes.Cell(2, 0): 2,
                                      classes.Cell(2, 1): 2,
                                      classes.Cell(2, 2): 2,
                                      classes.Cell(2, 3): 4,
                                      classes.Cell(2, 4): 4})
        self.assertIsNone(solver.select_areas(field))
        field.sets_cells_with_number({classes.Cell(0, 0): 1,
                                      classes.Cell(1, 0): 2,
                                      classes.Cell(1, 1): 3,
                                      classes.Cell(1, 2): 4,
                                      classes.Cell(2, 0): 3,
                                      classes.Cell(2, 1): 4,
                                      classes.Cell(2, 2): 2,
                                      classes.Cell(2, 3): 1,
                                      classes.Cell(2, 4): 3})
        self.assertIsNone(solver.select_areas(field))
        field.sets_cells_with_number({classes.Cell(0, 0): 1,
                                      classes.Cell(1, 0): 3,
                                      classes.Cell(1, 1): 3,
                                      classes.Cell(1, 2): 2,
                                      classes.Cell(2, 0): 2,
                                      classes.Cell(2, 1): 2,
                                      classes.Cell(2, 2): 1,
                                      classes.Cell(2, 3): 2,
                                      classes.Cell(2, 4): 1})
        self.assertIsNone(solver.select_areas(field))
        field.sets_cells_with_number({classes.Cell(0, 0): 3,
                                      classes.Cell(1, 0): 3,
                                      classes.Cell(1, 1): 3,
                                      classes.Cell(1, 2): 4,
                                      classes.Cell(2, 0): 2,
                                      classes.Cell(2, 1): 2,
                                      classes.Cell(2, 2): 4,
                                      classes.Cell(2, 3): 4,
                                      classes.Cell(2, 4): 4})
        self.assertEqual([
            classes.Area(cells=[classes.Cell(0, 0),
                                classes.Cell(1, 0), classes.Cell(1, 1)]),
            classes.Area(cells=[classes.Cell(1, 2), classes.Cell(2, 2),
                                classes.Cell(2, 3), classes.Cell(2, 4)]),
            classes.Area(cells=[classes.Cell(2, 0), classes.Cell(2, 1)])],
            solver.select_areas(field))

    def test_check_if_ok(self):
        """Метод тестирует метод check_if_ok"""
        areas = [classes.Area(cells=[classes.Cell(0, 0),
                                     classes.Cell(1, 1),
                                     classes.Cell(1, 2)])]
        cells = [classes.Cell(0, 0), classes.Cell(2, 0), classes.Cell(2, 1)]
        figure_false_areas = [classes.Cell(2, 0), classes.Cell(1, 1)]
        figure_false_cells_0 = [classes.Cell(1, 0), classes.Cell(2, 2)]
        figure_true = [classes.Cell(2, 0), classes.Cell(3, 1)]
        self.assertTrue(solver.check_if_ok(areas, cells, figure_true))
        self.assertFalse(solver.check_if_ok(areas, cells,
                                            figure_false_cells_0))
        self.assertFalse(solver.check_if_ok(areas, cells,
                                            figure_false_areas))


class GeneralTestMethods(unittest.TestCase):
    """Класс сожержит вспомогательные методы тестирования"""

    def check_if_linked(self, cells):
        """Метод проверяет список клеток на связность"""
        prev_cell = None
        for cell in cells:
            if prev_cell is not None:
                self.assertTrue(abs(cell.layer - prev_cell.layer) == 1 or
                                cell.layer == prev_cell.layer)
                self.assertTrue(abs(cell.place - prev_cell.place) == 1)
                self.assertTrue(0 < (abs(cell.place - prev_cell.place) +
                                     abs(cell.layer - prev_cell.layer)) < 3)
            prev_cell = cell

    def check_if_validate(self, areas, field):
        """Метод проверяет корректность найденого решения areas поля field"""
        n = field.n
        cells_in_areas = set()
        cells_with_number = set()
        cells_and_areas = dict()
        for area in areas:
            self.assertFalse(len(area.cells) == 0)
            self.assertFalse(len(area.cells) > field.n * field.n)
            self.check_if_linked(area.cells)
            cells = set()
            for cell in area.cells:
                self.assertFalse(cell in cells_in_areas)
                cells_in_areas.add(cell)
                self.assertFalse(cell in cells)
                cells.add(cell)
                cells_and_areas[cell] = area
                if field.areas:
                    self.assertEqual(len(area.cells), cell.number)
                elif cell in field.cells_with_number:
                    self.assertEqual(len(area.cells), cell.number)
                else:
                    self.assertEqual(0, cell.number)
            self.assertTrue(1 <= len(area.cells_with_number) <=
                            len(area.cells))
            for cell in area.cells_with_number:
                self.assertFalse(cell in cells_with_number)
                cells_with_number.add(cell)
            self.assertEqual(len(area.cells), len(cells))
        self.assertEqual(n * n, len(cells_in_areas))
        for t in range(n):
            for s in range(t * 2 + 1):
                cell = field.cells[t][s]
                self.assertTrue(cell in cells_in_areas)
        for cell in field.cells_with_number.keys():
            count = 0
            cell_area = None
            for area in areas:
                if cell in area.cells:
                    count += 1
                    if cell_area:
                        self.assertEqual(cell_area, area)
                    cell_area = area
                    self.assertEqual(field.cells_with_number[cell],
                                     len(cell_area.cells))
                    self.assertTrue(cell in cell_area.cells_with_number)
            self.assertTrue(1 <= count <= len(cell_area.cells))
        self.assertEqual(len(field.cells_with_number), len(cells_with_number))
        for cell in cells_with_number:
            self.assertTrue(cell in field.cells_with_number)
        for i in range(n):
            for j in range(2 * i + 1):
                cell = classes.Cell(i, j)
                for value in classes.direction_dictionary.values():
                    new_layer = i + value[0]
                    new_place = j + value[1]
                    if (0 <= new_layer < n and 0 <= new_place < 2 *
                            new_layer + 1):
                        new_cell = classes.Cell(new_layer, new_place)
                        area = cells_and_areas[cell]
                        new_area = cells_and_areas[new_cell]
                        if area != new_area:
                            self.assertFalse(len(area.cells) ==
                                             len(new_area.cells))
