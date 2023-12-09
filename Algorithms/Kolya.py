# Модуль Коли
from flask import session
from Algorithms.Usefull_elements import Step, get_edges, vertex_list_to_str
import math

def convert(input):
    N = len (input)
    result = []
    for i in range(N):
        for j in range(i+1, N):
            result.append((input[i][j], i+1, j+1))
    print(result)
    return result


def kraskal(input_matrix):
    R = convert(input_matrix)

    Rs = sorted(R, key=lambda x: x[0])
    U = set()  # список соединенных вершин
    D = {}      # словарь списка изолированных групп вершин
    T = []      # список ребер остова
    DI = {}     # словарь ребер
    steps = [] 
    all_vertex = []
    size_of_matrix = len(input_matrix)
    steps = []
    edges = get_edges(input_matrix)

    for i in range(1, size_of_matrix+1):
        all_vertex.append(i)

    alg_input = Step(True)
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    alg_input.step_label = 'Введенный исходный граф'
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'

    for r in Rs:
        if r[1] not in U or r[2] not in U:  # проверка для исключения циклов в остове
            if r[1] not in U and r[2] not in U: # если обе вершины не соединены, то
                D[r[1]] = [r[1], r[2]]          # формируем в словаре ключ с номерами вершин
                D[r[2]] = D[r[1]]               # и связываем их с одним и тем же списком вершин
            else:                           # иначе
                if not D.get(r[1]):             # если в словаре нет первой вершины, то
                    D[r[2]].append(r[1])        # добавляем в список первую вершину
                    D[r[1]] = D[r[2]]           # и добавляем ключ с номером первой вершины
                else:
                    D[r[1]].append(r[2])        # иначе, все то же самое делаем со второй вершиной
                    D[r[2]] = D[r[1]]

            T.append(r)             # добавляем ребро в остов
            U.add(r[1])             # добавляем вершины в множество U
            U.add(r[2])
            U1 = list(U)            # создаем список добавленных в остов вершин
            DI[(r[1],r[2])] = r[0] 
            print(DI)   # создаем словарь ребер добавленных в остов

            A = Step(True)              # тут все по объяснениям Андрея
            A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{r[1]},{r[2]}], так как оно имеет наименьший вес из всех ребер соединяющих две разные вершины, одна из которых содержится в нашем подграфе, а вторая - еще нет.</p>'
            A.nodes = U1
            alg_input.step_label = 'Введенный исходный граф'
            for i in U1:
                A.node_options[i] = f'label: "x{i}"'
                A.node_options[i] += f', shape: "circle"'
                A.node_options[i] += f', "color": "#FFFFFF"'
            A.edges = DI 
            A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
            steps.append(A)

    for r in Rs:    # проходим по ребрам второй раз и объединяем разрозненные группы вершин
        if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
            T.append(r)             # добавляем ребро в остов
            gr1 = D[r[1]]
            D[r[1]] += D[r[2]]      # объединем списки двух групп вершин
            D[r[2]] += gr1

            DI[(r[1],r[2])] = r[0]    # создаем словарь ребер добавленных в остов
            print(DI)
            B = Step(True)              # тут все по объяснениям Андрея
            message = '"Так как вершины {a2} и {a1} все еще не соедиbbнены и имеют наименьший вес ребра из не добавленных в остов, равный {a3}, соединяем их."'
            B.text = message.format(a1 = r[1], a2 = r[2], a3 = DI[r[1],r[2]])   # для добавления переменной в строку
            B.nodes = U1
            print (B.nodes)
            B.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
            B.edges = DI 
            B.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
            steps.append(B)

    alg_result = []
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = U1
    result_step.edges = DI
    for i in U1:
            result_step.node_options[i] = f'label: "{i}"'
            result_step.node_options[i] += f', shape: "circle"'
            result_step.node_options[i] += f', "color": "#FFFFFF"'
    alg_result.append(result_step)
    return [alg_input,steps,alg_result]

def get_min(R, U):
    rm = (math.inf, -1, -1)
    for v in U:
        rr = min(R, key=lambda x: x[0] if (x[1] == v or x[2] == v) and (x[1] not in U or x[2] not in U) else math.inf)
        if rm[0] > rr[0]:
            rm = rr

    return rm

def prim(input_matrix):
    R = convert(input_matrix)
    all_vertex = []
    N = len(input_matrix)
    steps = []
    edges = get_edges(input_matrix)

    for i in range(1, N):
        all_vertex.append(i)

    alg_input = Step(True)
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    alg_input.step_label = 'Введенный исходный граф'
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'
    
    R.append((math.inf, -1, -1))
    U = {1}   # множество соединенных вершин
    T = []    # список ребер остова
    DI = {}     # словарь ребер
    steps = [] 

    while len(U) < N:
        r = get_min(R, U)       # ребро с минимальным весом
        if r[0] == math.inf:    # если ребер нет, то остов построен
            break

        T.append(r)             # добавляем ребро в остов
        U.add(r[1])             # добавляем вершины в множество U
        U.add(r[2])
        DI[(r[1],r[2])] = r[0]
        U1 = list(U)

        A = Step()              # тут все по объяснениям Андрея
        A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
        A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
        A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{r[1]},{r[2]}], так как оно имеет наименьший вес из всех ребер соединяющих две разные вершины, одна из которых содержится в нашем подграфе, а вторая - еще нет.</p>'
        A.nodes = U1
        print(R)
        print (A.nodes)
        A.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
        A.edges = DI 
        A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
        steps.append(A)

    alg_result = []
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = U1
    result_step.edges = DI
    for i in U1:
        result_step.node_options[i] = f'label: "{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        result_step.node_options[i] += f', "color": "#FFFFFF"'
    alg_result.append(result_step)
    
    return [alg_input,steps,alg_result]