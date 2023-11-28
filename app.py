from flask import Flask, render_template, request, session
from datetime import timedelta
import Algorithms.Kirill as Kirill # импорт модуля Кирилла
import Algorithms.Kolya as Kolya # импорт модуля Кирилла

import time

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
    
    return render_template("main.html", title = 'Графы')

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
    steps = Kolya.kraskal(session.get("matrix"))
    print(f'Данные из сессии в другой функции: {session.get("matrix")}') # тестовая печать данных из сессии

    return render_template("Kolya/kraskal_result.html", title = 'Краскал', steps = steps)

# Алгоритм Прима
# страница с вводом матрицы смежности
@app.route("/prim")
def prim_input():
    return render_template("Kolya/prim.html", title = 'Прим')

# страница для вывода результата
@app.route('/prim/result')
def prim_result():
    time.sleep(2)
    steps = Kolya.prim(session.get("matrix"))

    return render_template("Kolya/prim_result.html", title = 'Прим', steps = steps)


if __name__ == '__main__':
    app.debug = True
    app.run()