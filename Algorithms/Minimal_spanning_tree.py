# Модуль Коли
from flask import session
from Algorithms.Usefull_elements import Step, get_edges, vertex_list_to_str
import math

def convert_krask(input):
    N = len (input)
    result = []
    for i in range(N):
        for j in range(i+1, N):
            if input[i][j] != 0:
                result.append((input[i][j], i, j))
    return result

def convert_prim(input):
    N = len (input)
    result = []
    for i in range(N):
        for j in range(i+1, N):
                if input[i][j] > 0:
                    result.append((input[i][j], i, j))
                else:
                    result.append((9999, i, j))
    return result


def kraskal(input_matrix):
    working_matrix = convert_krask(input_matrix)

    Rs = sorted(working_matrix, key=lambda x: x[0])
    nodes = set()  
    Dic = {}         
    dictionary = {}     
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

    for edge in Rs:
        if edge[1] not in nodes or edge[2] not in nodes:  
            if edge[1] not in nodes and edge[2] not in nodes:
                Dic[edge[1]] = [edge[1], edge[2]]         
                Dic[edge[2]] = Dic[edge[1]]               
            else:                           
                if not Dic.get(edge[1]):             
                    Dic[edge[2]].append(edge[1])    
                    Dic[edge[1]] = Dic[edge[2]]         
                else:
                    Dic[edge[1]].append(edge[2])       
                    Dic[edge[2]] = Dic[edge[1]]
      
            nodes.add(edge[1])          
            nodes.add(edge[2])
            U1 = list(nodes)         
            dictionary[(edge[1],edge[2])] = edge[0]  
            A = Step(True)     
            A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{edge[1]},{edge[2]}], так как оно имеет наименьший вес из всех ребер соединяющих две разные вершины, одна из которых содержится в нашем подграфе, а вторая - еще нет.</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
            A.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
            A.nodes = list(U1)
            A.step_label = 'Добавление ребер с минимальным размером.'
            for i in U1:
                A.node_options[i] = f'label: "x{i}"'
                A.node_options[i] += f', shape: "circle"'
                if i == edge[1] or i == edge[2]:
                    A.node_options[i] += f', "color": "#ADFF2F"'
                else:
                    A.node_options[i] += f', "color": "#FFFFFF"'
            A.edges = dict(dictionary) 
            steps.append(A)

    for edge in Rs:    
        if edge[2] not in Dic[edge[1]]:     
            for i in Dic[edge[1]]:
                if edge[2] not in Dic[i]:
                    Dic[i] += Dic[edge[2]]
            gr1 = Dic[edge[1]]
            Dic[edge[1]] += Dic[edge[2]]      
            Dic[edge[2]] += gr1

            dictionary[(edge[1],edge[2])] = edge[0]   
            B = Step(True)   
            B.step_label = 'Объединение компонент связности ребрами минимального размера.' 
            B.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим ребро [{edge[1]},{edge[2]}], так как оно имеет наименьший вес из всех ребер соединяющих получившиеся компоненты связности.</p>'
            B.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соединенные вершины: {vertex_list_to_str(U1)}</p>'
            B.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины до сих пор не включенные в остов: {vertex_list_to_str(list(set(all_vertex) - set(U1)))}</p>'
            B.nodes = list(U1)
            for i in U1:
                B.node_options[i] = f'label: "x{i}"'
                B.node_options[i] += f', shape: "circle"'
                if i == edge[1] or i == edge[2]:
                    B.node_options[i] += f', "color": "#ADFF2F"'
                else:
                    B.node_options[i] += f', "color": "#FFFFFF"'
            B.edges = dict(dictionary) 
            steps.append(B)
    alg_result = []
    U1 = list(all_vertex)
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = list(U1)
    result_step.edges = dictionary
    for i in U1:
            result_step.node_options[i] = f'label: "x{i}"'
            result_step.node_options[i] += f', shape: "circle"'
            result_step.node_options[i] += f', "color": "#FFFFFF"'
    alg_result.append(result_step)
    return [alg_input,steps,alg_result]

def get_min(working_matrix, nodes):
    rm = (math.inf, -1, -1)
    for v in nodes:
        rr = min(working_matrix, key=lambda x: x[0] if (x[1] == v or x[2] == v) and (x[1] not in nodes or x[2] not in nodes) else math.inf)
        if rm[0] > rr[0]:
            rm = rr
    return rm

def prim(input_matrix):
    working_matrix = convert_prim(input_matrix)
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
    
    working_matrix.append((math.inf, -1, -1))
    nodes = {0}    
    dictionary = {}     
    steps = [] 

    while len(nodes) < N:
        edge = get_min(working_matrix, nodes)     
        if edge[0] == math.inf:    
            break
        if not(edge[1] in nodes) :
            gr_node = edge[1]
        if not(edge[2] in nodes):
            gr_node = edge[2]         
        nodes.add(edge[1])             
        nodes.add(edge[2])
        if edge[0] != 9999:
            dictionary[(edge[1],edge[2])] = edge[0]
            U1 = list(nodes)

            A = Step(True)            
            A.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим вершину {gr_node}, соединенную минимальным из оставшихся ребром [{edge[1]},{edge[2]}], имеющим вес {edge[0]}</p>'
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
            A.edges = dict(dictionary) 
            steps.append(A)

    alg_result = []
    U1 = list(all_vertex)
    result_step = Step(True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Получившийся минимальный остов:</p>'
    result_step.nodes = U1
    result_step.edges = dictionary
    for i in U1:
        result_step.node_options[i] = f'label: "x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        result_step.node_options[i] += f', "color": "#FFFFFF"'
    alg_result.append(result_step)
    
    return [alg_input, steps, alg_result]