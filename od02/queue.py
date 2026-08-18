"""Урок od02. Очередь (Queue): на списке и на collections.deque.

Очередь — структура данных с дисциплиной FIFO (first in, first out:
первым пришёл — первым ушёл). Элементы входят с одного конца
(хвост очереди), а выходят с другого (голова). Аналогия — обычная
очередь в магазине.

Здесь две реализации с одинаковым контрактом:

* QueueOnList  — на списке, как показывали на уроке. Работает верно,
  но enqueue стоит O(n): списку нужны оба конца, а дёшев у него
  только правый.
* QueueOnDeque — на collections.deque, у которого дёшевы оба конца.
  Обе операции за O(1); именно так очередь делают в реальном коде.

Демоблок показывает, что поведение классов одинаковое, а скорость — нет.
"""

from collections import deque
from time import perf_counter


class QueueOnList:
    """Очередь на списке (схема с урока).

    Список хранит очередь «задом наперёд»: хвост — слева (индекс 0),
    голова — справа (конец списка). Новичок вставляется в начало
    списка, обслуживание снимает с конца.

    Цена: insert(0, ...) сдвигает ВСЕ элементы списка на позицию
    вправо, это O(n) на каждый enqueue. dequeue при этом дешёвый, O(1).
    (Зеркальный вариант append + pop(0) просто перекладывает O(n)
    из enqueue в dequeue — списку всё равно, какой конец «дорогой».)

    dequeue и peek на пустой очереди бросают IndexError.
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        """Поставить элемент в хвост очереди. O(n)."""
        self.items.insert(0, item)

    def dequeue(self):
        """Обслужить голову очереди: снять первый вошедший элемент. O(1)."""
        return self.items.pop()

    def peek(self):
        """Подсмотреть голову очереди, не снимая элемента."""
        return self.items[-1]

    def size(self):
        return len(self.items)


class QueueOnDeque:
    """Очередь на collections.deque — правильный инструмент задачи.

    deque (double-ended queue, «дек») внутри устроен как цепочка
    блоков, поэтому добавление и снятие О(1) с ОБОИХ концов.
    Храним очередь в естественном порядке: голова — слева,
    хвост — справа.

    dequeue и peek на пустой очереди бросают IndexError.
    """

    def __init__(self):
        self.items = deque()

    def is_empty(self):
        return not self.items

    def enqueue(self, item):
        """Поставить элемент в хвост очереди. O(1)."""
        self.items.append(item)

    def dequeue(self):
        """Обслужить голову очереди. O(1) — снятие слева, popleft."""
        return self.items.popleft()

    def peek(self):
        """Подсмотреть голову очереди, не снимая элемента."""
        return self.items[0]

    def size(self):
        return len(self.items)


def race(n, *queue_classes):
    """Гонка реализаций очереди: прогнать n элементов через каждую."""
    print(f"\nГонка на {n} элементах:")
    for queue_class in queue_classes:
        q = queue_class()
        start = perf_counter()
        for x in range(n):
            q.enqueue(x)
        while not q.is_empty():
            q.dequeue()
        elapsed = perf_counter() - start
        print(f"  {queue_class.__name__:<13} {elapsed:.3f} c")


if __name__ == "__main__":
    # Демонстрация 1: дисциплина FIFO.
    print("Очередь на списке. Входят: 'первый', 'второй', 'третий'")
    q = QueueOnList()
    for item in ["первый", "второй", "третий"]:
        q.enqueue(item)

    print(f"Размер: {q.size()}, у кассы: «{q.peek()}»")
    print("Обслуживаем всех:")
    while not q.is_empty():
        print(f"  dequeue() -> «{q.dequeue()}»")

    # Демонстрация 2: обе реализации ведут себя одинаково.
    источники = list(range(10))
    ql, qd = QueueOnList(), QueueOnDeque()
    for x in источники:
        ql.enqueue(x)
        qd.enqueue(x)
    из_списка = [ql.dequeue() for _ in range(ql.size())]
    из_дека = [qd.dequeue() for _ in range(qd.size())]
    print(f"\nВошло:          {источники}")
    print(f"QueueOnList  -> {из_списка}")
    print(f"QueueOnDeque -> {из_дека}")
    print(f"Результаты совпали: {из_списка == из_дека}")

    # Демонстрация 3: цена O(n) против O(1) на живых числах.
    # Прогоняем через каждую очередь n элементов и меряем время.
    # Вторая гонка вчетверо больше первой: у дека время вырастет ~в 4
    # раза (линия), у списка ~в 16 (квадрат).
    race(50_000, QueueOnList, QueueOnDeque)
    race(200_000, QueueOnList, QueueOnDeque)
