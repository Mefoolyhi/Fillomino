**Игра "Fillomino"**

Автор: Габдорахманова Елена

Примеры запуска: 
generator.py --size 3 --solution solve.txt | solver.py | drawer.py -f ascii

generator.py [--size SIZE] [--solution SOLUTION]
По числу size и строке solution строит поле размера size и записывает эталонное
решение в [solution].txt

solver.py
Находит решение заданного поля и выбрасывает исключение, если решения не
существует, на вход принимает головоломку

drawer.py [--format {ascii,colored}]
Визуализирует заданное поле и заданные решения в заданном формате