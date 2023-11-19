from flask import Flask, render_template, request

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def hello_world():
    return render_template("mainpage.html", title = 'Графы')

@app.route("/index")
def index():
    return render_template("index.html", title = 'Графы')

@app.route('/process', methods=['POST'])
def process_data():
    size = request.get_data(as_text=True) # получение данных
    print('Размер матрицы:', size) # вывод полученных данных
    return 'Данные успешно получены на сервере' # требуется вовзрат текстового значения

if __name__ == '__main__':
    app.debug = True
    app.run()