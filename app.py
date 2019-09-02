from flask import Flask, render_template, request
from main import search, stockpredict

app = Flask(__name__)
app.debug = True

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
        return predictStock(stockName)

def displayStock(stockName):
    stockData = []
    with open('static/stocks/'+stockName+'/'+stockName+'.txt', 'r') as filehandle:
        for line in filehandle:
            currentPlace = line[:-1]
            stockData.append(currentPlace)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)

def predictStock(stockName):
    stockData=stockpredict(stockName)
    return render_template("stockdetail.html", stockName = stockName, stockData=stockData)


if __name__ == "__main__":
    app.run()
