import pandas as pd
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
from io import BytesIO
from statsmodels.tsa.seasonal import seasonal_decompose

data = pd.read_csv("C:\\Users\\saira\\OneDrive\\Desktop\\ipbl\\nifty\\niftydata20yrs.csv")
data.set_index('Year', inplace=True)

def generate_plot(year):
    if year in data.index:
        yearly_data = data.loc[year, :'Dec'] 
        decomposition = seasonal_decompose(yearly_data, model='additive', extrapolate_trend='freq', period=6)

        
        fig, axes = plt.subplots(3, 1, figsize=(10, 8))
        axes[0].plot(yearly_data.index, yearly_data.values, label='Original', marker='o', linestyle='-')
        axes[0].legend(loc='upper left')
        axes[1].plot(yearly_data.index, decomposition.trend, label='Trend', marker='o', linestyle='-')
        axes[1].legend(loc='upper left')
        axes[2].plot(yearly_data.index, decomposition.seasonal, label='Seasonal', marker='o', linestyle='-')
        axes[2].legend(loc='upper left')
        plt.suptitle(f'Time Series analysis for {year}')
        plt.tight_layout()

        img_buffer = BytesIO()
        FigureCanvas(fig).print_png(img_buffer)

       
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig) 

        return img_str
    else:
        return None


app = Flask(__name__)

# Route for home page
@app.route('/')
def home():
    return render_template('main2.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        year = int(request.form['year'])
        print(f"Received POST request for year: {year}")
        plot_data = generate_plot(year)
        if plot_data:
            print("Plot data generated successfully.")
            return jsonify({'plot_data': plot_data})
        else:
            print(f"Data for the year {year} does not exist.")
            return jsonify({'error': f'Data for the year {year} does not exist.'})

if __name__ == '__main__':
    app.run(debug=True)
