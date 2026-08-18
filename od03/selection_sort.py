"""Урок od03. Сортировка выбором (selection sort).

Найти минимум всего массива — поставить первым. Найти минимум
остатка — вторым. И так далее: слева растёт отсортированный префикс,
причём каждый его элемент уже НАВСЕГДА на своём месте.

Сложность: O(n²) всегда — лучшего случая нет. Чтобы найти минимум
остатка, надо просмотреть весь остаток, каким бы «хорошим» ни был
вход: сравнений ровно n·(n-1)/2 на любых данных (проверяется
в compare_sorts.py).

Фирменное достоинство: минимум обменов — не больше одного за проход
(до n-1 всего). Фирменный недостаток: нестабильность — дальний обмен
может переставить равные элементы.
"""

from sort_stats import Stats


def selection_sort(items):
    """Вернуть (новый отсортированный список, Stats). Вход не меняется."""
    arr = list(items)
    stats = Stats("выбор")
    n = len(arr)
    for i in range(n - 1):  # последний элемент встанет на место сам
        min_index = i
        for j in range(i + 1, n):
            stats.comparisons += 1
            if arr[j] < arr[min_index]:
                min_index = j
        if min_index != i:  # холостой обмен «сам с собой» не считаем работой
            arr[i], arr[min_index] = arr[min_index], arr[i]
            stats.swaps += 1
    return arr, stats


if __name__ == "__main__":
    data = [5, 2, 4, 1, 3]
    result, stats = selection_sort(data)
    print(f"{data} -> {result}")
    print(f"Работа: {stats.summary()}")

    result, stats = selection_sort([1, 2, 3, 4, 5])
    print(f"\nУже отсортированный вход: {stats.summary()}")
    print("(сравнений столько же — выбору всё равно, какие данные)")
