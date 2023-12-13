from Algorithms.Usefull_elements import Step, intersection, addition, get_edges, invert_Graph, vertex_list_to_str, hsv_to_hex, replace_color
import copy

def algorithm_depth_first_search(matrix):
    mass = list() # массив смежных вершин
    vertex_mark = dict() # объявление пустого словаря (соотв. вершин меткам)
    vertex = list() # объявление пустого списка (вершины без меток)
    stack = list() # объявление пустого списка (стек)
    all_vertex = [] # список вершин
    steps = [] # список шагов
    alg_result = [] # шаг-результат
    edges = [] # список рёбер
    route = [] # маршрут
    loop = False # нет контура

    # вложенная функция, реализующая алгоритм
    def dfs(prev_ver, cur_ver):
        print(f' Текущая вершина: {cur_ver}')
        #h_step.node_options[cur_ver] = replace_color(h_step.node_options[cur_ver], "#DC143C") # изменение цвета по маршруту
        h_step.node_options[cur_ver] += ', borderWidth: 3, color: {border: "#DC143C", background: "#1E90FF", highlight: { border: "#DC143C" }}'; # изменение цвета границы по маршруту
        vertex_mark[cur_ver] = False # вершина просмотрена
        while mass[cur_ver]: # пока есть смежные вершины
            # h_step.edge_options[(cur_ver, mass[cur_ver][0])] += replace_color(h_step.edge_options[(cur_ver, mass[cur_ver][0])], "#DC143C")  # подкрашиваем ребро 
            if vertex_mark[mass[cur_ver][0]] == None: # МОЖЕТ БЫТЬ ПЕТЛЯ or vertex_mark[mass[cur_ver][0]] == False
                h_step.edge_options[(cur_ver, mass[cur_ver][0])] += ', "color": "#DC143C", width: 3'  # подкрашиваем ребро
            if vertex_mark[mass[cur_ver][0]] == None:
                print(f' Переходим к смежной вершине: {mass[cur_ver][0]}')
                route.append(cur_ver) # добавляем вершину в маршрут
                # переходим к первой смежной вершине
                if not dfs(cur_ver, mass[cur_ver][0]): # обнаружен контур
                    return False
                print(f' Возвращаемся к вершине {cur_ver}')
                h_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Возвращаемся к вершине {cur_ver}</p>' + h_step.text
                print(f' Текущая вершина: {cur_ver}')
                mass[cur_ver].pop(0) # удаляем просмотренную смежную вершину
            elif vertex_mark[mass[cur_ver][0]]:
                mass[cur_ver].pop(0) # удаляем просмотренную смежную вершину
            else:
                return False # обнаружен контур
        print(f'Смежных непомеченных вершин нет, помещаем в стек вершину {cur_ver}')
        vertex_mark[cur_ver] = True # определён порядок вершины
        stack.append(cur_ver) # помещаем вершину в стек
        vertex.remove(cur_ver) # исключаем вершину для повторного просмотра

        for ver in route:
            h_step.text += f'{ver}->'
        if route:
            route.pop()
            h_step.text += f'{cur_ver}</p><p class="mb-2 text-gray-500 dark:text-gray-400">Вершина {cur_ver} не имеет смежных вершин, добавляем её в стек {stack}</p>' # последний текст шага
        else:
            h_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Возвращаемся к вершине {cur_ver}</p><p class="mb-2 text-gray-500 dark:text-gray-400">Некуда шагать!</p><p class="mb-2 text-gray-500 dark:text-gray-400">Вершина {cur_ver} не имеет смежных вершин, добавляем её в стек {stack}</p>' # последний текст шага
        h_step.step_label = f'Добавление вершины x<sub>{cur_ver}</sub>&nbsp;в стек' # название шага
        h_step.node_options[cur_ver] += ', borderWidth: 1, "color": "#00FA9A"' # изменение цвета
        
        new_step = copy.deepcopy(h_step)
        h_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Маршрут обхода: ' # текст шага
        if prev_ver != cur_ver and (prev_ver, cur_ver) in edges:
            h_step.edge_options[(prev_ver, cur_ver)] += ', "color": "#1E90FF", width: 1'  # возвращаем цвет ребру
        # print(new_step.edge_options)
        steps.append(new_step) # добавляем шаг в список
        new_step = Step(True, True) # создаём новый шаг

        return True

    # инициализация
    size_of_matrix = len(matrix) # получаем размер матрицы
    for i in range(size_of_matrix):
        # словарь соответствия исходных вершин меткам
        vertex_mark.update({i: None})
        # формирование множеста непомеченных вершин
        vertex.append(i)
        # формирование массива смежных вершин
        neighbor = list() # смежные вершины
        for j in range(size_of_matrix):
            if matrix[i][j] == 1:
                neighbor.append(j)
        mass.append(neighbor)
        edges = get_edges(matrix) # список рёбер
    all_vertex = vertex.copy()

    # исходный граф
    alg_input = Step(True, True) # создаём первый шаг (исходный граф)
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Это граф по введённой матрице</p>' # текст шага
    alg_input.nodes = all_vertex # список вершин
    alg_input.edges = edges # список ребер

    # общие опции для рёбер
    for edge in edges.keys():
        alg_input.edge_options[edge] = 'label: "1"'
        alg_input.edge_options[edge] += ', "color": "#1E90FF"'
    print(f'рёбра: {alg_input.edge_options}')


    for i in all_vertex: # метки для вершин
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += ', shape: "circle"'
        alg_input.node_options[i] += ', "color": "#1E90FF"'


    # alg_input.edge_options[(0, 1)] += f', "color": "#FF69B4'
   
    # print(f'Исходный граф: {alg_input.node_options}')

    # steps.append(alg_input)

    # выбор начальной вершины обхода
    h_step = copy.deepcopy(alg_input) # создаём вспомогательный объект (шаг)
    print(vertex)
    while vertex:
        new_step = copy.deepcopy(alg_input) # создаём первый шаг
        h_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Маршрут обхода: ' # текст шага
        if not dfs(0, vertex[0]): # запуск алгоритма
            loop = True
            print('Выполнение алгоритма прервано из-за наличия контура')
            break
    print(f'Вершины в стеке:', list(map(lambda el: el, stack)))
    if not loop:
        print('Алгоритм успешно завершен')

        result_step = copy.deepcopy(alg_input)
        result_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Стек - {stack} ({stack[-1]} - вершина стека)</p>'
        result_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Это граф, разбитый на уровни</p>' # текст шага
        stack.reverse() # переворачиваем список для следования вершин по уровням
        for ver in stack: # установка уровней для вершин
            result_step.node_options[ver] = f'label: "x{ver}"'
            result_step.node_options[ver] += ', shape: "circle"'
            result_step.node_options[ver] += ', "color": "#1E90FF"'
            result_step.node_options[ver] += f', level: {stack.index(ver)}'
        
        neighbor_ver = [] # пары вершин соседних уровней
        for i in range(len(stack)-1):
            neighbor_ver.append(tuple([stack[i], stack[i+1]]))

        result_step.general_options += ', layout: { hierarchical: { direction: "LR", levelSeparation: 100} }'
        flag = True
        for edge in edges.keys():
            # result_step.edge_options[edge] = 'smooth: { "enabled": true, "type": "curvedCCW", "forceDirection": "none" }, width: 1'
            if edge in neighbor_ver:
                result_step.edge_options[edge] = 'smooth: { "enabled": true, "type": "dynamic", roundness: 0 }, width: 1'    
            elif flag:
                result_step.edge_options[edge] = 'smooth: { "enabled": true, "type": "curvedCW", roundness: 0.5 }, width: 1'
                flag = False
            else:
                result_step.edge_options[edge] = 'smooth: { "enabled": true, "type": "curvedCCW", roundness: 0.5 }, width: 1'
                flag = True
            
        alg_result.append(result_step)
    else:
        print('ОШИБКА')
        result_step = Step(True, True)
        result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400"">АЛГОРИТМ ПРЕРВАН ИЗ-ЗА НАЛИЧИЯ КОНТУРА В ГРАФЕ!</p>' # текст шага
        alg_result.append(result_step)

    return [ alg_input, steps, alg_result ]  
    
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
def check(matrix):
    size_of_matrix = len(matrix) # размер матрицы
    steps = []
    all_vertex = [] # список вершин
    edges = get_edges(matrix) # список рёбер
    

    # forward_closure = [] # прямое т. замыкание
    # reverse_closure = [] # обратное т. замыкание

    # graph_class_arr = []
    # tracked_vertex = [] # ДЛЯ АЛГОРИТМА (ОТСЛЕЖИВАЕМЫЕ ВЕРШИНЫ)


    for i in range(size_of_matrix): # создание списка вершин
        # tracked_vertex.append(i)
        all_vertex.append(i)
    
    # исходный граф
    alg_input = Step(True, True)
    alg_input.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Всё верно, это граф по введённой матрице</p>' # можно будет удалить
    alg_input.nodes = all_vertex # список вершин
    alg_input.edges = edges # список ребер
    for i in all_vertex: # метки для вершин
        alg_input.node_options[i] = f'label: "x{i}"'
        alg_input.node_options[i] += f', shape: "circle"'
        alg_input.node_options[i] += f', "color": "#1E90FF"' # синий цвет

    # queue = []
    # finished = []

    # работа алгоритма
    while len(tracked_vertex) > 0:
        new_step = Step(True, True) # формирование шага
        new_step.edges = edges # график
        new_step.step_label = '' # графика
        forward_closure.clear()
        reverse_closure.clear()
        vertex_to_review = tracked_vertex[0] 

        new_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Рассмотрим вершину x<sub>{vertex_to_review}</sub>.</p>' # графика (добавление текста)

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
        new_step.text += line # графика (добавление текста)
        # reverse_closure line
        line = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Г<sup>-n</sup><sub>x<sub>{vertex_to_review}</sub></sub> = '
        
        reverse_line = vertex_list_to_str(reverse_closure)

        line += reverse_line
        line += '</p>'
        new_step.text += line # графика (добавление текста)

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
        new_step.text += line # графика (добавление текста)
        graph_class_arr.append(equivalence_class)

        print(forward_closure)
        print(reverse_closure)
        # готовим граф
        new_step.nodes = all_vertex # вершины графа
        for i in all_vertex: # подкрашивание вершин
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
        print(untracked_vertex)
        for i in untracked_vertex:
            new_step.node_options[i] += f', "color": "#BCBCBC"'
        print(unreachable_vertex)
        for i in unreachable_vertex:
            new_step.node_options[i] += f', "color": "#FF2400"'

        for element in graph_class_arr[len(graph_class_arr)-1]:
            tracked_vertex.remove(element)
        steps.append(new_step) # ДОБАВЛЕНИЕ ШАГА
    print(graph_class_arr)
    
    # ЗАВЕРШЕНИЕ АЛГОРИТМА
    new_step = Step(True, True)
    new_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Вершины закончились. Алгоритм завершён</p>'
    new_step.nodes = all_vertex
    new_step.edges = edges
    new_step.step_label = 'Завершение алгоритма'
    for i in all_vertex:
        new_step.node_options[i] = f'label: "x{i}"'
        new_step.node_options[i] += f', shape: "circle"'
        new_step.node_options[i] += f', "color": "#BCBCBC"'
    steps.append(new_step) # ДОБАВЛЕНИЕ ШАГА
    hue_step = 0.08 # шаг hue меняет цвет

    # ШАГ-РЕЗУЛЬТАТ
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
                result_step.node_options[i] += f', "color": "{hsv_to_hex(color_offset * hue_step, 1, 1)}"'
    alg_result.append(result_step)
    result_step = Step(True, True)
    result_step.text = '<p class="mb-2 text-gray-500 dark:text-gray-400">Граф компонент сильной связности:</p>'
    for i in graph_class_arr:
        result_step.nodes.append(i[0])
    
    result_step.edges = edges
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
    
    alg_input = Step(True, True)
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
        new_step.step_label = f"Разметка графа. Начало обхода в глубину от вершины x<sub>{vertex}</sub>"
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
            new_step.step_label = f"Разметка графа. Обход в глубину от вершины x<sub>{vertex}</sub>"
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
        new_step.step_label = f"Разметка графа. Конец обхода в глубину от вершины x<sub>{vertex}</sub>"
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
        
    
    print(marks)

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
    print(graph_class_arr)

    queue = []
    visited = []

    vertex_mark_list = []

    for i in range(size_of_matrix):
        vertex_mark_list.append((i, marks[i]))
    
    vertex_mark_list.sort(key = lambda x: (x[1], x[0]), reverse = True)
    print(vertex_mark_list)

    hue_step = 0.08 # шаг hue меняет цвет

    while len(vertex_mark_list) > 0:
        
        curr_vertex = vertex_mark_list.pop(0)[0]
        class_vertex = curr_vertex
        if curr_vertex in visited: continue

        new_step = Step(True, True)
        not_visited = addition(all_vertex, visited)
        visited.sort()
        not_visited.sort()
        new_step.step_label = f"Выделение компонентов сильной связности. Начало обхода в глубину от вершины x<sub>{curr_vertex}</sub>"
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
            print(curr_vertex)
            for i in range(size_of_matrix):
                if invert_matrix[curr_vertex][i] > 0 and not (i in visited):
                    queue.append(i)
                    added_to_class.append(i)

            new_step = Step(True, True)
            not_visited = addition(all_vertex, visited)
            visited.sort()
            not_visited.sort()
            new_step.step_label = f"Выделение компонентов сильной связности. Обход в глубину от вершины x<sub>{class_vertex}</sub>"
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
        new_step.step_label = f"Выделение компонентов сильной связности. Конец обхода в глубину от вершины x<sub>{class_vertex}</sub>"
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


    print(graph_class_arr)
    
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
    
    result_step.edges = edges
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