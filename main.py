
def search(stockName):
    try:
        Image = open('static/stocks/'+stockName+'/'+stockName+'.png', 'r')
        # Store configuration file values
        print("file found")
        return 1

    except FileNotFoundError:
        # Keep preset values
        print("file not found")
        return 0
