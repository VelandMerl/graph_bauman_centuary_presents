from flask import Flask, render_template, request, session
from datetime import timedelta
import Algorithms.Kirill as Kirill # импорт модуля Кирилла
import Algorithms.Kolya as Kolya # импорт модуля Кирилла


class Step:
    text = "Default text for step"
    nodes = [] # вершины
    node_options = {} # доп опции вершин
    edges = {} # ребра. Формат: (from, to): weight
    edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
    general_options = 'width: 1200 + "px", height: 400 + "px"' # опции для всего холста



R = [(13, 1, 2), (18, 1, 3), (17, 1, 4), (14, 1, 5), (22, 1, 6),
     (26, 2, 3), (22, 2, 5), (3, 3, 4), (19, 4, 6)]

Rs = sorted(R, key=lambda x: x[0])
U = set()  # список соединенных вершин
D = {}      # словарь списка изолированных групп вершин
T = []      # список ребер остова
DI = {}     # словарь ребер
steps = [] 

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
        DI[r[1],r[2]] = r[0] 
        print(DI)   # создаем словарь ребер добавленных в остов

        A = Step()              # тут все по объяснениям Андрея
        message = '"Так как вершины {a1} и {a2} все еще не соединены и имеют наименьший вес ребра из не добавленных в остов, равный {a3}, соединяем их."'
        A.text = message.format(a1 = r[1], a2 = r[2], a3 = DI[r[1],r[2]])   # для добавления переменной в строку
        A.nodes = U1
        A.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
        A.edges = DI 
        A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
        steps.append(A)

for r in Rs:    # проходим по ребрам второй раз и объединяем разрозненные группы вершин
    if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
        T.append(r)             # добавляем ребро в остов
        gr1 = D[r[1]]
        D[r[1]] += D[r[2]]      # объединем списки двух групп вершин
        D[r[2]] += gr1

        DI[r[2],r[1]] = r[0]    # создаем словарь ребер добавленных в остов
        U1 = D[r[2]]
        print(DI)
        A = Step()              # тут все по объяснениям Андрея
        message = '"Так как вершины {a2} и {a1} все еще не соедиbbнены и имеют наименьший вес ребра из не добавленных в остов, равный {a3}, соединяем их."'
        A.text = message.format(a1 = r[2], a2 = r[1], a3 = DI[r[2],r[1]])   # для добавления переменной в строку
        A.nodes = U1
        A.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
        A.edges = DI 
        A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
        steps.append(A)


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'your_secret_key' # секретный ключ для подписы данных сессии

# alg_input = Step()
# alg_steps = []
# alg_last = Step()
# return [alg_input, alg_steps, alg_last]
@app.route('/')
def hello_world():
    
    # getdata()
    # input, steps, last = algorithm(session['matrix'])
    
    return render_template("main.html", title = 'Графы', steps = steps)

@app.route("/index")
def index():
    return render_template("index.html", title = 'Графы')

# универсальная функция для всех для сохранения матрицы в сессии
@app.route('/set_data_to_session', methods=['POST'])
def set_data_to_session():
    data = request.get_json() # получаем данные
    matrix = data.get('matrix')
    size = data.get('size')
    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    session['size'] = size # сохранение матрицы в словаре "Session"

    print(f'Размер: {size}', f'Матрица: {matrix}', sep="\n") # тестовый вывод

    return 'Данные успешно получены на сервере' # требуется возврат текстового значения

# Кирилл (алгоритм Демукрона)
# страница с вводом матрицы смежности
@app.route("/demukron")
def demukron_input():
    return render_template("Kirill/demukron.html", title = 'Демукрон')

# страница для вывода результата
@app.route('/demukron/result')
def demukron_result():

    print(f'Данные из сессии в другой функции: {session.get("matrix")}') # тестовая печать данных из сессии

    Kirill.demukron() # обращение к функции, реализующей алгоритм

    return render_template("Kirill/demukron_result.html", title = 'Демукрон')


# Коля
# Алгоритм Краскала
# страница с вводом матрицы смежности
@app.route("/kraskal")
def kraskal_input():
    return render_template("Kolya/kraskal.html", title = 'Краскал')

# страница для вывода результата
@app.route('/kraskal/result')
def kraskal_result():

    print(f'Данные из сессии в другой функции: {session.get("matrix")}') # тестовая печать данных из сессии

    Kolya.kraskal() # обращение к функции, реализующей алгоритм

    return render_template("Kolya/kraskal_result.html", title = 'Демукрон')

# Алгоритм Прима
# страница с вводом матрицы смежности
@app.route("/prim")
def prim_input():
    return render_template("Kolya/prim.html", title = 'Демукрон')

# страница для вывода результата
@app.route('/prim/result')
def prim_result():

    print(f'Данные из сессии в другой функции: {session.get("matrix")}') # тестовая печать данных из сессии

    Kolya.prim() # обращение к функции, реализующей алгоритм

    return render_template("Kolya/prim_result.html", title = 'Демукрон')


if __name__ == '__main__':
    app.debug = True
    app.run()