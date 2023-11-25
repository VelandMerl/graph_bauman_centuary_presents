from flask import Flask, render_template, request


class Step:
    text = "Default text for step"
    nodes = [] # вершины
    node_options = {} # доп опции вершин
    edges = {} # ребра. Формат: (from, to): weight
    edge_options = {} # Опции рёбер. Формат (from, to): options(как строка)
    general_options = 'width: 1200 + "px", height: 400 + "px",  edges: { arrows: { to: {enabled: true}} , smooth: { enabled: true} },' # опции для всего холста

steps = []
A = Step()
A.text = "\"Something for step 1\""
A.nodes = [1, 2, 3] 
A.node_options =  { 1: 'label: "1", "color": "#FFFFFF"', 2: 'label: \"2\", \"color\": \"#97c2fc\"', 3: '' } 
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 } 
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' } 
steps.append(A)

A = Step()
A.text = "Something to step 2"
A.nodes = ["1", "2", "3"]
A.node_options =  { "1": 'label: \"node 1\", \"color\": \"#97c2fc\"', "2": 'label: \"node 2\", \"color\": \"#97c2fc\"', "3": '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
steps.append(A)

A = Step()
A.text = "Something at step 3"
A.nodes = [1, 2, 3]
A.node_options =  { 1: 'label: \"MT\", \"color\": \"#97c2fc\"', 2: 'label: \"AT\", \"color\": \"#97c2fc\"', 3: '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
steps.append(A)

A = Step()
A.text = "Something at step 4"
A.nodes = [1, 2, 3]
A.node_options =  { 1: 'label: \"MT\", \"color\": \"#97c2fc\"', 2: 'label: \"AT\", \"color\": \"#97c2fc\"', 3: '' }
A.edges = { (1, 2): 4, (2, 3): 5, (3, 1): 10 }
A.edge_options = { (1, 2): '\"width\": 2', (2, 3): '' }
steps.append(A)

app = Flask(__name__)
app.config.from_object('config')

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

# в работе (не трогать)
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