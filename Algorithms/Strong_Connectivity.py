from Algorithms.Usefull_elements import Step, intersection, addition, get_edges, invert_Graph, vertex_list_to_str, hsv_to_hex
# Серые - больше не рассматриваются untracked_vertex
# Синие - можно только добраться forward_closure
# Зелёные - можно до них добраться и от них добраться equivalence_class
# Фиолетовые - от них можно добраться reverse_closure
# Красные - нельзя ни добраться ни от них добраться unreachable_vertex

def algorithm_Malgrange(matrix):
    size_of_matrix = len(matrix)
    steps = []
    edges = get_edges(matrix)

    forward_closure = []
    reverse_closure = []

    graph_class_arr = []
    tracked_vertex = []

    all_vertex = []

    for i in range(0, size_of_matrix):
        tracked_vertex.append(i)
        all_vertex.append(i)
    
    alg_input = Step(True, True, True)
    first_line = []
    first_line.append('')
    for i in range(0, size_of_matrix):
        first_line.append(f'x<sub>{i}</sub>')
    alg_input.matrix.append(list(first_line))
    for i in range(0, size_of_matrix):
        next_line = []
        next_line.append(f'x<sub>{i}</sub>')
        next_line += (list(matrix[i]))
        alg_input.matrix.append(list(next_line))
    for i in range(1, size_of_matrix+1):
        alg_input.matrix[i][i] = -1
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'
    
    queue = []
    finished = []
    prev_matrix = []
    for i in alg_input.matrix:
        prev_matrix.append(list(i))
    while len(tracked_vertex) > 0:
        new_step = Step(True, True, True)
        for i in prev_matrix:
            new_step.matrix.append(list(i))
        new_step.edges = edges
        new_step.step_label = ''
        forward_closure.clear()
        reverse_closure.clear()
        vertex_to_review = tracked_vertex[0]

        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Рассмотрим вершину x<sub>{vertex_to_review}</sub>.</p>'

        #forward
        queue.clear()
        queue.append(tracked_vertex[0])
        forward_closure.append(tracked_vertex[0])
        finished.clear()

        while len(queue) > 0:
            curr_vertex = queue.pop(0)
            if curr_vertex in finished: continue
            else: finished.append(curr_vertex)
            for i in range(0, size_of_matrix):
                if matrix[curr_vertex][i] > 0 and not (i in forward_closure) and i in tracked_vertex:
                    queue.append(i)
                    forward_closure.append(i)
        #reverse
        queue.clear()
        queue.append(tracked_vertex[0])
        reverse_closure.append(tracked_vertex[0])
        finished.clear()

        while len(queue) > 0:
            curr_vertex = queue.pop(0)
            if curr_vertex in finished: continue
            else: finished.append(curr_vertex)
            for i in range(0, size_of_matrix):
                if matrix[i][curr_vertex] > 0 and not (i in reverse_closure) and i in tracked_vertex:
                    queue.append(i)
                    reverse_closure.append(i)

        equivalence_class = intersection(forward_closure, reverse_closure)
        untracked_vertex = addition(all_vertex, tracked_vertex)
        unreachable_vertex = addition(addition(addition(all_vertex, forward_closure), reverse_closure), untracked_vertex)

        forward_closure.sort()
        reverse_closure.sort()
        equivalence_class.sort()

        # forward_closure line
        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Г<sup>n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '

        forward_line = vertex_list_to_str(forward_closure)

        line += forward_line
        line += '</p>'
        new_step.text += line
        # reverse_closure line
        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Г<sup>-n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '
        
        reverse_line = vertex_list_to_str(reverse_closure)

        line += reverse_line
        line += '</p>'
        new_step.text += line

        # equivalence_class line
        class_line = vertex_list_to_str(equivalence_class)


        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">C<sub>x<sub>{vertex_to_review}</sub></sub> = '
        line += f'Г<sup>n</sup><sub>x<sub>{vertex_to_review}</sub></sub> &cap; Г<sup>-n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '
        line += forward_line + ' &cap; ' + reverse_line + ' = ' + class_line
        line += '</p>'
        new_step.text += line
        graph_class_arr.append(equivalence_class)

        # готовим граф
        new_step.nodes = all_vertex
        for i in all_vertex:
            new_step.node_options[i] = f'label: "x{i}"'
            new_step.node_options[i] += f', shape: "circle"'
        for i in forward_closure:
            if not (i in equivalence_class):
                new_step.node_options[i] += f', "color": "#1683DF"'
        for i in reverse_closure:
            if not (i in equivalence_class):
                new_step.node_options[i] += f', "color": "#B900FF"'
        for i in equivalence_class:
            new_step.node_options[i] += f', "color": "#2B912D"'
        for i in untracked_vertex:
            new_step.node_options[i] += f', "color": "#BCBCBC"'
        for i in unreachable_vertex:
            new_step.node_options[i] += f', "color": "#FF2400"'

        for element in graph_class_arr[len(graph_class_arr)-1]:
            tracked_vertex.remove(element)

        position = len(new_step.matrix[1])
        for i in range(size_of_matrix):
            if i in forward_closure:
                new_step.matrix[i+1].append(f'&#10004;')
            elif i in untracked_vertex:
                new_step.matrix[i+1].append('/')
            else:
                new_step.matrix[i+1].append('&#10006;')
        closure_line = []
        closure_line.append(f'Г<sup>-n</sup><sub>х<sub>{vertex_to_review}</sub></sub>')
        for i in range(size_of_matrix):
            if i in reverse_closure:
                closure_line.append(f'&#10004;')
            elif i in untracked_vertex:
                closure_line.append('/')
            else:
                closure_line.append('&#10006;')
        new_step.matrix.append(closure_line)
        new_step.matrix[0].append(f'Г<sup>n</sup><sub>х<sub>{vertex_to_review}</sub></sub>')
        prev_matrix = []
        for i in new_step.matrix:
            prev_matrix.append(list(i))
        
        steps.append(new_step)
    new_step = Step(True, True, True)
    closure_line = []
    closure_line.append('')
    for i in range(size_of_matrix):
        closure_line.append('/')
    prev_matrix.append(closure_line)
    for i in range(size_of_matrix):
        prev_matrix[i+1].append('&nbsp;&nbsp;/&nbsp;')
    for i in prev_matrix:
        new_step.matrix.append(list(i))
    new_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины закончились. Алгоритм завершён</p>'
    new_step.nodes = all_vertex
    new_step.edges = edges
    new_step.step_label = 'Завершение алгоритма'
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i}"'
        new_step.node_options[i] += f', shape: "circle"'
        new_step.node_options[i] += f', "color": "#BCBCBC"'
    steps.append(new_step)
    hue_step = 0.1 # шаг hue меняет цвет
    alg_result = []
    result_step = Step(True, True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Компоненты сильной связности:</p>'
    for graph_class in graph_class_arr:
        result_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">C<sub>x<sub>{graph_class[0]}</sub></sub> = {vertex_list_to_str(graph_class)}</p>'
    result_step.nodes = all_vertex
    result_step.edges = edges
    for i in all_vertex:
        result_step.node_options[i] = f'label: "x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        
        for color_offset in range(len(graph_class_arr)):
            if i in graph_class_arr[color_offset]:
                result_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 0.9)}"'
    alg_result.append(result_step)
    result_step = Step(True, True, True)
    for i in prev_matrix:
        result_step.matrix.append(list(i))
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф компонент сильной связности и таблица:</p>'
    for i in graph_class_arr:
        result_step.nodes.append(i[0])
    
    graph_class_edges = {}
    for graph_class in graph_class_arr:
        for i in graph_class:
            for j in range(size_of_matrix):
                if matrix[i][j] > 0 and not (j in graph_class):
                    for each_class in graph_class_arr:
                        if j in each_class:
                            graph_class_edges[(graph_class[0], each_class[0])] = matrix[i][j]
                            break
    result_step.edges = graph_class_edges

    for i in result_step.nodes:
        result_step.node_options[i] = f'label: "C | x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        
        for color_offset in range(len(graph_class_arr)):
            if i in graph_class_arr[color_offset]:
                result_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
    alg_result.append(result_step)
    return [ alg_input, steps, alg_result ]

####################################################################################################
####################################################################################################
####################################################################################################

def algorithm_Kosaraju(matrix):
    size_of_matrix = len(matrix)
    steps = []
    edges = get_edges(matrix)
    marks = []
    all_vertex = []

    for i in range(size_of_matrix):
        marks.append('?')
        all_vertex.append(i)
    
    alg_input = Step(True, True, True)
    first_line = []
    first_line.append('')
    for i in range(0, size_of_matrix):
        first_line.append(f'x{i}')
    alg_input.matrix.append(list(first_line))
    for i in range(0, size_of_matrix):
        next_line = []
        next_line.append(f'x{i}')
        next_line += (list(matrix[i]))
        alg_input.matrix.append(list(next_line))
    for i in range(1, size_of_matrix+1):
        alg_input.matrix[i][i] = -1
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'
    
    queue = []
    
    iterator = 0

    visited = []

    for vertex in range(0, size_of_matrix):
        if vertex in visited: continue
        new_step = Step(True, True)
        not_visited = addition(all_vertex, visited)
        visited.sort()
        not_visited.sort()
        new_step.step_label = f"Разметка графа. Начало обхода в глубину от вершины x{vertex}"
        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины с метками: {vertex_list_to_str(visited)}</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">В графе остались вершины без меток: {vertex_list_to_str(not_visited)}</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим в стек обхода вершину x<sub>{vertex}</sub> и выполним обход графа в глубину</p>'
        new_step.nodes = all_vertex
        new_step.edges = edges
        for i in all_vertex:
            new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
            new_step.node_options[i] += f', shape: "circle"'
            if i in not_visited:
                new_step.node_options[i] += f', "color": "#E9636E"'
            else:
                new_step.node_options[i] += f', "color": "#AED585"'
        steps.append(new_step)

        queue.clear()
        queue.append(vertex)
        while len(queue) > 0:
            start_stack = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Состояние стека обхода графа в глубину в начале шага: {vertex_list_to_str(queue)} &#9668; Вершина стека</p>'

            curr_vertex = queue.pop()
            iterator += 1
            marks[curr_vertex] = iterator

            set_mark_text = '<p class="mb-2 text-gray-500 dark:text-gray-400">'
            not_marked_neighbor = []
            if not(curr_vertex in visited):
                set_mark_text += f'У данной вершины нет метки. Значение итератора равно {iterator}. Дадим вершине х<sub>{curr_vertex}</sub> метку {iterator}.'
                for i in range(size_of_matrix):
                    if matrix[curr_vertex][i] > 0 and marks[i] == '?':
                        queue.append(curr_vertex)
                        queue.append(i)
                        not_marked_neighbor.append(i)
                visited.append(curr_vertex)
            set_mark_text += '</p>'
            # формирование шага для обхода в глубину
            new_step = Step(True, True)
            new_step.step_label = f"Разметка графа. Обход в глубину от вершины x{vertex}"
            new_step.text = start_stack
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Возьмём вершину из стека. Это оказалась вершина x<sub>{curr_vertex}</sub></p>'
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Рассмотрим вершину x<sub>{curr_vertex}</sub></p>'
            new_step.text += set_mark_text
            if len(not_marked_neighbor) == 0:
                new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Непомеченных соседних вершин нет. Значит, в стек обхода текущую вершину x<sub>{curr_vertex}</sub> не добавляем.</p>'
            else:
                new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Непомеченные соседние вершины: {vertex_list_to_str(not_marked_neighbor)}</p>'
                new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Поскольку есть непомеченные соседние вершины, то сохраняем текущую вершину x<sub>{curr_vertex}</sub> в стек обхода. После этого добавляем непомеченные соседние вершины</p>'
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Состояние стека обхода графа в глубину в конце шага: {vertex_list_to_str(queue)} &#9668; Вершина стека</p>'
            new_step.nodes = all_vertex
            new_step.edges = edges
            for i in all_vertex:
                new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
                new_step.node_options[i] += f', shape: "circle"'
                if i == curr_vertex:
                    new_step.node_options[curr_vertex] += f', "color": "#2B912D"'
                elif i in not_marked_neighbor:
                    new_step.node_options[i] += f', "color": "#F5CAA8"'
                else:
                    new_step.node_options[i] += f', "color": "#FFFFFF"'
            
            steps.append(new_step)
        new_step = Step()
        new_step.step_label = f"Разметка графа. Конец обхода в глубину от вершины x{vertex}"
        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Стек обхода графа в глубину пуст.</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Конец обхода графа в глубину от вершины x<sub>{vertex}</sub></p>'
        steps.append(new_step)

    new_step = Step(True, True)
    visited.sort()
    new_step.step_label = f"Конец разметки графа"
    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины с метками: {vertex_list_to_str(visited)}</p>'
    new_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Вершин без меток не осталось: { }</p>'
    new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Все вершины размечены</p>'
    new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Конец разметки графа</p>'
    new_step.nodes = all_vertex
    new_step.edges = edges
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
        new_step.node_options[i] += f', shape: "circle"'
        new_step.node_options[i] += f', "color": "#AED585"'
    steps.append(new_step)   

    invert_matrix = invert_Graph(matrix, size_of_matrix)
    inverted_edges = get_edges(invert_matrix)
    new_step = Step(True, True)
    visited.sort()
    new_step.step_label = f"Инверсия рёбер матрицы"
    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Инвертируем рёбра матрицы, инвертировав матрицу смежности</p>'
    new_step.nodes = all_vertex
    new_step.edges = inverted_edges
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
        new_step.node_options[i] += f', shape: "circle"'
        new_step.node_options[i] += f', "color": "#FFFFFF"'
    steps.append(new_step)   

    graph_class_arr = []

    queue = []
    visited = []

    vertex_mark_list = []

    for i in range(size_of_matrix):
        vertex_mark_list.append((i, marks[i]))
    
    vertex_mark_list.sort(key = lambda x: (x[1], x[0]), reverse = True)

    hue_step = 0.1 # шаг hue меняет цвет

    while len(vertex_mark_list) > 0:
        
        curr_vertex = vertex_mark_list.pop(0)[0]
        class_vertex = curr_vertex
        if curr_vertex in visited: continue

        new_step = Step(True, True)
        not_visited = addition(all_vertex, visited)
        visited.sort()
        not_visited.sort()
        new_step.step_label = f"Выделение компонентов сильной связности. Начало обхода в глубину от вершины x{curr_vertex}"
        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины, добавленные в компоненты сильной связности: {vertex_list_to_str(visited)}</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины, не добавленные в компоненты сильной связности: {vertex_list_to_str(not_visited)}</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Добавим в стек обхода вершину с наибольшей меткой, то есть вершину x<sub>{curr_vertex}</sub> и выполним обход графа в глубину</p>'
        # new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Также добавим вершину x<sub>{curr_vertex}</sub> в компоненту сильной связности C<sub>x<sub>{class_vertex}</sub></sub></p>'
        new_step.nodes = all_vertex
        new_step.edges = inverted_edges
        for i in all_vertex:
            new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
            new_step.node_options[i] += f', shape: "circle"'
            if i in not_visited:
                new_step.node_options[i] += f', "color": "#FFFFFF"'
            else:
                for color_offset in range(len(graph_class_arr)):
                    if i in graph_class_arr[color_offset]:
                        new_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
        steps.append(new_step)

        graph_class = []
        # graph_class.append(curr_vertex)
        # visited.append(curr_vertex)
        queue.clear()
        queue.append(curr_vertex)
        while len(queue) > 0:
            added_to_class = []
            start_stack = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Состояние стека обхода графа в глубину в начале шага: {vertex_list_to_str(queue)} &#9668; Вершина стека</p>'
            curr_vertex = queue.pop()
            if curr_vertex in visited: continue
            graph_class.append(curr_vertex)
            visited.append(curr_vertex)
            for i in range(size_of_matrix):
                if invert_matrix[curr_vertex][i] > 0 and not (i in visited):
                    queue.append(i)
                    added_to_class.append(i)

            new_step = Step(True, True)
            not_visited = addition(all_vertex, visited)
            visited.sort()
            not_visited.sort()
            new_step.step_label = f"Выделение компонентов сильной связности. Обход в глубину от вершины x{class_vertex}"
            new_step.text = start_stack
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Возьмём вершину из стека. Это оказалась вершина x<sub>{curr_vertex}</sub></p>'
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Рассмотрим вершину x<sub>{curr_vertex}</sub>. Добавим её в компоненту сильной связности C<sub>x<sub>{class_vertex}</sub></sub></p>'
            if len(added_to_class) == 0:
                new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Нет соседних вершин, не добавленных в компоненты сильной связности: {vertex_list_to_str(added_to_class)}</p>'
            else:
                new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Соседние вершины, не добавленные в компоненты сильной связности: {vertex_list_to_str(added_to_class)}. Добавим их в стек обхода</p>'
            new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Состояние стека обхода графа в глубину в конце шага: {vertex_list_to_str(queue)} &#9668; Вершина стека</p>'
            new_step.nodes = all_vertex
            new_step.edges = inverted_edges
            for i in all_vertex:
                new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
                new_step.node_options[i] += f', shape: "circle"'
                if i in not_visited:
                    new_step.node_options[i] += f', "color": "#FFFFFF"'
                else:
                    color_offset = 0
                    for color_offset in range(len(graph_class_arr)):
                        if i in graph_class_arr[color_offset]:
                            new_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
                    color_offset += 1
                    if i in graph_class:
                        new_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
            steps.append(new_step)
        graph_class_arr.append(graph_class)
        new_step = Step()
        new_step.step_label = f"Выделение компонентов сильной связности. Конец обхода в глубину от вершины x{class_vertex}"
        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Стек обхода графа в глубину пуст.</p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Конец выделения компоненты сильной связности от вершины x<sub>{vertex}</sub></p>'
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">Получена компонента C<sub>x<sub>{class_vertex}</sub></sub> = {vertex_list_to_str(graph_class)}</p>'
        steps.append(new_step)
    new_step = Step(True, True)
    visited.sort()
    new_step.step_label = f"Конец выделения компонентов сильной связности"
    new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины, добавленные в компоненты сильной связности: {vertex_list_to_str(visited)}</p>'
    new_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Нет вершин, не добавленных в компоненты сильной связности: { }</p>'
    new_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Все вершины распределены по компонентам сильной связности</p>'
    new_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Конец выделения компонентов сильной связности</p>'
    new_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Полученные компоненты сильной связности:</p>'
    for graph_class in graph_class_arr:
        new_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">C<sub>x<sub>{graph_class[0]}</sub></sub> = {vertex_list_to_str(graph_class)}</p>'
    new_step.nodes = all_vertex
    new_step.edges = inverted_edges
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i} | {marks[i]}"'
        new_step.node_options[i] += f', shape: "circle"'
        if i in not_visited:
            new_step.node_options[i] += f', "color": "#FFFFFF"'
        else:
            for color_offset in range(len(graph_class_arr)):
                if i in graph_class_arr[color_offset]:
                    new_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
    steps.append(new_step)   


    
    alg_result = []
    result_step = Step(True, True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Компоненты сильной связности:</p>'
    for graph_class in graph_class_arr:
        result_step.text += f'<p class="mb-2 text-gray-500 dark:text-gray-400">C<sub>x<sub>{graph_class[0]}</sub></sub> = {vertex_list_to_str(graph_class)}</p>'
    result_step.nodes = all_vertex
    result_step.edges = edges
    for i in all_vertex:
        result_step.node_options[i] = f'label: "x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        if i in not_visited:
            result_step.node_options[i] += f', "color": "#FFFFFF"'
        else:
            for color_offset in range(len(graph_class_arr)):
                if i in graph_class_arr[color_offset]:
                    result_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
    alg_result.append(result_step)
    result_step = Step(True, True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф компонент сильной связности:</p>'
    for i in graph_class_arr:
        result_step.nodes.append(i[0])
    
    graph_class_edges = {}
    for graph_class in graph_class_arr:
        for i in graph_class:
            for j in range(size_of_matrix):
                if matrix[i][j] > 0 and not (j in graph_class):
                    for each_class in graph_class_arr:
                        if j in each_class:
                            graph_class_edges[(graph_class[0], each_class[0])] = matrix[i][j]
                            break
    result_step.edges = graph_class_edges

    for i in result_step.nodes:
        result_step.node_options[i] = f'label: "C | x{i}"'
        result_step.node_options[i] += f', shape: "circle"'
        if i in not_visited:
            result_step.node_options[i] += f', "color": "#FFFFFF"'
        else:
            for color_offset in range(len(graph_class_arr)):
                if i in graph_class_arr[color_offset]:
                    result_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
    alg_result.append(result_step)
    return [ alg_input, steps, alg_result]