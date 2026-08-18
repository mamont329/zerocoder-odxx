"""Урок od02. Граф (Graph) и его обходы — финал урока, где всё сходится.

Граф — множество вершин и рёбер между ними. Хранится в виде словаря
смежности: вершина -> список её соседей. Граф ненаправленный, поэтому
каждое ребро записывается в обе стороны.

Главный сюжет файла — обходы («посетить все вершины, шагая по рёбрам»).
В графе, в отличие от дерева, есть циклы, поэтому обходу нужны:
  * память о посещённых вершинах (set), иначе — вечное хождение по кругу;
  * хранилище «куда идти дальше» — и вот тут выстреливают структуры
    из начала урока:
      стек    -> DFS, обход ВГЛУБЬ (ныряем по ветке до упора)
      очередь -> BFS, обход В ШИРИНУ (расходимся от старта кругами)
    Код обходов одинаковый, отличается ТОЛЬКО структура хранения —
    выбор структуры данных определяет алгоритм.

Подопытный — граф с урока: «клуб карате Закари» (34 участника секции,
рёбра — дружба; после конфликта тренера (вершина 1) и президента (34)
клуб раскололся на два лагеря точно по структуре связей).
"""

from stack import Stack
from queue import QueueOnDeque


class Graph:
    """Ненаправленный граф на словаре смежности."""

    def __init__(self):
        self.adjacency = {}

    def add_vertex(self, vertex):
        """Добавить вершину (если её ещё нет)."""
        self.adjacency.setdefault(vertex, [])

    def add_edge(self, a, b):
        """Добавить ребро a—b. Граф ненаправленный: запись в обе стороны."""
        self.add_vertex(a)
        self.add_vertex(b)
        self.adjacency[a].append(b)
        self.adjacency[b].append(a)

    def neighbors(self, vertex):
        return self.adjacency[vertex]

    def vertex_count(self):
        return len(self.adjacency)

    def edge_count(self):
        """Рёбер вдвое меньше, чем записей: каждое записано с двух сторон."""
        return sum(len(adj) for adj in self.adjacency.values()) // 2

    def dfs(self, start):
        """Обход вглубь (depth-first search) на явном стеке.

        Снимаем вершину со стека; если ещё не посещена — посещаем
        и кладём в стек её соседей. LIFO выталкивает наверх свежих
        соседей, поэтому обход ныряет по ветке до упора и лишь потом
        возвращается к отложенным развилкам.

        (reversed при укладке соседей — только ради порядка «как в
        рекурсии»: первый в списке сосед обрабатывается первым.)
        """
        order = []
        visited = set()
        stack = Stack()
        stack.push(start)
        while not stack.is_empty():
            vertex = stack.pop()
            if vertex in visited:
                continue  # уже были: вершина попала в стек с двух развилок
            visited.add(vertex)
            order.append(vertex)
            for neighbor in reversed(self.neighbors(vertex)):
                if neighbor not in visited:
                    stack.push(neighbor)
        return order

    def bfs(self, start):
        """Обход в ширину (breadth-first search) на очереди.

        Тот же цикл, что у dfs, но хранилище — FIFO: соседи
        обрабатываются в порядке обнаружения, поэтому обход расходится
        от старта «кругами» — сначала все вершины в одном шаге,
        потом в двух, и так далее.
        """
        order = []
        visited = {start}
        queue = QueueOnDeque()
        queue.enqueue(start)
        while not queue.is_empty():
            vertex = queue.dequeue()
            order.append(vertex)
            for neighbor in self.neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
        return order


# Рёбра графа Закари (34 вершины, 78 рёбер дружбы).
ZACHARY_EDGES = [
    (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9),
    (1, 11), (1, 12), (1, 13), (1, 14), (1, 18), (1, 20), (1, 22), (1, 32),
    (2, 3), (2, 4), (2, 8), (2, 14), (2, 18), (2, 20), (2, 22), (2, 31),
    (3, 4), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29), (3, 33),
    (4, 8), (4, 13), (4, 14), (5, 7), (5, 11), (6, 7), (6, 11), (6, 17),
    (7, 17), (9, 31), (9, 33), (9, 34), (10, 34), (14, 34), (15, 33),
    (15, 34), (16, 33), (16, 34), (19, 33), (19, 34), (20, 34), (21, 33),
    (21, 34), (23, 33), (23, 34), (24, 26), (24, 28), (24, 30), (24, 33),
    (24, 34), (25, 26), (25, 28), (25, 32), (26, 32), (27, 30), (27, 34),
    (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 33), (31, 34),
    (32, 33), (32, 34), (33, 34),
]


if __name__ == "__main__":
    # Демонстрация 1: маленький граф, где разница обходов видна глазами.
    #
    #     A --- B --- D
    #     |           |
    #     C --- E     F
    #      \         /
    #       ---------
    small = Graph()
    for a, b in [("A", "B"), ("A", "C"), ("B", "D"), ("C", "E"),
                 ("D", "F"), ("E", "F")]:
        small.add_edge(a, b)

    print("Маленький граф (A и F соединены двумя путями — есть цикл):")
    print(f"  DFS от A: {small.dfs('A')}   <- нырнул через B до F, потом хвосты")
    print(f"  BFS от A: {small.bfs('A')}   <- кругами: сосед A, соседи соседей...")

    # Демонстрация 2: клуб карате Закари.
    club = Graph()
    for a, b in ZACHARY_EDGES:
        club.add_edge(a, b)

    print(f"\nКлуб Закари: {club.vertex_count()} участников, "
          f"{club.edge_count()} дружеских связей")
    print(f"Друзей у тренера (1): {len(club.neighbors(1))}, "
          f"у президента (34): {len(club.neighbors(34))}")

    dfs_order = club.dfs(1)
    bfs_order = club.bfs(1)
    print(f"\nDFS от тренера: {dfs_order}")
    print(f"BFS от тренера: {bfs_order}")
    print(f"Оба обхода посетили всех: "
          f"{len(dfs_order) == len(bfs_order) == club.vertex_count()} "
          f"-> граф связный, клуб (пока) един")
