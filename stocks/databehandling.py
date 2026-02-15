import os
import pandas as pd
import numpy as np
#import matplotlib
#matplotlib.use('Qt5Agg')  # skifter backend til Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import base64
from io import BytesIO
import yfinance as yf
from .models import aktier, aktiepriser, nyheder_links, annotation
from openai import OpenAI
import datetime as dt
from django.conf import settings
from adjustText import adjust_text


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')    
    buffer.close()
    return graph

def get_plot(x,y, annoteringer, filename):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,8))
    plt.plot(x,y, color='blue', alpha=0.10)
    plt.margins(x=0.2)
    plt.margins(y=0.2)

    x_list = list(x) ## konverterer x (datoer fra kursgrafen) og y (aktieprisen).
    y_list = list(y)
    

    if not x_list or not y_list:
        print("Ingen data tilgængelig for grafen.")
        return None

    offset = (max(y_list) - min(y_list)) * 0.05
    placerings_dict = {}

    x_min = min(x_list)
    x_max = max(x_list)
    

    annoteringer_filtered = [
        (tekst, dato) for tekst, dato in annoteringer
        if x_min <= dato <= x_max
    ] ## filtrerer med list comprehension annoteringer, så de kun inkluderer dem, der falder inden for x-aksens interval.

    for tekst, dato in annoteringer_filtered:
        nærmeste_index = min(range(len(x_list)), key=lambda i: abs(x_list[i] - dato)) ## finder nærmeste dato i x_list til annoteringens dato
        print(nærmeste_index)
        x_val = x_list[nærmeste_index]
        print(x_val)
        y_val = y_list[nærmeste_index]
        print(y_val)

        n  = placerings_dict.get(x_val, 0)
        y_offset = y_val + offset * (n + 1)
        placerings_dict[x_val] = n + 1

        plt.annotate(
            tekst,
            xy=(x_val, y_val),
            xytext=(x_val, y_offset),
            ha='center',
            va='bottom',
            fontsize=10,
            arrowprops=dict(
                arrowstyle='->',
                color='red',
                linewidth=0.8
            )
        )
    ax = plt.gca()
    # --- Major ticks = kvartalsstart (gridlines)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
    ax.grid(which='major', axis='x', linewidth=0.8, alpha=0.4)

    # --- Minor ticks = midt i kvartalet (labels)
    ax.xaxis.set_minor_locator(
        mdates.MonthLocator(bymonth=[2,5,8,11], bymonthday=15)
    )

    # Slå major labels fra
    ax.xaxis.set_major_formatter(mdates.DateFormatter(''))

    # Formatter til Q1, Q2 osv.
    def quarter_formatter(x, pos=None):
        date = mdates.num2date(x)
        quarter = (date.month - 1) // 3 + 1
        return f"Q{quarter}"

    ax.xaxis.set_minor_formatter(FuncFormatter(quarter_formatter))

    # Vis kun minor labels
    ax.tick_params(axis='x', which='minor', labelsize=9)
    #plt.title('Sample Plot')
    #plt.xlabel('X-axis')
    #plt.ylabel('Y-axis')
    plt.tight_layout()
    filepath = os.path.join(settings.MEDIA_ROOT, 'charts', filename)
    plt.savefig(filepath, format='png')
    plt.close()

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