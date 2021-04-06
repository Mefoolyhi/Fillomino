"""Модуль содержит все классы, необходимые для работы"""


class Field:
    """Класс игрового поля"""

    def __init__(self, n):
        self.n = n
        self.cells = []
        for i in range(n):
            layer = []
            for j in range(i * 2 + 1):
                layer.append(Cell(i, j))
            self.cells.append(layer)
        self.cells_with_number = set()
        self.areas = None

    def sets_cells_with_number(self, cells_with_numbers):
        """Устанавливает клетки, в которых лежат цифры"""
        self.cells_with_number = cells_with_numbers
        for cell, value in cells_with_numbers.items():
            self.cells[cell.layer][cell.place].set_number(value)

    def set_areas(self, areas):
        """Устанавливает решение на поле"""
        self.areas = areas
        for area in areas:
            for i in range(len(area.cells)):
                if area.cells[i] in self.cells_with_number:
                    area.set_cells_with_number(i)
                area.cells[i].set_number(len(area.cells))


class Area:
    """Класс закрашенной одним цветом зоны"""

    def __init__(self, background=None, cells=None):
        if cells is None:
            cells = []
        self.cells = cells
        self.background = background
        self.cells_with_number = set()

    def __str__(self):
        s = []
        for cell in self.cells:
            s.append(str(cell))
        return '; '.join(s)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        first_set = set(self.cells)
        second_set = set(other.cells)
        if len(first_set) != len(second_set):
            return False
        for cell in first_set:
            if cell not in second_set:
                return False
        return True

    def __len__(self):
        return len(self.cells)

    def add_cell(self, cell):
        """Метод добавляет в зону новую клетку"""
        self.cells.append(cell)

    def set_cells_with_number(self, index):
        """Метод устанавливает клетки с номерами"""
        self.cells_with_number.add(self.cells[index])
        self.cells[index].set_number(len(self.cells))
    
    def find_cell(self, x, y):
        """Метод возвращает клетку по ее координатам"""
        etalon = Cell(x, y)
        for cell in self.cells:
            if etalon == cell:
                return cell
            

class Cell:
    """Класс клетки игрового поля"""

    def __init__(self, layer, place, number=0):
        self.layer = layer
        self.place = place
        self.number = number

    def set_number(self, index):
        self.number = index

    def __eq__(self, other):
        return self.place == other.place and self.layer == other.layer

    def __hash__(self):
        return self.layer * 2_971_215_073 + self.place

    def __str__(self):
        return f"Cell: {self.layer}, {self.place}, number: {self.number}"


"""Словарь для получения соседних клеток"""
direction_dictionary = {
    0: (-1, -1),
    1: (0, -1),
    2: (0, 1),
    3: (1, 1)
}
