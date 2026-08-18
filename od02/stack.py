"""Урок od02. Стек (Stack) на основе списка.

Стек — структура данных с дисциплиной LIFO (last in, first out:
последним пришёл — первым ушёл). Все операции работают только
с одним концом — вершиной стека. Аналогия: стопка тарелок,
кладём сверху и берём сверху.

Списку Python дёшево (за O(1)) даются операции с его правым концом —
append() и pop(), — поэтому правый конец списка и назначен вершиной.
"""


class Stack:
    """Стек с контрактом из четырёх базовых операций + size.

    Снятие или подглядывание на пустом стеке — ошибка использования:
    pop() и peek() честно падают с IndexError, как их списочные
    прообразы. Перед вызовом стоит проверять is_empty().
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        """Пуст ли стек. Пустой список в Python «ложен», поэтому not."""
        return not self.items

    def push(self, item):
        """Положить элемент на вершину стека."""
        self.items.append(item)

    def pop(self):
        """Снять элемент с вершины стека и вернуть его."""
        return self.items.pop()

    def peek(self):
        """Подсмотреть вершину стека, не снимая элемента."""
        return self.items[-1]

    def size(self):
        """Количество элементов в стеке."""
        return len(self.items)


if __name__ == "__main__":
    # Демонстрация 1: дисциплина LIFO в чистом виде.
    stack = Stack()
    top = "—" if stack.is_empty() else stack.peek()
    print(f"Размер стека: {stack.size()}, на вершине: «{top}»")

    print("Кладём в стек по очереди: 'первый', 'второй', 'третий'")
    for item in ["первый", "второй", "третий"]:
        stack.push(item)

    print(f"Размер стека: {stack.size()}, на вершине: «{stack.peek()}»")

    print("Снимаем всё до опустошения:")
    while not stack.is_empty():
        print(f"  pop() -> «{stack.pop()}»")
    print(f"Стек пуст: {stack.is_empty()}")

    # Демонстрация 2: мини-применение — разворот строки.
    # Символы входят в стек в прямом порядке, а выходят в обратном:
    # LIFO разворачивает последовательность сам, без всяких срезов.
    # (В od01 мы разворачивали строку срезом [::-1] — вот его механика
    # «вручную».)
    word = "алгоритм"
    letters = Stack()
    for ch in word:
        letters.push(ch)

    reversed_word = ""
    while not letters.is_empty():
        reversed_word += letters.pop()

    print(f"\nРазворот через стек: «{word}» -> «{reversed_word}»")
