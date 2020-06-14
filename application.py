from flask import Flask

app = Flask(__name__)
@app.route("/")
def index():
    return 'Hello'

@app.route("/port")
def port():
    return "The script is running on [port]"

@app.route("/fibonacci")
def fibonacci():
    a = 0
    b = 1
    res = str(a) + ', ' + str(b)
    for i in range(2,100):
        c = a + b
        a = b
        b = c
        res = res + ', ' + str(c) 
    return res
