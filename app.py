from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def hello_world():
    return render_template("mainpage.html", title = 'Графы')

@app.route("/index")
def index():
    return render_template("index.html", title = 'Графы')

# обработка размера матрицы
@app.route('/process/size', methods=['POST']) 
def process_size():
    size = request.get_data(as_text=True) # получение данных
    print('Размер матрицы:', size) # вывод полученных данных
    return 'Данные успешно получены на сервере' # требуется возврат текстового значения

# обработка матрицы
@app.route('/process/matrix', methods=['POST']) 
def process_matrix():
    matrix = request.get_data(as_text=True)  # получаем матрицу из запроса
    print(matrix)
    return 'Данные успешно получены на сервере' # требуется возврат текстового значения

if __name__ == '__main__':
    app.debug = True
    app.run()