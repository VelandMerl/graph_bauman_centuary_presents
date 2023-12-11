# Модуль Коли
from flask import session
from Algorithms.Usefull_elements import Step, get_edges, vertex_list_to_str
import math

def convert(input):
    N = len (input)
    result = []
    for i in range(N):
        for j in range(i+1, N):
            result.append((input[i][j], i, j))
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

    for i in range(0, size_of_matrix):
        all_vertex.append(i)

    alg_input = Step(True, False, True)
    first_line = []
    first_line.append('')
    for i in range(0, size_of_matrix):
        first_line.append(f'x{i}')
    alg_input.matrix.append(list(first_line))
    for i in range(0, size_of_matrix):
        next_line = []
        next_line.append(f'x{i}')
        next_line += (list(input_matrix[i]))
        alg_input.matrix.append(list(next_line))
    for i in range(1, size_of_matrix+1):
        alg_input.matrix[i][i] = -1
    
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Введенный граф</p>'
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
            DI[(r[1],r[2])] = r[0]  # создаем словарь ребер добавленных в остов

            A = Step(True)     
            A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{r[1]},{r[2]}], так как оно имеет наименьший вес из всех ребер соединяющих две разные вершины, одна из которых содержится в нашем подграфе, а вторая - еще нет.</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
            A.nodes = list(U1)
            A.step_label = 'Добавление ребер с минимальным размером.'
            for i in U1:
                A.node_options[i] = f'label: "x{i}"'
                A.node_options[i] += f', shape: "circle"'
                if i == r[1] or i == r[2]:
                    A.node_options[i] += f', "color": "#ADFF2F"'
                else:
                    A.node_options[i] += f', "color": "#FFFFFF"'
            A.edges = dict(DI) 
            steps.append(A)

    for r in Rs:    # проходим по ребрам второй раз и объединяем разрозненные группы вершин
        if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
            T.append(r)             # добавляем ребро в остов
            gr1 = D[r[1]]
            D[r[1]] += D[r[2]]      # объединим списки двух групп вершин
            D[r[2]] += gr1

            DI[(r[1],r[2])] = r[0]    # создаем словарь ребер добавленных в остов
            B = Step(True)   
            B.step_label = 'Объединение компонент связности ребрами минимального размера.' 
            B.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{r[1]},{r[2]}], так как оно имеет наименьший вес из всех ребер соединяющих получившиеся компоненты связности.</p>'
            B.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
            B.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
            B.nodes = list(U1)
            for i in U1:
                B.node_options[i] = f'label: "x{i}"'
                B.node_options[i] += f', shape: "circle"'
                if i == r[1] or i == r[2]:
                    B.node_options[i] += f', "color": "#ADFF2F"'
                else:
                    B.node_options[i] += f', "color": "#FFFFFF"'
            B.edges = dict(DI) 
            steps.append(B)

    alg_result = []
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = U1
    result_step.edges = DI
    for i in U1:
            result_step.node_options[i] = f'label: "x{i}"'
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

    for i in range(0, N):
        all_vertex.append(i)
    
    alg_input = Step(True, False, True)
    first_line = []
    first_line.append('')
    for i in range(0, N):
        first_line.append(f'x{i}')
    alg_input.matrix.append(list(first_line))
    for i in range(0, N):
        next_line = []
        next_line.append(f'x{i}')
        next_line += (list(input_matrix[i]))
        alg_input.matrix.append(list(next_line))
    for i in range(1, N+1):
        alg_input.matrix[i][i] = -1

    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Введенный граф</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    alg_input.step_label = 'Введенный исходный граф'
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'
    
    R.append((math.inf, -1, -1))
    U = {0}   
    T = []    
    DI = {}     
    steps = [] 

    while len(U) < N:
        r = get_min(R, U)     
        if r[0] == math.inf:    
            break
        if not(r[1] in U) :
            gr_node = r[1]
        if not(r[2] in U):
            gr_node = r[2]
        T.append(r)            
        U.add(r[1])             
        U.add(r[2])
        DI[(r[1],r[2])] = r[0]
        U1 = list(U)

        A = Step(True)            
        A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим вершину {gr_node}, соединенную минимальным из оставшихся ребром [{r[1]},{r[2]}], имеющим вес {r[0]}</p>'
        A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
        A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
        A.nodes = list(U1)
        A.step_label = 'Объединение компонент связности ребрами минимального размера.' 
        for i in U1:
            A.node_options[i] = f'label: "x{i}"'
            A.node_options[i] += f', shape: "circle"'
            if i == gr_node :
                A.node_options[i] += f', "color": "#ADFF2F"'
            else:
                A.node_options[i] += f', "color": "#FFFFFF"' 
        A.edges = dict(DI) 
        steps.append(A)

    alg_result = []
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = U1
    result_step.edges = DI
    for i in U1:
        result_step.node_options[i] = f'label: "x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        result_step.node_options[i] += f', "color": "#FFFFFF"'
    alg_result.append(result_step)
    
    return [alg_input, steps, alg_result]