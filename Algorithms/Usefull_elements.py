class Step:
    def __init__(self, flag=False):
        self.text = "Default text for step"
        self.step_label = "Default text for step label" # Приписка к шагу
        self.nodes = [] # вершины
        self.node_options = {} # доп опции вершин
        self.edges = {} # ребра. Формат: (from, to): weight
        self.edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
        self.general_options = 'width: 1200 + "px", height: 400 + "px"' # опции для всего холста
        if flag:
          self.general_options += ', edges: { arrows: { to: { enabled: true } } }'
    text = "Default text for step"
    step_label = "Default text for step label" # Приписка к шагу
    nodes = [] # вершины
    node_options = {} # доп опции вершин
    edges = {} # ребра. Формат: (from, to): weight
    edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
    general_options = 'width: 1200 + "px", height: 400 + "px"' # опции для всего холста

# объединение
def intersection(A, B):
  C = []
  for tmp in A:
    if tmp in B:
      C.append(tmp)
  return C
# дополнение
def addition(A, B):
  C = []
  for tmp in A:
    if not (tmp in B):
      C.append(tmp)
  return C

def invert_Graph(matr, size_N):
  tmp_matr = []
  for i in range(size_N):
    tmp_matr.append(list(matr[i]))
  for i in range(size_N):
    for j in range(i, size_N):
      tmp_matr[i][j], tmp_matr[j][i] = tmp_matr[j][i], tmp_matr[i][j]
  return tmp_matr

def get_edges(matrix):
  edges = {}
  for i in range(len(matrix)):
    for j in range(len(matrix)):
      if matrix[i][j] > 0:
        edges[(i, j)] = matrix[i][j]
  return edges