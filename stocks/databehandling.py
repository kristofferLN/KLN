import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use('Qt5Agg')  # skifter backend til Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from io import BytesIO
import yfinance as yf
from .models import aktier, aktiepriser


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

def get_stocks_data():
    aktie_data_til_grafer = {}
    tickers = aktier.objects.values("ticker", "selskab")
    for tick in tickers:
        try:    
            aktie = yf.Ticker(tick["ticker"])
            hist = aktie.history(period="1y")
            if hist.empty:
                continue
            hist = hist[['Close']]  # Kun 'Close' priser
            hist.index = pd.to_datetime(hist.index)
            aktie_data_til_grafer[tick["selskab"]] = hist
        except Exception:
            continue
    #print(aktie_data_til_grafer)
    return aktie_data_til_grafer

##engangsbrug
def aktiepris_close_til_db():
    tickers = aktier.objects.values("ticker")
    for tick in tickers:
        try:    
            aktie = yf.Ticker(tick["ticker"])
            hist = aktie.history(period="1y")
            if hist.empty:
                continue
            hist = hist[['Close']]  # Kun 'Close' priser
            hist.index = pd.to_datetime(hist.index)
            for dato, row in hist.iterrows():
                pris_close = row['Close']
                aktiepris_entry = aktiepriser(selskab=aktier.objects.get(ticker=tick["ticker"]), dato=dato, pris_close=pris_close)
                aktiepris_entry.save()
        except Exception:
            continue

#ÆLSMDGS