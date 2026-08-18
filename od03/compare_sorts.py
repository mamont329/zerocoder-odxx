"""Урок od03. Сводный стенд: корректность, гонка, статистика, краш-тест.

Собирает все четыре сортировки и прогоняет их через:
  1) проверку корректности против эталона sorted() на коварных случаях;
  2) гонку по секундомеру на трёх типах данных;
  3) таблицу счётчиков (чистая работа алгоритмов, без питоновских
     накладных расходов);
  4) проверку теоретических предсказаний числами;
  5) краш-тест версии с pivot = первый элемент.
"""

import random
from time import perf_counter

from bubble_sort import bubble_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from quick_sort import quick_sort, quick_sort_first_pivot

ALGORITHMS = [bubble_sort, selection_sort, insertion_sort, quick_sort]


def check_correctness():
    """Все сортировки на всех случаях обязаны совпасть с sorted()."""
    cases = [
        [],                       # пустой
        [7],                      # один элемент
        [2, 1],                   # минимальный беспорядок
        [3, 1, 2, 3, 1, 3],       # дубликаты
        list(range(10)),          # уже отсортированный
        list(range(10, 0, -1)),   # задом наперёд
        [5, -3, 0, 5, 2, -3],     # отрицательные и повторы
        ["груша", "арбуз", "яблоко", "банан"],  # строки сортируются тоже
        [random.randint(-50, 50) for _ in range(100)],  # случайный большой
    ]
    for case in cases:
        expected = sorted(case)
        original = list(case)
        for algo in ALGORITHMS + [quick_sort_first_pivot]:
            result, _ = algo(case)
            assert result == expected, (
                f"{algo.__name__} ошибся на {case}: {result} != {expected}")
            assert case == original, (
                f"{algo.__name__} изменил входной список — нарушен контракт!")
    print(f"Корректность: все алгоритмы совпали с sorted() "
          f"на {len(cases)} наборах, входы не изменены.")


def make_datasets(n):
    """Три характера данных: хаос, порядок, анти-порядок."""
    return [
        ("случайные", [random.randint(0, n) for _ in range(n)]),
        ("отсортированные", list(range(n))),
        ("обратные", list(range(n, 0, -1))),
    ]


def race(n):
    """Секундомер: наши четыре + встроенный sorted() вне конкурса."""
    print(f"\n=== Гонка, n = {n} ===")
    for label, data in make_datasets(n):
        print(f"\n  Данные: {label}")
        for algo in ALGORITHMS:
            start = perf_counter()
            _, stats = algo(data)
            elapsed = perf_counter() - start
            print(f"    {stats.name:<15} {elapsed * 1000:8.1f} мс")
        start = perf_counter()
        sorted(data)
        elapsed = perf_counter() - start
        print(f"    {'sorted() [C]':<15} {elapsed * 1000:8.1f} мс")


def stats_table(n):
    """Чистая работа алгоритмов: счётчики вместо секундомера."""
    print(f"\n=== Статистика, n = {n} ===")
    header = (f"    {'алгоритм':<15} {'сравнения':>10} {'обмены':>8} "
              f"{'сдвиги':>8} {'копир.':>8} {'глубина':>8}")
    for label, data in make_datasets(n):
        print(f"\n  Данные: {label}")
        print(header)
        for algo in ALGORITHMS:
            _, s = algo(data)
            print(f"    {s.name:<15} {s.comparisons:>10} {s.swaps:>8} "
                  f"{s.writes:>8} {s.copies:>8} {s.max_depth:>8}")


def count_inversions(arr):
    """Число инверсий — пар (i, j), стоящих не в том порядке.
    Лобовой подсчёт за O(n²): для проверки предсказаний хватает."""
    return sum(
        1
        for i in range(len(arr))
        for j in range(i + 1, len(arr))
        if arr[i] > arr[j]
    )


def check_predictions():
    """Три теоретических предсказания, проверенные счётчиками."""
    print("\n=== Проверка предсказаний ===")

    # 1. Обмены пузырька = сдвиги вставок = число инверсий входа.
    print("\n  1) обмены пузырька == сдвиги вставок == число инверсий:")
    for trial in range(3):
        data = [random.randint(0, 999) for _ in range(300)]
        inversions = count_inversions(data)
        _, bubble_stats = bubble_sort(data)
        _, insertion_stats = insertion_sort(data)
        ok = inversions == bubble_stats.swaps == insertion_stats.writes
        print(f"     инверсий: {inversions}, обменов: {bubble_stats.swaps}, "
              f"сдвигов: {insertion_stats.writes} -> {'✓' if ok else 'РАСХОЖДЕНИЕ!'}")

    # 2. Сравнения выбора — ровно n(n-1)/2 на ЛЮБЫХ данных.
    n = 500
    expected = n * (n - 1) // 2
    print(f"\n  2) сравнения выбора всегда n(n-1)/2 = {expected} при n = {n}:")
    for label, data in make_datasets(n):
        _, s = selection_sort(data)
        ok = s.comparisons == expected
        print(f"     {label:<16} {s.comparisons} -> {'✓' if ok else 'РАСХОЖДЕНИЕ!'}")

    # 3. Отсортированный вход: адаптивные алгоритмы делают O(n) работы.
    n = 1000
    tidy = list(range(n))
    _, b = bubble_sort(tidy)
    _, i = insertion_sort(tidy)
    print(f"\n  3) отсортированный вход (n = {n}):")
    print(f"     пузырёк:  {b.comparisons} сравнений, {b.swaps} обменов "
          f"(один проход — сработал флаг)")
    print(f"     вставки:  {i.comparisons} сравнений, {i.writes} сдвигов "
          f"(каждая «карта» сразу на месте)")


def crash_test():
    """Worst case версии с pivot = s[0]: не замедление, а падение."""
    print("\n=== Краш-тест: pivot = первый элемент ===")
    tidy = list(range(1100))
    _, s = quick_sort(tidy)
    print(f"  случайный pivot на отсортированных 1100: глубина "
          f"{s.max_depth}, сравнений {s.comparisons} — норма")
    try:
        quick_sort_first_pivot(tidy)
        print("  pivot = s[0]: неожиданно выжил (так быть не должно)")
    except RecursionError:
        print("  pivot = s[0]: RecursionError — дерево рекурсии выродилось "
              "в палку глубиной ~1100\n  и упёрлось в лимит Python (~1000). "
              "Худший случай O(n²) — это ещё и падение.")


if __name__ == "__main__":
    check_correctness()
    race(2000)
    stats_table(1000)
    check_predictions()
    crash_test()
