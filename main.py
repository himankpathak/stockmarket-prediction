
def search(stockName):
    try:
        Image = open('static/stocks/'+stockName+'/'+stockName+'1.png', 'r')
        # Store configuration file values
        print("cache found")
        return 1

    except FileNotFoundError:
        # Keep preset values
        print("file not found")
        return 0
