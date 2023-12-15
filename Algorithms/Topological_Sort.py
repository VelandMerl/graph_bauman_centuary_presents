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
    print(f'Вершины: {all_vertex}')

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
        
        print(f'Пары смежных вершин: {neighbor_ver}')

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

# топологическая соритровка, алгоритм Демукрона

# диалог с пользователем
def demukron(matrix):
    vertex_level = dict() # объявление пустого словаря (соотв. вершин уровням)
    vertex = set() # объявление пустого множества (вершины без уровня)
    all_vertex = [] # список вершин
    edges = [] # список рёбер
    steps = [] # список шагов
    alg_result = [] # шаг-результат

    # реализация алгоритма
    def dm(vertex):
        # формирование уровня
        print(f'матрица {matrix}')
        print(f'вершины {vertex}')
        level = 0
        while vertex:
            flag = False # уровень отсутствует
            level_v = set()  # вершины формируемого уровня
            for i in vertex: # просмотр столбца матрицы
                sum = 0
                # просмотр входящих вершин
                for j in range(len(matrix)):
                    sum += matrix[j][i]
                if sum == 0:
                    level_v.add(i) # добавление вершины в уровень
                    vertex_level[i] = level # обновление уровня вершины
                    flag = True # уровень найден
            if flag:
                print(f'Вершины {level} уровня: ', set(map(lambda el: el, level_v)))
            else:
                return False # уровень не сформирован
            for i in level_v:
                matrix[i] = list(map(lambda el: 0, matrix[i]))  # удаление(зануление) строки
            print(f'матрица {matrix}')
            vertex -= level_v # исключение вершин с определённым уровнем
            level += 1
        return True

    # инициализация
    for i in range(len(matrix)):
        # словарь соответствия исходных вершин уровням
        vertex_level.update({i: None})
        # формирование множеста вершин без уровня
        vertex.add(i)
    edges = get_edges(matrix) # список рёбер
    all_vertex = vertex.copy() # список вершин

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

    res = dm(vertex) # запуск алгоритма
    if res:
        print('Алгоритм успешно завершен')  
        print(f'Вершины по уровням: {vertex_level}')
    else:
        print('Выполнение алгоритма прервано из-за наличия контура')
    
    result_step = copy.deepcopy(alg_input)
    result_step.text = f'<p class="mb-2 text-gray-500 dark:text-gray-400">Разделение вершин по уровням - {vertex_level})</p>'
    result_step.text += '<p class="mb-2 text-gray-500 dark:text-gray-400">Это граф, разбитый на уровни</p>' # текст шага
    for ver, level in vertex_level.items(): # установка уровней для вершин
        result_step.node_options[ver] = f'label: "x{ver}"'
        result_step.node_options[ver] += ', shape: "circle"'
        result_step.node_options[ver] += ', "color": "#1E90FF"'
        result_step.node_options[ver] += f', level: {level}'
    
    neighbor_ver = [] # пары вершин соседних уровней
    sorted_levels = sorted(set(vertex_level.values()))  # Получение уникальных значений уровней и их сортировка
    for level in sorted_levels[:-1]:  # Проход по уровням, исключая последний
        current_level_vertices = [vertex for vertex, vertex_level in vertex_level.items() if vertex_level == level]  # Вершины текущего уровня
        next_level_vertices = [vertex for vertex, vertex_level in vertex_level.items() if vertex_level == level + 1]  # Вершины следующего уровня
        neighbor_pairs = [(v1, v2) for v1 in current_level_vertices for v2 in next_level_vertices]  # Пары соседних вершин
        neighbor_ver.extend(neighbor_pairs)  # Добавление пар в список

    result_step.general_options += ', layout: { hierarchical: { direction: "LR", levelSeparation: 100, nodeSpacing: 150} }'


    print(edges)
    print(neighbor_ver)
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
    steps.append(alg_input)

    return [ alg_input, steps, alg_result ]  