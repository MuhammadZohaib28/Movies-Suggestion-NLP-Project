from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/suggestion')
def suggestion():
    return render_template("suggestion.html")


if __name__ == '__main__':
    app.debug = True
    app.run()