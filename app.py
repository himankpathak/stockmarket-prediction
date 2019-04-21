from flask import Flask, render_template, request
from main import search


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/', methods=['POST'])
def requestStock():
    text = request.form['sname']
    stockName = text.upper()
    print(stockName)
    if(search(stockName)):
        return displayStock(stockName)
    else:
        pass

@app.route("/stockdetail")
def displayStock(stockName):
    return render_template("stockdetail.html", stockName = stockName)

if __name__ == "__main__":
    app.run(debug=True)
