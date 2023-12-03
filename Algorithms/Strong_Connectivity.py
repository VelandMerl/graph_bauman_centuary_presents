from Algorithms.Usefull_elements import Step, intersection, addition, get_edges, invert_Graph
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
    
    alg_input = Step(True)
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>'
    alg_input.nodes = all_vertex
    alg_input.edges = edges
    for i in all_vertex:
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', "color": "#FFFFFF"'
    
    queue = []
    finished = []

    while len(tracked_vertex) > 0:
        new_step = Step(True)
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
        forward_line = '{ '
        forward_line += f'x<sub>{forward_closure[0]}</sub>'
        for i in range(1, len(forward_closure)):
            forward_line += f', x<sub>{forward_closure[i]}</sub>'
        forward_line += ' }'
        line += forward_line
        line += '</p>'
        new_step.text += line
        # reverse_closure line
        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Г<sup>-n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '
        reverse_line = '{ '
        reverse_line += f'x<sub>{reverse_closure[0]}</sub>'
        for i in range(1, len(reverse_closure)):
            reverse_line += f', x<sub>{reverse_closure[i]}</sub>'
        reverse_line += ' }'
        line += reverse_line
        line += '</p>'
        new_step.text += line

        # equivalence_class line
        class_line = '{ '
        class_line += f'x<sub>{equivalence_class[0]}</sub>'
        for i in range(1, len(equivalence_class)):
            class_line += f', x<sub>{equivalence_class[i]}</sub>'
        class_line += ' }'

        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">C<sub>x<sub>{vertex_to_review}</sub></sub> = '
        line += f'Г<sup>n</sup><sub>x<sub>{vertex_to_review}</sub></sub> &cap; Г<sup>-n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '
        line += forward_line + ' &cap; ' + reverse_line + ' = ' + class_line
        line += '</p>'
        new_step.text += line
        graph_class_arr.append(equivalence_class)

        print(forward_closure)
        print(reverse_closure)
        # готовим граф
        new_step.nodes = all_vertex
        for i in all_vertex:
            new_step.node_options[i] = f'label: "x{i}"'
        for i in forward_closure:
            new_step.node_options[i] += f', "color": "#1683DF"'
        for i in reverse_closure:
            new_step.node_options[i] += f', "color": "#B900FF"'
        for i in equivalence_class:
            new_step.node_options[i] += f', "color": "#2B912D"'
        print(untracked_vertex)
        for i in untracked_vertex:
            new_step.node_options[i] += f', "color": "#BCBCBC"'
        print(unreachable_vertex)
        for i in unreachable_vertex:
            new_step.node_options[i] += f', "color": "#FF2400"'

        for element in graph_class_arr[len(graph_class_arr)-1]:
            tracked_vertex.remove(element)
        steps.append(new_step)
    print(graph_class_arr)
    new_step = Step(True)
    new_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины закончились. Алгоритм завершён</p>'
    new_step.nodes = all_vertex
    new_step.edges = edges
    new_step.step_label = 'Завершение алгоритма'
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i}"'
        new_step.node_options[i] += f', "color": "#BCBCBC"'
    steps.append(new_step)
    return [ alg_input, steps ]

def algorithm_Kosaraju(matrix):
    size_of_matrix = len(matrix)
    steps = []
    edges = get_edges(matrix)
    marks = []
    for i in range(size_of_matrix):
        marks.append('?')
    queue = []
    
    iterator = 0

    visited = []

    for vertex in range(0, size_of_matrix):
        if vertex in visited: continue
        queue.clear()
        queue.append(vertex)
        while len(queue) > 0:
            curr_vertex = queue.pop()
            if not(curr_vertex in visited):
                for i in range(size_of_matrix):
                    if matrix[curr_vertex][i] > 0 and marks[i] == '?':
                        queue.append(curr_vertex)
                        queue.append(i)
                    visited.append(curr_vertex)
            iterator += 1
            marks[curr_vertex] = iterator
    
    print(marks)

    invert_matrix = invert_Graph(matrix)

    graph_class_arr = []
    print(graph_class_arr)

    queue = []
    visited = []

    vertex_mark_list = []

    for i in range(size_of_matrix):
        vertex_mark_list.append((i, marks[i]))
    
    vertex_mark_list.sort(key = lambda x: (x[1], x[0]), reverse = True)
    print(vertex_mark_list)

    while len(vertex_mark_list) > 0:
        curr_vertex = vertex_mark_list.pop(0)[0]
        if curr_vertex in visited: continue

        graph_class = []
        graph_class.append(curr_vertex)
        visited.append(curr_vertex)
        queue.clear()
        queue.append(curr_vertex)
        while len(queue) > 0:
            curr_vertex = queue.pop()
            for i in range(size_of_matrix):
                if invert_matrix[curr_vertex][i] > 0 and not (i in visited):
                    queue.append(i)
                    graph_class.append(i)
                    visited.append(i)
        graph_class_arr.append(graph_class)
    
    print(graph_class_arr)
    