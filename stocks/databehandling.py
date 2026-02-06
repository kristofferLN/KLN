import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use('Qt5Agg')  # skifter backend til Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from io import BytesIO
import yfinance as yf


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')    
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,2))
    plt.plot(x,y)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    #plt.title('Sample Plot')
    #plt.xlabel('X-axis')
    #plt.ylabel('Y-axis')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_novo_nordisk_data():
    data = {}
    novo = yf.Ticker("NOVO-B.CO")
    hist = novo.history(period="1y")  # Hent historiske data for den sidste måned
    hist = hist[['Close']]  # Kun 'Close' priser
    hist.index = pd.to_datetime(hist.index)
    return hist


