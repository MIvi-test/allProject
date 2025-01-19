def prefix_func(s:str):
    n = len(s)
    p = [0]*n
    for i in range(1,n):
        cur = p[i-1]
        while (s[i] != s[cur]) and (cur>0):
            cur = p[cur-1]
        
        if s[i] == s[cur]:
            p[i] = cur +1
    
    return p

def z_function(s):
    n = len(s)
    z = [0] * n
    left, right = 0, 0
    
    for i in range(1, n):
        # Если текущий индекс находится внутри ранее найденного блока
        if i <= right:
            # Используем информацию о блоке, чтобы начать с правильного значения
            z[i] = min(right - i + 1, z[i - left])
        
        # Расширяем блок до тех пор, пока символы совпадают
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        # Обновляем границы блока, если нашли больший блок
        if i + z[i] - 1 > right:
            left = i
            right = i + z[i] - 1
    
    return z

from typing import List

def compress(a: List[int]) -> List[int]:
    # Создаем копию списка a
    b = sorted(a)
    
    # Убираем дубликаты из отсортированного списка
    b = list(set(b))
    
    # Преобразуем исходный список a, заменяя значения на индексы в списке b
    for i in range(len(a)):
        a[i] = b.index(a[i])
        
    return a

mod = 1e9 + 7
def binpow(a, n):
    res = 1
    while n > 0:
        if n % 2 == 1:
            res = (res * a) % mod
        a = (a * a) % mod
        n //= 2
    return res

print(int(binpow(3, 32)))
print(3**32 % mod)
def scanline(segments):
    events = []

    # Создание событий для начала и конца отрезков
    for l, r in segments:
        events.append((l, 1))   # Начало отрезка
        events.append((r, -1))  # Конец отрезка

    # Сортировка событий: по координате, затем по типу (конец перед началом)
    events.sort(key=lambda x: (x[0], -x[1]))

    cnt = 0  # Текущая количество перекрывающихся отрезков
    res = 0  # Максимальное количество перекрывающихся отрезков

    # Обработка событий
    for _, typ in events:
        cnt += typ
        res = max(res, cnt)

    return res

MAXN = 10**5

used = [False] * MAXN
h = [0] * MAXN
d = [0] * MAXN

def dfs(v, p=-1):
    global g
    used[v] = True
    h[v] = d[v] = 0 if p == -1 else h[p] + 1
    
    for u in g[v]:
        if u != p:
            if used[u]: # Если ребро обратное
                d[v] = min(d[v], h[u])
            else: # Если ребро прямое
                dfs(u, v)
                d[v] = min(d[v], d[u])
                if h[v] < d[u]:
                    # Если невозможно другим путём добраться до вершины v или выше,
                    # то ребро (v, u) является мостом
                    pass # Здесь можно добавить код для обработки моста

# Пример использования функции dfs
g = [] # Здесь нужно предварительно заполнить список смежности g
dfs(0) # Начинаем обход с вершины 0
color = {}
def dfs(v, p = 1):
    # v start, p parent
    global g, color
    used[v] = True
    if color[v] == color[p]:
        print('не двудольный')
    else:
        
        for u in g[v]:
            if u != p:
                if used[u]:
                    continue
                else:
                    dfs(u, v)
                    h[v] = min(h[v], h[u] + 1)


# Пример использования
if __name__ == "__main__":
    segments = [(1, 3), (2, 5), (4, 6)]
    print("Максимальное количество перекрывающихся отрезков:", scanline(segments))
 