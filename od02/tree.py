"""Урок od02. Дерево (Tree) — иерархическая структура из узлов.

Дерево определяется рекурсивно: это узел-корень плюс набор
дочерних ДЕРЕВЬЕВ (каждый ребёнок — сам корень своего поддерева).
Базовый случай — лист: дерево из одного узла без детей.

Из-за рекурсивного определения все операции над деревом пишутся
рекурсией по одной и той же схеме, что и факториал (n! = n*(n-1)!
с базой 0! = 1): «обработай узел сам + рекурсивно детей», база — лист.

Здесь общее (не бинарное) дерево: детей у узла сколько угодно.
Пример — структура каталогов нашего репозитория.
"""


class TreeNode:
    """Узел дерева: значение и список детей.

    Отдельного класса «Tree» не нужно: любой узел — это уже дерево
    (он корень своего поддерева). Держишь ссылку на корень — держишь
    всё дерево.
    """

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child_node):
        """Подвесить готовый узел ребёнком и вернуть его.

        Возврат ребёнка позволяет строить дерево в одну строку:
        node = root.add_child(TreeNode("подпапка"))
        """
        self.children.append(child_node)
        return child_node

    def is_leaf(self):
        """Лист ли это: узел без детей (базовый случай рекурсий)."""
        return not self.children

    def size(self):
        """Число узлов в поддереве: сам узел + размеры детских поддеревьев.

        Рекурсия: size(лист) = 1; size(узел) = 1 + сумма size(детей).
        """
        return 1 + sum(child.size() for child in self.children)

    def height(self):
        """Высота поддерева: этажи от этого узла до самого дальнего листа.

        Рекурсия: height(лист) = 0; height(узла) = 1 + максимум из
        высот детей (самая длинная ветка и определяет высоту).
        """
        if self.is_leaf():
            return 0
        return 1 + max(child.height() for child in self.children)

    def print_tree(self, level=0):
        """Печать «лесенкой»: узел, затем рекурсивно детей с отступом.

        Параметр level — глубина текущего узла: сколько шагов рекурсии
        сделано от корня, столько и отступов.
        """
        print("    " * level + str(self.value))
        for child in self.children:
            child.print_tree(level + 1)


if __name__ == "__main__":
    # Строим дерево — структуру каталогов нашего репозитория.
    root = TreeNode("zerocoder-odxx/")

    od01 = root.add_child(TreeNode("od01/"))
    od01.add_child(TreeNode("palindrome.py"))

    od02 = root.add_child(TreeNode("od02/"))
    od02.add_child(TreeNode("stack.py"))
    od02.add_child(TreeNode("queue.py"))
    treepy = od02.add_child(TreeNode("tree.py"))
    treepy.add_child(TreeNode("tree.py child"))

    notes = root.add_child(TreeNode("notes/"))
    notes.add_child(TreeNode("gamma-function.html"))

    root.add_child(TreeNode(".gitignore"))

    print("Дерево каталогов:")
    root.print_tree()

    print(f"\nУзлов в дереве (size): {root.size()}")
    print(f"Высота дерева (height): {root.height()}")

    # Любой узел — сам себе дерево: те же операции у поддерева od02.
    print(f"\nПоддерево od02: размер {od02.size()}, высота {od02.height()}")
    od02.print_tree()

    # Лист — базовый случай: размер 1, высота 0.
    leaf = TreeNode("одинокий лист")
    print(f"\nЛист: size = {leaf.size()}, height = {leaf.height()}, "
          f"is_leaf = {leaf.is_leaf()}")
