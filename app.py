import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import pacf 
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima.model import ARIMA
from flask import Flask, render_template, request
app = Flask(__name__)
data=pd.read_csv("C:\\Users\\saira\\OneDrive\\Desktop\\ipbl\\nifty\\niftydata20yrs.csv")
 
def forecast_data(numsteps):
    d = 0
    forecast_list = []
    
    max_pacf_lag = 0
    for column in data.columns[1:]:
      
        series = data[column]
        
       
        pacf_values = pacf(series, nlags=6)
        
      
        max_pacf_index = (np.abs(pacf_values[1:]) > 0.05).argmax() + 1
        if max_pacf_index > max_pacf_lag:
            max_pacf_lag = max_pacf_index
    
    
    p = max_pacf_lag
    
    
    max_acf_lag = 0
    for column in data.columns[1:]:
        acf_values = acf(data[column], nlags=12)
        max_acf_index = (np.abs(acf_values[1:]) > 0.05).argmax() + 1
        if max_acf_index > max_acf_lag:
            max_acf_lag = max_acf_index
    
    q = max_acf_lag
    
    for column in data.columns[1:]:
        series = data[column]
        model = ARIMA(series, order=(p, d, q))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=numsteps)
        forecast_list.append(list(forecast))
        
    return forecast_list

    
@app.route('/')
def home():
	return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        numsteps = int(request.form['year'])
        forecast = forecast_data(numsteps)
        print(forecast)
        return render_template('res1.html', forecast=forecast, numsteps=numsteps)
        
if __name__ == '__main__':
    app.run()
