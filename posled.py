class Graph:
    def __init__(self):
     # словарь, содержащий ключи, которые сопоставляются с соответствующим объектом вершины
        self.vertices = {}
    def add_vertex(self, key):
        """Добавьте вершину с заданным ключом к графу."""
        vertex = Vertex(key)
        self.vertices[key] = vertex
    def get_vertex(self, key):
        """Возвращает объект vertex с соответствующим ключом."""
        return self.vertices[key]
    def __contains__(self, key):
        return key in self.vertices
    def add_edge(self, src_key, dest_key, weight=1):
        """Добавьте ребро из src_key в dest_key с заданным весом."""
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)
    def does_edge_exist(self, src_key, dest_key):
        """Возвращает True, если существует ребро от src_key до dest_key."""
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])
    def __len__(self):
        return len(self.vertices)
    def __iter__(self):
        return iter(self.vertices.values())
 
class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}
    def get_key(self):
        """Возвращает ключ, соответствующий этому объекту вершины."""
        return self.key
    def add_neighbour(self, dest, weight):
        """Пусть эта вершина указывает на dest с заданным весом ребра."""
        self.points_to[dest] = weight
    def get_neighbours(self):
        """Верните все вершины, на которые указывает эта вершина."""
        return self.points_to.keys()
    def get_weight(self, dest):
        """Получить вес ребра от этой вершины до dest."""
        return self.points_to[dest]
    def does_it_point_to(self, dest):
        """Возвращает True, если эта вершина указывает на dest."""
        return dest in self.points_to

def floyd_warshall(g):
    """Вернуть массив расстояний distance и next_v.
    distance[u][v] это кратчайшее расстояние от вершины u до v.
    next_v[u][v] следующая вершина после вершины v на кратчайшем пути от u до v.
    Она не является таковой, если между ними нет пути. next_v[u][u] должно быть
    None для каждого u.
    g объект графа, который может иметь отрицательные веса ребер.
    """
    distance = {v:dict.fromkeys(g, float('inf')) for v in g}
    next_v = {v:dict.fromkeys(g, None) for v in g}
 
    for v in g:
        for n in v.get_neighbours():
            distance[v][n] = v.get_weight(n)
            next_v[v][n] = n
 
    for v in g:
         distance[v][v] = 0
         next_v[v][v] = None
 
    for p in g: 
        for v in g:
            for w in g:
                if distance[v][w] > distance[v][p] + distance[p][w]:
                    distance[v][w] = distance[v][p] + distance[p][w]
                    next_v[v][w] = next_v[v][p]
 
    return distance, next_v
 
def print_path(next_v, u, v):
    """Вывести кратчайший путь от вершины u до v.
    next_v-это словарь, где next_v[u][v] - следующая вершина после вершины
    u на кратчайшем пути от u до v. Она не является таковой, если между ними
    нет пути. next_v[u][u] должно быть None для каждого u.
    u и v являются вершинными объектами.
    """
    p = u
    while (next_v[p][v]):
        print('{} -> '.format(p.get_key()), end='')
        p = next_v[p][v]
    print('{} '.format(v.get_key()), end='')
 
 
g = Graph()
print('Меню')
print('добавить вершину <key>')
print('добавить ребро <вершина_1> <вершина_2> <вес>')
print('флойд-уоршелл')
print('отобразить')
print('выход')
 
while True:
    do = input('Чтобы бы вы хотели сделать? ').split()
 
    operation = do[0]
    if operation == 'добавить':
        suboperation = do[1]
        if suboperation == 'вершину':
            key = int(do[2])
            if key not in g:
                g.add_vertex(key)
            else:
                print('Вершина уже существует.')
        elif suboperation == 'ребро':
            src = int(do[2])
            dest = int(do[3])
            weight = int(do[4])
            if src not in g:
                print('Вершина {} не существует.'.format(src))
            elif dest not in g:
                print('Вершина {} не существует.'.format(dest))
            else:
                if not g.does_edge_exist(src, dest):
                    g.add_edge(src, dest, weight)
                else:
                    print('Ребро уже существует.')
 
    elif operation == 'флойд-уоршелл':
        distance, next_v = floyd_warshall(g)
        print('Кратчайшие расстояния:')
        for start in g:
            for end in g:
                if next_v[start][end]:
                    print('От {} до {}: '.format(start.get_key(),end.get_key()), end = '')
                    print_path(next_v, start, end)
                    print('(расстояние {})'.format(distance[start][end]))
 
    elif operation == 'отобразить':
        print('Вершины: ', end='')
        for v in g:
            print(v.get_key(), end=' ')
        print()
 
        print('Рёбра: ')
        for v in g:
            for dest in v.get_neighbours():
                w = v.get_weight(dest)
                print('(вершина_1={}, вершина_2={}, вес={}) '.format(v.get_key(), dest.get_key(), w))
        print()
 
    elif operation == 'выход':
        break
