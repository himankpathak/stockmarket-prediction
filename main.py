import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dropout, Dense
import matplotlib.pyplot as plt

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

#Function to process the data into 7 day look back slices
def processData(data,lb):
    X,Y = [],[]
    for i in range(len(data)-lb-1):
        X.append(data[i:(i+lb),0])
        Y.append(data[(i+lb),0])
    return np.array(X),np.array(Y)

# Main Stock Prediction Function
def stockpredict(stockName):
    data = pd.read_csv('dataset/all_stocks_5yr.csv')
    cl = data[data['Name']==stockName].Close
    path = os.getcwd()
    os.mkdir(path+"/static/stocks/"+stockName)

    # Scaling using MinMaxScaler
    scl = MinMaxScaler()
    cl = cl.values.reshape(cl.shape[0],1)
    cl = scl.fit_transform(cl)

    X,Y = processData(cl,7)
    X_train,X_test = X[:int(X.shape[0]*0.80)],X[int(X.shape[0]*0.80):]
    Y_train,Y_test = Y[:int(Y.shape[0]*0.80)],Y[int(Y.shape[0]*0.80):]

    # building the RNN LSTM model
    model = Sequential()
    model.add(LSTM(32,input_shape=(7,1)))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.compile(optimizer='adam',loss='mse')
    #Reshape data for (Sample,Timestep,Features)
    X_train = X_train.reshape((X_train.shape[0],X_train.shape[1],1))
    X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))

    hist = model.fit(X_train,Y_train,epochs=50,validation_data=(X_test,Y_test),shuffle=False)

    plt.plot(hist.history['loss'])
    plt.plot(hist.history['val_loss'])
    plt.legend(['Loss', 'Validation Loss'], loc='upper right')
    plt.savefig('static/stocks/'+stockName+'/'+stockName+'2.png')
    plt.clf()
    plt.close()

    i=249
    Xt = model.predict(X_test[i].reshape(1,7,1))
    pprice=scl.inverse_transform(Xt).copy()
    pprice=round(float(pprice.tolist()[0][0]),2)

    Xt = model.predict(X_test)
    rval = scl.inverse_transform(Y_test.reshape(-1,1))
    pval = scl.inverse_transform(Xt)
    ploss=0
    for i in range(len(rval)):
        ploss += abs((rval[i] - pval[i])/rval[i])*100
    ploss = round(float(ploss / len(rval)), 2)
    acr = 100-ploss

    plt.plot(rval)
    plt.plot(pval)
    plt.ylabel('Price')
    plt.xlabel('Days')
    plt.legend(['Real', 'Prediction'], loc='upper left')
    plt.savefig('static/stocks/'+stockName+'/'+stockName+'1.png')
    plt.clf()
    plt.close()

    filepathtosave = path+"/static/stocks/"+stockName+"/"+stockName+".txt"
    tostore = [str(pprice),str(acr)]
    with open(filepathtosave, 'w') as filehandle:
        for listitem in tostore:
            filehandle.write('%s\n' % listitem)

    return tostore
