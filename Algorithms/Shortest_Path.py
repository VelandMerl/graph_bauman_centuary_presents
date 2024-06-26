import math
from Algorithms.Usefull_elements import Step, intersection, addition, get_edges, invert_Graph, vertex_list_to_str, hsv_to_hex

def algorithm_Dijkstra(matrix, start = 0, end = 0, orgraph = True):
    if end < 0 or end > (len(matrix)-1):
        end = len(matrix)-1
    if start < 0 or start > (len(matrix)-1):
        start = 0
        
    n = len(matrix)
    visited = [False] * n
    dist = [math.inf] * n
    dist[start] = 0

    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                matrix[i][j] *= -1


    steps = []
    alg_result = []

    edges = get_edges(matrix)
    all_vertex = []
    for i in range(n):
        all_vertex.append(i)
    
    if not orgraph:
        for i in range(len(matrix)):
            j = i
            while j != len(matrix):
                matrix[j][i] = matrix[i][j]
                j += 1

    alg_input = Step(True, orgraph, True)
    first_line = []
    first_line.append('')
    for i in range(n): 
        first_line.append(f'x{i}')
    alg_input.matrix.append(list(first_line))
    for i in range(n): 
        next_line = []
        next_line.append(f'x{i}')
        next_line += list(matrix[i])
        alg_input.matrix.append(list(next_line))
    for i in range(1, n+1):
        alg_input.matrix[i][i] = -1

    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф по введённой матрице смежности</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#8FBFE0"'


    def gofrom():
        index = 0
        distmin = math.inf
        for i in range(n):
            if dist[i] < distmin and visited[i] == False:
                distmin = dist[i]
                index = i
        if distmin == math.inf: 
            index = -1 
        return index

    line_list = []

    next_line = []
    next_line.append(0)
    next_line += list(dist)
    line_list.append(next_line)



    while False in visited:

        i = gofrom()
        if i == -1: 
            break 

        new_step = Step(True, orgraph, True)
        new_step.nodes = all_vertex
        new_step.edges = edges
        new_step.step_label = f'Рассматриваем вершину {i}'
        new_step.matrix.append(list(first_line))

        step_string = f'Находим кратчайшие пути в остальные вершины. <br/> Сравниваем кратчайший путь из вершины {start} в данную вершину и сумму кратчайшего пути из вершины {start} в вершину {i} и пути из вершины {i} в данную вершину. <br/>'
        for j in range(n):
            if matrix[i][j] != 0 and (not visited[j]): 
                if dist[j] <= dist[i] + matrix[i][j]:
                    step_string += f'(х{j}) {dist[j]} <= {dist[i]} + {matrix[i][j]} <br/>'
                else:
                    step_string += f'(х{j}) {dist[j]} > {dist[i]} + {matrix[i][j]}, обновляем значение в ячейке {j} <br/>'
                dist[j] = min(dist[j], dist[i] + matrix[i][j])
        visited[i] = True
        step_string += f'Следующей рассматриваем непосещенную вершину с наименьшим значением в ее ячейке <br/>'
        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{step_string}</p>'

        for j in all_vertex:
            new_step.node_options[j] = f'label: "x{j}"'
            new_step.node_options[j] += f', shape: "circle"'
            if (visited[j]) and (j == i):
                new_step.node_options[j] += f', "color": "#89E375"'
            elif visited[j]:
                new_step.node_options[j] += f', "color": "#DFDFDF"'
            else:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
        next_line = [] 
        next_line.append(f'x{i}') 
        next_line += list(dist) 
        line_list.append(next_line) 
        for x in range(len(line_list)):
            new_step.matrix.append(line_list[x])
        steps.append(new_step)

    path = [end]
    dist_sum = dist[end]
    kostil = [end]
    kost_flag = False
    endend = end
    while end != start:
        new_step = Step(True, orgraph, True)
        new_step.nodes = all_vertex
        new_step.edges = edges
        new_step.step_label = f'Поиск кратчайшего пути из вершины {end} в вершину {start}'
        flag = True

        for j in all_vertex:
            new_step.node_options[j] = f'label: "x{j}"'
            new_step.node_options[j] += f', shape: "circle"'

            if j in path:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
                prev_vert = -1
                for k in range(len(path)):
                    if path[k] == j and len(path) > 1 and k != (len(path)-1):
                        prev_vert = path[k + 1]
                if prev_vert != -1:
                    if flag:
                        new_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                    else:
                        new_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
            elif matrix[j][end] != 0:
                new_step.node_options[j] += f', "color": "#FF6868"'
                for k in range(n):
                    if k != end:
                        if flag:
                            new_step.edge_options[(j, k)] = f' "color": "#659CC1"'
                        else:
                            new_step.edge_options[(j, k)] += f' "color": "#659CC1"'
            else:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
        
        distance_string = f'Находим длину кратчайшего пути из смежных вершин в вершину {end}. <br/>Для этого сравниваем длину кратчайшего пути из веришны {start} в вершину {end} и сумму длины кратчайшего пути из вершины {start} в вершину, смежную вершине {end}, и пути из этой смежной вершины в вершину {end}. <br/>'
        for i in range(n):
            if matrix[i][end] != 0:
                distance_string += f"(х{i}) "
                if dist[end] == dist[i] + matrix[i][end]:
                    distance_string += f"{dist[end]} = {dist[i]} + {matrix[i][end]} <br/>"
                    distance_string += f"Добавляем в путь вершину {i} и рассматриваем ее <br/>"
                    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
                    path.append(i)
                    end = i
                    steps.append(new_step)
                    break
                else:
                    distance_string += f"{dist[end]} =/= {dist[i]} + {matrix[i][end]} <br/>"
        
        kostil.append(path[-1]) 
        if kostil[-2] == kostil[-1]: 
            new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Пути не найдены</p>'
            kost_flag = True
            steps.append(new_step)
            break

    final_step = Step(True, orgraph, True)
    final_step.nodes = all_vertex
    final_step.edges = edges
    distance_string = ''
    flag = True

    for j in all_vertex:
        final_step.node_options[j] = f'label: "x{j}"'
        final_step.node_options[j] += f', shape: "circle"'
        if j in path:
            if j == start:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if l != path[-2]:
                        if flag:
                            final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                        else:
                            final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
            elif j == endend:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if not kost_flag:
                        if l != path[1]:
                            if flag:
                                final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                                final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                            else:
                                final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
                                final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
            else:
                final_step.node_options[j] += f', "color": "#8FBFE0"'
            print(path)
            prev_vert = -1
            for k in range(len(path)):
                if path[k] == j and len(path) > 1 and k != (len(path)-1):
                    prev_vert = path[k + 1]
            if prev_vert != -1:
                if flag:
                    final_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] = f' "color": "#89E375"'
                else:
                    final_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] += f' "color": "#89E375"'
        else:
            final_step.node_options[j] += f', "color": "#8FBFE0"'

    path = list(reversed(path))
    distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: "
    for i in range(len(path)-1):
        distance_string += f"x{path[i]} -> "
    i += 1
    if len(kostil) == 1:
        distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: x{start} <br/> Длина кратчайшего пути: {dist_sum}"
    elif kostil[-2] != kostil[-1] and dist_sum != math.inf:
        distance_string += f"x{path[i]} <br/> Длина кратчайшего пути: {dist_sum}"
    else:
        distance_string = f"Пути из вершины {start} в вершину {endend} не существует"
    
    final_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
    
    alg_result.append(final_step)


    return [ alg_input, steps, alg_result ]

def algorithm_Bellman_Ford(matrix, start = 0, end = 0, orgraph = True):
    if end < 0 or end > (len(matrix)-1):
        end = len(matrix)-1
    if start < 0 or start > (len(matrix)-1):
        start = 0
        
    n = len(matrix)

    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                matrix[i][j] *= -1
    
    dist = [math.inf] * n
    dist[start] = 0 

    path = []
    element = []

    steps = []
    alg_result = []
    kost_flag = False
    edges = get_edges(matrix)

    if not orgraph:
        for i in range(len(matrix)):
            j = i
            while j != len(matrix):
                matrix[j][i] = matrix[i][j]
                j += 1
    
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0:
                element.append((matrix[i][j], i, j))

    all_vertex = []
    for i in range(n):
        all_vertex.append(i)


    alg_input = Step(True, orgraph, True)
    first_line = []
    first_line.append('')
    for i in range(n): 
        first_line.append(f'x{i}')
    alg_input.matrix.append(list(first_line))
    for i in range(n): 
        next_line = []
        next_line.append(f'x{i}')
        next_line += list(matrix[i])
        alg_input.matrix.append(list(next_line))
    for i in range(1, n+1):
        alg_input.matrix[i][i] = -1

    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф по введённой матрице смежности</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#8FBFE0"'

    
    print(dist)
    first_line.append('<b>dist<b>')
    for i in range(n-1):
        for j in range(len(element)): 
            step_string = f'Нахождим длину кратчайшего пути из вершины {start} в вершину {element[j][2]}. <br/> Для этого сравниваем длину кратчайшего пути из вершины {start} в вершину {element[j][2]} и сумму длины кратчайшего пути из вершины {start} в вершину {element[j][1]} и длины пути из вершины {element[j][1]} в вершину {element[j][2]}. <br/>'

            if orgraph:
                if dist[element[j][1]] != math.inf and dist[element[j][2]] > (dist[element[j][1]] + element[j][0]):
                    step_string += f'{dist[element[j][2]]} > {dist[element[j][1]]} + {element[j][0]} <br/>'
                    step_string += f'Заменяем значение в {element[j][2]} ячейке столбца и строки dist <br/>'
                    dist[element[j][2]] = dist[element[j][1]] + element[j][0]
                    line_list = []
                    for k in range(n):
                        next_line = []
                        next_line.append(f'x{k}')
                        next_line += list(matrix[k])
                        next_line.append(dist[k])
                        line_list.append(next_line)

                    new_step = Step(True, orgraph, True)
                    new_step.step_label = f'Вычисление кратчайших путей из вершины {start} в остальные вершины графа'
                    new_step.nodes = all_vertex
                    new_step.edges = edges
                    for l in all_vertex:
                        new_step.node_options[l] = f'label: "x{l}"'
                        new_step.node_options[l] += f', shape: "circle"'
                        new_step.edge_options[(element[j][1], element[j][2])] = f' "color": "#74CB61"'
                        new_step.node_options[l] += f', "color": "#8FBFE0"'

                    new_step.matrix.append(list(first_line))

                    for x in range(len(line_list)):
                        new_step.matrix.append(line_list[x])

                    last_line = []
                    last_line.append('<b>dist<b>')
                    last_line += list(dist)
                    new_step.matrix.append(last_line)
                    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{step_string}</p>'
                    steps.append(new_step)

                    print(dist)
                elif dist[element[j][2]] != math.inf:
                    step_string += f'{dist[element[j][2]]} =< {dist[element[j][1]]} + {element[j][0]} <br/>'

            else:
                if dist[element[j][2]] != math.inf and dist[element[j][1]] > (dist[element[j][2]] + element[j][0]):
                    step_string += f'{dist[element[j][1]]} > {dist[element[j][1]]} + {element[j][0]} <br/>'
                    step_string += f'Заменяем значение в {element[j][2]} ячейке столбца и строки dist <br/>'
                    dist[element[j][1]] = dist[element[j][2]] + element[j][0]

                    line_list = []
                    for k in range(n):
                        next_line = []
                        next_line.append(f'x{k}')
                        next_line += list(matrix[k])
                        next_line.append(dist[k])
                        line_list.append(next_line)

                    new_step = Step(True, orgraph, True)
                    new_step.step_label = f'Вычисление кратчайших путей из вершины {start} в остальные вершины графа'
                    new_step.nodes = all_vertex
                    new_step.edges = edges
                    for l in all_vertex:
                        new_step.node_options[l] = f'label: "x{l}"'
                        new_step.node_options[l] += f', shape: "circle"'

                        new_step.edge_options[(element[j][2], element[j][1])] = f' "color": "#74CB61"'
                        new_step.node_options[l] += f', "color": "#8FBFE0"'

                    new_step.matrix.append(list(first_line))

                    for x in range(len(line_list)):
                        new_step.matrix.append(line_list[x])

                    last_line = []
                    last_line.append('<b>dist<b>')
                    last_line += list(dist)
                    new_step.matrix.append(last_line)
                    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{step_string}</p>'
                    steps.append(new_step)

                    print(dist)
                elif dist[element[j][2]] != math.inf:
                    step_string += f'{dist[element[j][2]]} <= {dist[element[j][1]]} + {element[j][0]} <br/>'
                    
    print()

    path = [end]
    dist_sum = dist[end]
    flag= True
    kostil = [end] 
    endend = end

    while end != start:
        new_step = Step(True, orgraph, True)
        new_step.nodes = all_vertex
        new_step.edges = edges
        new_step.step_label = f'Поиск кратчайшего пути из {end} в {start}'
        for j in all_vertex:
            new_step.node_options[j] = f'label: "x{j}"'
            new_step.node_options[j] += f', shape: "circle"'
    
            if j in path:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
                prev_vert = -1
                for k in range(len(path)):
                    if path[k] == j and len(path) > 1 and k != (len(path)-1):
                        prev_vert = path[k + 1]
                if prev_vert != -1:
                    if flag:
                        new_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                        if not orgraph:
                            new_step.edge_options[(j, prev_vert)] = f' "color": "#89E375"'
                    else:
                        new_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
                        if not orgraph:
                            new_step.edge_options[(j, prev_vert)] += f' "color": "#89E375"'
            elif matrix[j][end] != 0:
                new_step.node_options[j] += f', "color": "#FF6868"'
                for k in range(n):
                    if k != end:
                        if flag:
                            new_step.edge_options[(j, k)] = f' "color": "#659CC1"'
                            if not orgraph:
                                new_step.edge_options[(k, j)] = f' "color": "#659CC1"'
                                new_step.edge_options[(k, end)] = f' "color": "#FF6868"'
                                new_step.edge_options[(end, k)] = f' "color": "#FF6868"'
                        else:
                            new_step.edge_options[(j, k)] += f' "color": "#659CC1"'
                            if not orgraph:
                                new_step.edge_options[(k, j)] += f' "color": "#659CC1"'
                                new_step.edge_options[(k, end)] += f' "color": "#FF6868"'
                                new_step.edge_options[(end, k)] += f' "color": "#FF6868"'
            else:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
        distance_string = f'Находим длину кратчайшего пути из смежных вершин в вершину {end}. <br/>Для этого сравниваем длину кратчайшего пути из веришны {start} в вершину {end} и сумму длины кратчайшего пути из вершины {start} в вершину, смежную вершине {end}, и пути из этой смежной вершины в вершину {end}. <br/>'
        for i in range(n):
            if matrix[i][end] != 0:
                distance_string += f"(х{i}) "
                if dist[end] == dist[i] + matrix[i][end]:
                    distance_string += f"{dist[end]} = {dist[i]} + {matrix[i][end]} <br/>"
                    distance_string += f"Добавляем в путь вершину {i} и рассматриваем ее <br/>"
                    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
                    path.append(i)
                    end = i
                    steps.append(new_step)
                    break
                else:
                    distance_string += f"{dist[end]} =/= {dist[i]} + {matrix[i][end]} <br/>"
        
        # if i == n-1:
        kostil.append(path[-1]) ###
        if kostil[-2] == kostil[-1]: ###
            new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Пути не найдены</p>'
            steps.append(new_step)
            kost_flag = True
            break

    final_step = Step(True, orgraph, True)
    final_step.nodes = all_vertex
    final_step.edges = edges
    distance_string = ''
    flag = True

    for j in all_vertex:
        final_step.node_options[j] = f'label: "x{j}"'
        final_step.node_options[j] += f', shape: "circle"'
        if j in path:
            if j == start:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if l != path[-2]:
                        if flag:
                            final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                        else:
                            final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
            elif j == endend:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if not kost_flag:
                        if l != path[1]:
                            if flag:
                                final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                                final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                            else:
                                final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
                                final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
            else:
                final_step.node_options[j] += f', "color": "#8FBFE0"'
            print(path)
            prev_vert = -1
            for k in range(len(path)):
                if path[k] == j and len(path) > 1 and k != (len(path)-1):
                    prev_vert = path[k + 1]
            if prev_vert != -1:
                if flag:
                    final_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] = f' "color": "#89E375"'
                else:
                    final_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] += f' "color": "#89E375"'
        else:
            final_step.node_options[j] += f', "color": "#8FBFE0"'

    path = list(reversed(path))
    distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: "
    for i in range(len(path)-1):
        distance_string += f"x{path[i]} -> "
    i += 1

    print(dist)
    if len(kostil) == 1:
        distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: x{start} <br/> Длина кратчайшего пути: {dist_sum}"
    elif kostil[-2] != kostil[-1] and dist_sum != math.inf:
        distance_string += f"x{path[i]} <br/> Длина кратчайшего пути: {dist_sum}"
    else:
        distance_string = f"Пути из вершины {start} в вершину {endend} не существует"
    
    final_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
    alg_result.append(final_step)

    return [ alg_input, steps, alg_result ]

def algorithm_Floyd_Warshall(matrix, start = 0, end = 0, orgraph = True):
    if end < 0 or end > (len(matrix)-1):
        end = len(matrix)-1
    if start < 0 or start > (len(matrix)-1):
        start = 0

    n = len(matrix)
        
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                matrix[i][j] *= -1
    
    edges = get_edges(matrix)
    if not orgraph:
        for i in range(len(matrix)):
            j = i
            while j != len(matrix):
                matrix[j][i] = matrix[i][j]
                j += 1

    all_vertex = []
    for i in range(n):
        all_vertex.append(i)
    
    steps = []
    alg_result = []

    alg_input = Step(True, orgraph, True)
    first_line = []
    first_line.append('')

    for i in range(n): 
        first_line.append(f'x{i}')

    alg_input.matrix.append(list(first_line))

    for i in range(n): 
        next_line = []
        next_line.append(f'x{i}')
        next_line += list(matrix[i])
        alg_input.matrix.append(list(next_line))

    for i in range(1, n+1):
        alg_input.matrix[i][i] = -1

    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф по введённой матрице смежности</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#8FBFE0"'

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0 and i != j:
                matrix[i][j] = math.inf

    dist = list(map(lambda p: list(map(lambda q: q, p)), matrix))
    
    for k in range(n):
        line_list = []
        step_string = f'Находим длины кратчайших путей, проходящих через вершину {k}, во все вершины графа. <br/> Для этого сравнивается длина кратчайшего пути из начальной вершины в конечную с суммой длин пути из начальной вершины в вершину {k} и пути из этой вершины в конечную. <br/>' ############
        for i in range(n): 
            step_string += f'<br/>Из вершины {i}: <br/>'
            for j in range(n):
                if dist[i][j] <= dist[i][k] + dist[k][j]:
                    step_string += f'(в х{j}) {dist[i][j]} <= {dist[i][k]} + {dist[k][j]} <br/>'
                else:
                    step_string += f'(в х{j}) {dist[i][j]} > {dist[i][k]} + {dist[k][j]}, обновляем длину кратчайшего пути <br/>'
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
            
            next_line = []
            next_line.append(f'x{i}')
            next_line += list(dist[i])
            line_list.append(next_line)

            new_step = Step(True, orgraph, True)
            new_step.nodes = all_vertex
            new_step.edges = edges
            new_step.step_label = f'Рассматриваем вершину {k} в качестве дополнительной'
            new_step.matrix.append(list(first_line))

            for x in range(len(line_list)):
                new_step.matrix.append(line_list[x])

            new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{step_string}</p>'
            for j in all_vertex:
                new_step.node_options[j] = f'label: "x{j}"'
                new_step.node_options[j] += f', shape: "circle"'
                if j != k:
                    new_step.node_options[j] += f', "color": "#8FBFE0"'
                else:
                    new_step.node_options[j] += f', "color": "#89E375"'
        steps.append(new_step)


    for i in range(n):
        for j in range(n):
            print(dist[i][j], end="  ")
        print(" ")

    path = [end]
    flag= True
    kostil = [end] 
    dist_sum = dist[start][end]
    endend = end
    print()
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end="  ")
        print(" ")

    while end != start:
        new_step = Step(True, orgraph, True)
        new_step.nodes = all_vertex

        new_step.edges = edges
        new_step.step_label = f'Поиск кратчайшего пути из вершины {end} в вершину {start}'
        for j in all_vertex:
            new_step.node_options[j] = f'label: "x{j}"'
            new_step.node_options[j] += f', shape: "circle"'
            if j in path:
                new_step.node_options[j] += f', "color": "#8FBFE0"'
                prev_vert = -1
                for k in range(len(path)):
                    if path[k] == j and len(path) > 1 and k != (len(path)-1):
                        prev_vert = path[k + 1]
                if prev_vert != -1:
                    if flag:
                        new_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                        if not orgraph:
                            new_step.edge_options[(j, prev_vert)] = f' "color": "#89E375"'
                    else:
                        new_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
                        if not orgraph:
                            new_step.edge_options[(j, prev_vert)] += f' "color": "#89E375"'
            elif matrix[j][end] != 0 and matrix[j][end] != math.inf:
                new_step.node_options[j] += f', "color": "#FF6868"'
                for k in range(n):
                    if k != end:
                        if flag:
                            new_step.edge_options[(j, k)] = f' "color": "#659CC1"'
                            if not orgraph:
                                new_step.edge_options[(k, j)] = f' "color": "#659CC1"'
                                new_step.edge_options[(k, end)] = f' "color": "#FF6868"'
                                new_step.edge_options[(end, k)] = f' "color": "#FF6868"'
                        else:
                            new_step.edge_options[(j, k)] += f' "color": "#659CC1"'
                            if not orgraph:
                                new_step.edge_options[(k, j)] += f' "color": "#659CC1"'
                                new_step.edge_options[(k, end)] += f' "color": "#FF6868"'
                                new_step.edge_options[(end, k)] += f' "color": "#FF6868"'
            else:
                new_step.node_options[j] += f', "color": "#8FBFE0"'

        distance_string = f'Находим длину кратчайшего пути из смежных вершин в вершину {end}. <br/>Для этого сравниваем длину кратчайшего пути из веришны {start} в вершину {end} и сумму длины кратчайшего пути из вершины {start} в вершину, смежную вершине {end}, и пути из этой смежной вершины в вершину {end}. <br/>'
        for i in range(n):
            if matrix[i][end] != 0:
                distance_string += f"(х{i}) "
                if dist[start][end] == dist[start][i] + matrix[i][end]:
                    distance_string += f"{dist[start][end]} = {dist[start][i]} + {matrix[i][end]} <br/>"
                    distance_string += f"Добавляем в путь вершину {i} и рассматриваем ее <br/>"
                    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
                    path.append(i)
                    end = i
                    steps.append(new_step)
                    break
                else:
                    distance_string += f"{dist[start][end]} =/= {dist[start][i]} + {matrix[i][end]} <br/>"
        

        kostil.append(path[-1]) 
        if kostil[-2] == kostil[-1]: 
            new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Пути не найдены</p>'
            steps.append(new_step)
            break

    final_step = Step(True, orgraph, True)
    final_step.nodes = all_vertex
    final_step.edges = edges
    distance_string = ''
    flag = True
    for j in all_vertex:
        final_step.node_options[j] = f'label: "x{j}"'
        final_step.node_options[j] += f', shape: "circle"'
        
        if j in path:
            if j == start:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if l != path[-2]:
                        if flag:
                            final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                        else:
                            final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
                            final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
            elif j == endend:
                final_step.node_options[j] += f', "color": "#89E375"'
                for l in range(n):
                    if l != path[1]:
                        if flag:
                            final_step.edge_options[(l, j)] = f' "color": "#8FBFE0"'
                            final_step.edge_options[(j, l)] = f' "color": "#8FBFE0"'
                        else:
                            final_step.edge_options[(l, j)] += f' "color": "#8FBFE0"'
                            final_step.edge_options[(j, l)] += f' "color": "#8FBFE0"'
            else:
                final_step.node_options[j] += f', "color": "#8FBFE0"'
            print(path)
            prev_vert = -1
            for k in range(len(path)):
                if path[k] == j and len(path) > 1 and k != (len(path)-1):
                    prev_vert = path[k + 1]
            if prev_vert != -1:
                if flag:
                    final_step.edge_options[(prev_vert, j)] = f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] = f' "color": "#89E375"'
                else:
                    final_step.edge_options[(prev_vert, j)] += f' "color": "#89E375"'
                    if not orgraph:
                        final_step.edge_options[(j, prev_vert)] += f' "color": "#89E375"'
        else:
            final_step.node_options[j] += f', "color": "#8FBFE0"'

    path = list(reversed(path))
    distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: "

    for i in range(len(path)-1):
        distance_string += f"x{path[i]} -> "
    i += 1

    if len(kostil) == 1:
        distance_string = f"Кратчайший путь из вершины {start} в вершину {endend}: x{start} <br/> Длина кратчайшего пути: {dist_sum}"
    elif kostil[-2] != kostil[-1] and dist_sum != math.inf:
        distance_string += f"x{path[i]} <br/> Длина кратчайшего пути: {dist_sum}"
    else:
        distance_string = f"Пути из вершины {start} в вершину {endend} не существует"
    
    final_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">{distance_string}</p>'
    alg_result.append(final_step)
    

    return [ alg_input, steps, alg_result ]

