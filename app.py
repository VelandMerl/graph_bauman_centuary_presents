from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def hello_world():
    return render_template("mainpage.html", title = 'Графы')
@app.route("/index")
def index():
	return render_template("index.html", title = 'Графы')
if __name__ == '__main__':
    app.debug = True
    app.run()