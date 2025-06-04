def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Классическое расстояние Левенштейна.
    Возвращает кол-во правок (вставка/удаление/замена), необходимых,
    чтобы превратить s1 в s2.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # стоимость вставки
            deletions = current_row[j] + 1 # стоимость удаления
            substitutions = previous_row[j] + (c1 != c2) # стоимость замены
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Расстояние Дамерау-Левенштейна — учитывает операцию перестановки соседних символов.
    """
    d = {}
    len_s1 = len(s1)
    len_s2 = len(s2)

    for i in range(-1, len_s1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len_s2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len_s1):
        for j in range(len_s2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1, # удаление
                d[(i, j - 1)] + 1, # вставка
                d[(i - 1, j - 1)] + cost # замена
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)

    return d[(len_s1 - 1, len_s2 - 1)]
