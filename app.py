from flask import Flask, render_template, request, session, jsonify
import Algorithms.Strong_Connectivity as sc # импорт модуля Андрея
import Algorithms.Topological_Sort as ts # импорт модуля Кирилла
import Algorithms.Minimal_spanning_tree as st # импорт модуля Коли
import Algorithms.Shortest_Path as sp # импорт модуля Маши
import ast

from flask_sqlalchemy import SQLAlchemy ## имплементация бд


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'your_secret_key' # секретный ключ для подписы данных сессии

## имплементация бд
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Bauman:Baumanpassword@localhost/GraphDB'
db = SQLAlchemy(app)

class Problem_class(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pr_cl = db.Column(db.Text, nullable=False)
    dsc = db.Column(db.Text)

    def __repr__(self):
        return f"Problem class: {self.pr_cl}"

class Algorithm (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    alg = db.Column(db.Text, nullable=False)
    dsc = db.Column(db.Text)
    key = db.Column(db.Text, nullable=False)
    
    pr_cl_id = db.Column(db.Integer, db.ForeignKey('problem_class.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f"Algorithm: {self.alg}"
    
class Example (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ex = db.Column(db.Text, nullable=False)
    dsc = db.Column(db.Text)

    alg_id = db.Column(db.Integer, db.ForeignKey('algorithm.id', ondelete='CASCADE'), nullable=False)
    
    def __repr__(self):
        return f"Example: {self.ex}"
## имплементация бд

# начальная страница
@app.route('/')
def home():
    return render_template("index.html", show_alg_btn = [], title = 'Графы')

# универсальная функция для сохранения матрицы в сессии
@app.route('/set_data_to_session', methods=['POST'])
def set_data_to_session():
    data = request.get_json() # получаем данные
    matrix = data.get('matrix')
    size = data.get('size')
    pathFlag = data.get('pathFlag')

    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    session['size'] = size # сохранение матрицы в словаре "Session"

    print(f'Размер: {size}', f'Матрица: {matrix}', sep="\n") # тестовый вывод

    if pathFlag:
        session['start_ver'] = data.get('start_ver') # сохранение нач. вершины в словаре "Session"
        session['finish_ver'] = data.get('finish_ver') # сохранение кон. вершины в словаре "Session"
        session['orgraph'] = data.get('orgraph') # сохранение вида графа
        print(f'Начало: {session["start_ver"]}', f'Конец: {session["finish_ver"]}', f'Тип графа: {session["orgraph"]}', sep="\n") # тестовый вывод


    return 'Данные успешно получены на сервере' # требуется возврат текстового значения

# получение данных из БД
@app.route('/set_dbdata', methods=['POST'])
def set_dbdata():
    data = request.get_json() # получаем данные
    alg_code = data.get('alg_code') # получаем переданную строку
    # запрос для получения матрицы
    algos = Algorithm.query.filter_by(key = alg_code).first()
    matrix = Example.query.filter_by(alg_id = algos.id).first().ex # получение матрицы
    print(matrix)
    matrix = ast.literal_eval(matrix)
    print(matrix)
    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    print(session['matrix'])

    try:
        # получение направления
        dsc = Example.query.filter_by(alg_id = algos.id).first().dsc 
        dsc = ast.literal_eval(dsc)
        session['start_ver'] = dsc[0] # сохранение нач. вершины в словаре "Session"
        session['finish_ver'] = dsc[1] # сохранение кон. вершины в словаре "Session"
        session['orgraph'] = dsc[2] # сохранение вида графа
        print(session['start_ver'],  session['finish_ver'], session['orgraph'])
    except ValueError:
        print('Этих данных нет в БД')

    return jsonify({'dbData': alg_code})

# алгоритмы Даны
@app.route("/sorting_array")
def sorting_array():
    
    return render_template("binary_tree/sorting_array.html", title = 'Сортировка массива')

@app.route("/traversal")
def traversal():
    
    return render_template("binary_tree/traversal.html", title = 'Обходы')


# алгоритмы Маши
@app.route("/shortest_path")
def shortest_path():
    return render_template("shortest_path.html", show_alg_btn = [], title = 'Кратчайший путь', ds_desc = Algorithm.query.filter_by(key = 'ds').first(), bf_desc = Algorithm.query.filter_by(key = 'bf').first(), fl_desc = Algorithm.query.filter_by(key = 'fl').first())

@app.route('/shortest_path/dijkstra')
def dijkstra():

    alg_input, steps, alg_result = sp.algorithm_Dijkstra(session['matrix'], session["start_ver"], session["finish_ver"], session['orgraph'])
    return render_template("main.html", show_alg_btn = ["ds", "bf", "fl"], title = 'Дейкстра', alg_title = "Алгоритм Дейкстры", alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/shortest_path/bellman–ford')
def bellman_ford():

    alg_input, steps, alg_result = sp.algorithm_Bellman_Ford(session['matrix'], session["start_ver"], session["finish_ver"], session['orgraph'])
    return render_template("main.html", show_alg_btn = ["ds", "bf", "fl"], title = 'Беллман-Форд', alg_title = "Алгоритм Беллмана-Форда", alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/shortest_path/floyd_warshall')
def floyd_warshall():

    alg_input, steps, alg_result = sp.algorithm_Floyd_Warshall(session['matrix'], session["start_ver"], session["finish_ver"], session['orgraph']) 
    return render_template("main.html", show_alg_btn = ["ds", "bf", "fl"], title = 'Флойд-Уоршелл', alg_title = "Алгоритм Флойда-Уоршелла", alg_input = alg_input, steps = steps, alg_result = alg_result)


# алгоритмы Андрей
@app.route("/strong_connectivity")
def strong_connectivity_input():
    return render_template("strong_connectivity.html", show_alg_btn = [], title = 'Разбиение графа', ml_desc = Algorithm.query.filter_by(key = 'ml').first(), ks_desc = Algorithm.query.filter_by(key = 'ks').first())

@app.route('/strong_connectivity/malgrange')
def Malgrange():
    # matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = sc.algorithm_Malgrange(session['matrix'])
    return render_template("main.html", show_alg_btn = ["ml", "ks"], title = 'Мальгранж', alg_title = "Алгоритм Мальгранжа", alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/strong_connectivity/kosaraju')
def Kosaraju():
    # matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = sc.algorithm_Kosaraju(session['matrix'])
    return render_template("main.html", show_alg_btn = ["ml", "ks"], title = 'Косарайю', alg_title = "Алгоритм Косарайю", alg_input = alg_input, steps = steps, alg_result = alg_result)

# алгоритмы Кирилла
@app.route("/topological_sort")
def topological_sort_input():
    return render_template("topological_sort.html", show_alg_btn = [], title = 'Топологическая сортировка', dm_desc = Algorithm.query.filter_by(key = 'dm').first(), dfs_desc = Algorithm.query.filter_by(key = 'dfs').first())

@app.route('/topological_sort/depth_first_search')
def depth_first_search():
    # matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = ts.algorithm_depth_first_search(session['matrix'])
    return render_template("main.html", show_alg_btn = ["dm", "dfs"], title = 'Поиск в глубину', alg_title = "Поиск в глубину", alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/topological_sort/demukron')
def demukron():
    matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]

    alg_input, steps, alg_result = ts.demukron(session['matrix'])
    # alg_input, steps, alg_result = ts.demukron(matrix)
    return render_template("main.html", show_alg_btn = ["dm", "dfs"], title = 'Демукрон', alg_title = "Алгоритм Демукрона", alg_input = alg_input, steps = steps, alg_result = alg_result)

# алгоритмы Коли
@app.route("/minimal_spanning_tree")
def minimal_spanning_tree():
    return render_template("minimal_spanning_tree.html", show_alg_btn = [], title = 'Минимальный остов', kr_desc = Algorithm.query.filter_by(key = 'kr').first(), pr_desc = Algorithm.query.filter_by(key = 'pr').first())

@app.route('/minimal_spanning_tree/kraskal')
def kraskal():
    alg_input, steps, alg_result = st.kraskal(session['matrix'])
    return render_template("main.html", show_alg_btn = ["kr", "pr"], title = 'Краскал', alg_title = "Алгоритм Краскала", alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/minimal_spanning_tree/prim')
def prim():
    alg_input, steps, alg_result = st.prim(session['matrix'])
    return render_template("main.html", show_alg_btn = ["kr", "pr"], title = 'Прим', alg_title = "Алгоритм Прима", alg_input = alg_input, steps = steps, alg_result = alg_result)


if __name__ == '__main__':
    # app.debug = True
    app.run(host="0.0.0.0")