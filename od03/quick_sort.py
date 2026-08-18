"""Урок od03. Быстрая сортировка (quicksort, Тони Хоар, 1959).

«Разделяй и властвуй»: выбираем опорный элемент (pivot), раскидываем
остальных на меньших и больших, опорный оказывается на своём
окончательном месте, половинки сортируем рекурсивно. База рекурсии —
кучка из 0-1 элементов.

Разбиение трёхчастное (left / center / right): ВСЕ элементы, равные
опорному, оседают в center и в рекурсию не идут — на данных с
дубликатами это серьёзная экономия.

Сложность: O(n·log n) в среднем — если pivot делит кучки примерно
пополам, дерево рекурсии имеет глубину ~log n. Но худший случай —
O(n²): неудачный pivot делит как «1 против всех», дерево вырождается
в палку глубиной n.

Здесь две версии, различающиеся ТОЛЬКО выбором опорного:
  * quick_sort             — случайный pivot: худший случай на любых
    данных астрономически маловероятен;
  * quick_sort_first_pivot — pivot = первый элемент (как в версии
    с урока): на уже отсортированном входе гарантированный худший
    случай, а на ~1000+ элементах — RecursionError (лимит глубины
    рекурсии Python). Краш-тест — в compare_sorts.py.
"""

import random

from sort_stats import Stats


def _quick(s, stats, depth, choose_pivot):
    stats.calls += 1
    if depth > stats.max_depth:
        stats.max_depth = depth
    if len(s) <= 1:  # база: пустая или одноэлементная кучка отсортирована
        return s

    pivot = choose_pivot(s)
    left, center, right = [], [], []
    for x in s:
        stats.copies += 1
        stats.comparisons += 1
        if x < pivot:
            left.append(x)
        else:
            stats.comparisons += 1  # второе сравнение: x > pivot или равен
            if x > pivot:
                right.append(x)
            else:
                center.append(x)

    return (_quick(left, stats, depth + 1, choose_pivot)
            + center
            + _quick(right, stats, depth + 1, choose_pivot))


def quick_sort(items):
    """Вернуть (новый отсортированный список, Stats). Случайный pivot."""
    stats = Stats("быстрая (rnd)")
    result = _quick(list(items), stats, 1, random.choice)
    return result, stats


def quick_sort_first_pivot(items):
    """Как на уроке: pivot = первый элемент. Для демонстрации worst case."""
    stats = Stats("быстрая (s[0])")
    result = _quick(list(items), stats, 1, lambda s: s[0])
    return result, stats


if __name__ == "__main__":
    data = [5, 2, 8, 1, 9, 3, 8, 2]
    result, stats = quick_sort(data)
    print(f"{data} -> {result}")
    print(f"Работа: {stats.summary()}")

    # Один и тот же отсортированный вход, разные pivot:
    tidy = list(range(200))
    _, stats_rnd = quick_sort(tidy)
    _, stats_first = quick_sort_first_pivot(tidy)
    print(f"\nОтсортированный вход из 200 элементов:")
    print(f"  случайный pivot: глубина {stats_rnd.max_depth}, "
          f"сравнений {stats_rnd.comparisons}")
    print(f"  pivot = s[0]:    глубина {stats_first.max_depth}, "
          f"сравнений {stats_first.comparisons}  <- палка и квадрат")
