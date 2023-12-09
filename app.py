from flask import Flask, render_template, request, session
from datetime import timedelta
import Algorithms.Kirill as Kirill # импорт модуля Кирилла
import Algorithms.Kolya as Kolya # импорт модуля Кирилла
import Algorithms.Strong_Connectivity as sc # импорт модуля Кирилла

import time


from Algorithms.Usefull_elements import Step
test_steps = []



A = Step()
A.text = "\"Something for step 1\""
A.nodes = [1, 2, 3] 
A.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 } 
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
test_steps.append(A)

A = Step()
A.text = "Something to step 2"
A.nodes = ["1", "2", "3"]
A.node_options =  { "1": 'label: \"node 1\", \"color\": \"#97c2fc\"', "2": 'label: \"node 2\", \"color\": \"#97c2fc\"', "3": '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
test_steps.append(A)

A = Step()
A.text = "Something at step 3"
A.nodes = [1, 2, 3]
A.node_options =  { 1: 'label: \"MT\", \"color\": \"#97c2fc\"', 2: 'label: \"AT\", \"color\": \"#97c2fc\"', 3: '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
test_steps.append(A)

A = Step()
A.text = "Something at step 4"
A.nodes = [1, 2, 3]
A.node_options =  { 1: 'label: \"MT\", \"color\": \"#97c2fc\"', 2: 'label: \"AT\", \"color\": \"#97c2fc\"', 3: '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
test_steps.append(A)

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
    matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    # alg_input, steps = sc.algorithm_Malgrange(matrix)
    alg_input, steps, alg_result = sc.algorithm_Kosaraju(matrix)
    return render_template("main.html", title = 'Мальгранж', alg_input = alg_input, steps = steps, alg_result = alg_result)
    # return render_template("main.html", title = 'Графы')

@app.route('/Malgrange')
def Malgrange():
    
    # getdata()
    # input, steps, last = algorithm(session['matrix'])
    matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = sc.algorithm_Malgrange(matrix)
    # alg_input, steps, alg_result = sc.algorithm_Kosaraju(matrix)
    return render_template("main.html", title = 'Мальгранж', alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/Kosaraju')
def Kosaraju():
    
    # getdata()
    # input, steps, last = algorithm(session['matrix'])
    matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    # alg_input, steps = sc.algorithm_Malgrange(matrix)
    alg_input, steps, alg_result = sc.algorithm_Kosaraju(matrix)
    return render_template("main.html", title = 'Косарайю', alg_input = alg_input, steps = steps, alg_result = alg_result)

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
    time.sleep(2)
    alg_input, steps, alg_result = Kolya.kraskal(session.get("matrix"))
    return render_template("main.html", title = 'Краскал', alg_input = alg_input, steps = steps, alg_result = alg_result)

# Алгоритм Прима
# страница с вводом матрицы смежности
@app.route("/prim")
def prim_input():
    return render_template("Kolya/prim.html", title = 'Прим')

# страница для вывода результата
@app.route('/prim/result')
def prim_result():
    time.sleep(2)
    alg_input, steps, alg_result = Kolya.prim(session.get("matrix"))

    return render_template("main.html", title = 'Прим', alg_input = alg_input, steps = steps, alg_result = alg_result)


if __name__ == '__main__':
    app.debug = True
    app.run()