import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify
import io
import base64

data = pd.read_csv("C:\\Users\\saira\\OneDrive\\Desktop\\ipbl\\nifty\\niftydata20yrs.csv")

def plot_data(column):
    plt.figure(figsize=(12, 10))
    plt.bar(data['Year'], data[column], color='skyblue', edgecolor='black', width=0.8)  
    plt.title(f"Histogram of {column} returns", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Returns", fontsize=14)
    plt.xticks(range(2000, 2024), rotation=45, ha='right', fontsize=12)
    plt.xlim(1999.5, 2023.5)
    bar_img = get_img_base64()
    plt.close()

    plt.figure(figsize=(12, 10))
    plt.plot(data['Year'], data[column], color='skyblue', marker='o', linewidth=3) 
    plt.title(f"Histogram plot curve of {column} returns", fontsize=16)
    plt.xlabel("Years", fontsize=14)
    plt.ylabel("Returns", fontsize=14)
    plt.xticks(range(2000, 2024), rotation=45, ha='right', fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlim(1999.5, 2023.5)
    line_img = get_img_base64()
    plt.close()

    monthly_returns = data[column]
    
    mean_return = np.mean(monthly_returns)
    std_deviation = np.std(monthly_returns)
    
    min_return = min(monthly_returns)
    max_return = max(monthly_returns)
    bin_edges = np.linspace(min_return, max_return, num=24)

    plt.figure(figsize=(12, 8))
    hist, bins, _ = plt.hist(monthly_returns, bins=bin_edges, edgecolor='black')
    plt.title(f'Histogram of {column} Returns')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.axvline(mean_return, color='r', linestyle='dashed', linewidth=1, label='Mean')
    plt.axvline(mean_return - std_deviation, color='g', linestyle='dashed', linewidth=1, label='-1 Std Dev')
    plt.axvline(mean_return + std_deviation, color='g', linestyle='dashed', linewidth=1, label='+1 Std Dev')
    plt.axvline(mean_return - 2 * std_deviation, color='b', linestyle='dashed', linewidth=1, label='-2 Std Dev')
    plt.axvline(mean_return + 2 * std_deviation, color='b', linestyle='dashed', linewidth=1, label='+2 Std Dev')
    plt.legend()
    plt.yticks(np.arange(0, max(hist) + 1, step=1))
    hist_img = get_img_base64()
    plt.close()

    return bar_img, line_img, hist_img

def get_img_base64():
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode('utf8')
    return 'data:image/png;base64,' + img_b64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main3.html')

@app.route('/plot', methods=['POST'])
def plot():
    column = request.form['column']
    bar_img, line_img, hist_img = plot_data(column)
    return jsonify(bar_plot=bar_img, line_plot=line_img, hist_plot=hist_img)

if __name__ == '__main__':
    app.run(debug=True)
