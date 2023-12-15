from flask import Flask, render_template, request, session, jsonify
import Algorithms.Strong_Connectivity as sc # импорт модуля Андрея
import Algorithms.Topological_Sort as ts # импорт модуля Кирилла
import Algorithms.Minimal_spanning_tree as st # импорт модуля Коли

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
    return render_template("index.html", title = 'Графы')

# универсальная функция для сохранения матрицы в сессии
@app.route('/set_data_to_session', methods=['POST'])
def set_data_to_session():
    data = request.get_json() # получаем данные
    matrix = data.get('matrix')
    size = data.get('size')
    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    session['size'] = size # сохранение матрицы в словаре "Session"

    print(f'Размер: {size}', f'Матрица: {matrix}', sep="\n") # тестовый вывод

    return 'Данные успешно получены на сервере' # требуется возврат текстового значения

# получение данных из БД
@app.route('/set_dbdata', methods=['POST'])
def set_dbdata():
    data = request.get_json() # получаем данные
    info = data.get('dbData')
    print(info)
    matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]
    session['matrix'] = matrix # сохранение матрицы в словаре "Session"
    print(session['matrix'])

    return jsonify({'dbData': info})

# session['db_alg'] = Algorithm.query.filter_by(key = alg_code).first().dsc # сохранение экземпляра сущности Алгоритм в словаре "Session"
# session['db_class'] = Problem_class.query.filter_by(id = Algorithm.query.filter_by(key = alg_code).first().pr_cl_id).first().dsc # сохранение экземпляра сущности Алгоритм в словаре "Session"
    
# print(f'Класс алгоритма: {alg_code}', f'БД: {session["db_class"]}', sep="\n") # тестовый вывод
# print(f'Код алгоритма: {alg_code}', f'БД: {session["db_alg"]}', sep="\n") # тестовый вывод


# алгоритмы Андрей
@app.route("/strong_connectivity")
def strong_connectivity_input():
    return render_template("strong_connectivity.html", title = 'Разбиение графа', ml_desc = Algorithm.query.filter_by(key = 'ml').first(), ks_desc = Algorithm.query.filter_by(key = 'ks').first())

@app.route('/strong_connectivity/malgrange')
def Malgrange():
    # matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = sc.algorithm_Malgrange(session['matrix'])
    return render_template("main.html", title = 'Мальгранж', alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/strong_connectivity/kosaraju')
def Kosaraju():
    # matrix = [ [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [1, 1, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = sc.algorithm_Kosaraju(session['matrix'])
    return render_template("main.html", title = 'Косарайю', alg_input = alg_input, steps = steps, alg_result = alg_result)

# алгоритмы Кирилла
@app.route("/topological_sort")
def topological_sort_input():
    return render_template("topological_sort.html", title = 'Топологическая сортировка', dm_desc = Algorithm.query.filter_by(key = 'dm').first(), dfs_desc = Algorithm.query.filter_by(key = 'dfs').first())

@app.route('/topological_sort/depth_first_search')
def depth_first_search():
    # matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = ts.algorithm_depth_first_search(session['matrix'])
    return render_template("main.html", title = 'Поиск в глубину', alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/topological_sort/demukron')
def demukron():
    matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]

    alg_input, steps, alg_result = ts.demukron(session['matrix'])
    # alg_input, steps, alg_result = ts.demukron(matrix)
    return render_template("main.html", title = 'Поиск в глубину', alg_input = alg_input, steps = steps, alg_result = alg_result)

# алгоритмы Коли
@app.route("/minimal_spanning_tree")
def minimal_spanning_tree():
    return render_template("minimal_spanning_tree.html", title = 'Минимальный остов', kr_desc = Algorithm.query.filter_by(key = 'kr').first(), pr_desc = Algorithm.query.filter_by(key = 'pr').first())

@app.route('/minimal_spanning_tree/kraskal')
def kraskal():
    alg_input, steps, alg_result = st.kraskal(session['matrix'])
    return render_template("main.html", title = 'Краскал', alg_input = alg_input, steps = steps, alg_result = alg_result)

@app.route('/minimal_spanning_tree/prim')
def prim():
    alg_input, steps, alg_result = st.prim(session['matrix'])
    return render_template("main.html", title = 'Прим', alg_input = alg_input, steps = steps, alg_result = alg_result)


if __name__ == '__main__':
    # app.debug = True
    app.run(host="0.0.0.0")