import os
import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use('Qt5Agg')  # skifter backend til Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from io import BytesIO
import yfinance as yf
from .models import aktier, aktiepriser, nyheder_links, annotation
from openai import OpenAI
import datetime as dt


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')    
    buffer.close()
    return graph

def get_plot(x,y, annoteringer):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,5))
    plt.plot(x,y)
    placering = 0.9
    for tekst, dato in annoteringer:
        placering -= 0.05
        plt.annotate(tekst, xy=(dato, placering), xytext=(dato, placering + 0.1), arrowprops=dict(facecolor='red', shrink=0.05), xycoords=('data', 'axes fraction'), textcoords=('data', 'axes fraction'))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.15)
    #plt.title('Sample Plot')
    #plt.xlabel('X-axis')
    #plt.ylabel('Y-axis')
    plt.tight_layout()
    graph = get_graph()
    plt.close()
    return graph

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

## skal sættes på til _i_db__"""
def opsummer_nyheder():
    links = nyheder_links.objects.filter(selskab__selskab="Novo Nordisk B A/S").values_list("link", flat=True)
    links_liste = list(links)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-5.2-chat-latest",
        messages=[{
            "role": "system",
                "content": "Du skal opsummere nyheder til én samlet tekst på ca. tre linjer"},
            {"role": "user", 
                "content": f"Du skal opsummere følgende nyheder til én samlet tekst på ca. tre linjer: {links_liste}"}])
    summaries = response.choices[0].message.content
    print(summaries)

##til terminalen
from stocks.databehandling import opsummer_nyheder
from stocks.models import nyheder_links
from stocks.models import aktier
from openai import OpenAI

def bulk_migrering_annotations():
    df = pd.read_excel("C:/Users/krist/VSCodeProjects/KLN/stocks/bulk_migrering_annotations.xlsx", 
                       parse_dates=['dato_fra', 'dato_til'])

    for index, row in df.iterrows():
        annotation_entry = annotation.objects.create(
            selskab=aktier.objects.get(selskab=row['selskab']), 
            dato_fra=row['dato_fra'], 
            dato_til=row['dato_til'] if pd.notnull(row['dato_til']) else None,
            annotation_text=row['annotation_text'])




    # aktie = aktier.objects.get(selskab="Novo Nordisk B A/S")
    # annotation.objects.create(
    #     selskab=aktie,
    #     dato_fra="2023-01-01",
    #     dato_til="2023-12-31",
    #     annotation_text="Dette er en annotion for Novo Nordisk i 2023"
    # )


#sdg