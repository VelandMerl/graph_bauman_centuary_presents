from flask import Flask, render_template, request, session
import Algorithms.Strong_Connectivity as sc # импорт модуля Андрея
import Algorithms.Topological_Sort as ts # импорт модуля Кирилла
import Algorithms.Minimal_spanning_tree as st # импорт модуля Коли


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'your_secret_key' # секретный ключ для подписы данных сессии

# начальная страница
@app.route('/')
def home():
    return render_template("index.html", title = 'Графы')

# страница выбора решаемой задачи
@app.route("/index")
def index():
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

# алгоритмы Андрей
@app.route("/strong_connectivity")
def strong_connectivity_input():
    return render_template("strong_connectivity.html", title = 'Разбиение графа')

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
    return render_template("topological_sort.html", title = 'Топологическая сортировка')

@app.route('/topological_sort/depth_first_search')
def depth_first_search():
    # matrix = [ [0, 1, 0, 1, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 1, 0, 0, 1], [0, 0, 1, 0, 0] ]
    alg_input, steps, alg_result = ts.algorithm_depth_first_search(session['matrix'])
    return render_template("main.html", title = 'Поиск в глубину', alg_input = alg_input, steps = steps, alg_result = alg_result)

# алгоритмы Коли
@app.route("/minimal_spanning_tree")
def minimal_spanning_tree():
    return render_template("minimal_spanning_tree.html", title = 'Минимальный остов')

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