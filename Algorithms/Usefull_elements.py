class Step:
    def __init__(self, enable_graph_flag = False, arrow_flag = False, enable_table_flag = False):
        self.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Default text for step</p>'
        self.step_label = 'Default text for step label' # Приписка к шагу
        self.nodes = [] # вершины
        self.node_options = {} # доп опции вершин
        self.edges = {} # ребра. Формат: (from, to): weight
        self.edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
        self.general_options = 'width: "100%", height: 400 + "px", interaction: { navigationButtons: true, }' # опции для всего холста
        if arrow_flag:
            self.general_options += ', edges: { arrows: { to: { enabled: true } } }'
        self.enable_graph = enable_graph_flag
        self.enable_table = enable_table_flag
        self.matrix = []
    text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Default text for step</p>'
    step_label = "Default text for step label" # Приписка к шагу
    nodes = [] # вершины
    node_options = {} # доп опции вершин
    edges = {} # ребра. Формат: (from, to): weight
    edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
    general_options = 'width: 1200 + "px", height: 400 + "px"' # опции для всего холста
    enable_graph = False
    enable_table = False
    matrix = []

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

def vertex_list_to_str(vertex_list):
    if len(vertex_list) == 0: return '{ }'
    result = '{ '
    result += f'x<sub>{vertex_list[0]}</sub>'
    for i in range(1, len(vertex_list)):
        result += f', x<sub>{vertex_list[i]}</sub>'
    result += ' }'
    return result


def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

import colorsys

def hsv_to_rgb(hue, saturation, value):
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)

    return tuple(round(x * 255) for x in rgb)

def hsv_to_hex(hue, saturation, value):
    rgb = hsv_to_rgb(hue, saturation, value)
    return rgb_to_hex(rgb[0], rgb[1],rgb[2])