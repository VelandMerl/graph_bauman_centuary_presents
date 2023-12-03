from Algorithms.Usefull_elements import Step, intersection, addition, get_edges
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
    
    queue = []
    finished = []

    while len(tracked_vertex) > 0:
        new_step = Step(True)
        new_step.edges = edges
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
        new_step.nodes = list(all_vertex)
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
    return steps