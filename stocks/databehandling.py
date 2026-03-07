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

def get_plot(x,y, annoteringer, filename, selskabet):
    plt.switch_backend('AGG')
    plt.figure(figsize=(6, 5))
    plt.plot(x, y, color = 'black', alpha=1, linewidth=1)
    
    x_list = list(x) ## konverterer x (datoer fra kursgrafen) og y (aktieprisen) til en ægte list.
    y_list = list(y)
    if not x_list or not y_list:
        print("Ingen data tilgængelig for grafen.")
        return None
    max_y = max(y_list)
    max_x = max(x_list)
    min_x = min(x_list)
    offset_base = max_y * 0.05
    ymin,ymax = plt.ylim()
    yticks = plt.yticks()[0]
    plt.ylim(ymin, ymax*1.06)
    plt.yticks(yticks, fontsize="large")
    plt.fill_between(x, y, plt.ylim()[0], alpha=0.3)
    

    annoteringer_filtered = [
    a for a in annoteringer
    if min_x <= a.dato_fra <= max_x
]
    datoer = set(a.dato_fra for a in annoteringer_filtered)
    priser = aktiepriser.objects.filter(selskab__selskab=selskabet, dato__in=datoer)
    pris_dict = {p.dato: p.pris_close for p in priser}

    for a in annoteringer_filtered:
        y_value = pris_dict.get(a.dato_fra)
        if y_value is None:
            continue
        xy = (a.dato_fra, y_value)
        offset = offset_base + ((max_y - y_value) * 0.4)
        plt.annotate(
            a.annotation_text,
            xy=xy,
            xytext=(xy[0], xy[1] + offset + (a.forced_y_position if a.forced_y_position else 0)),
            fontsize=9,
            color='white',
            ha='center',
            va='bottom',
            bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='black', alpha=0.5),
            arrowprops=dict(arrowstyle='-', linestyle='--', color='black')
        )
    
    if not filename.endswith("_10y.png"):     
        ax = plt.gca()
        # --- Major ticks = kvartalsstart (gridlines)
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
        ax.grid(which='major', axis='x', linewidth=0.6, alpha=0.2)

        # --- Minor ticks = midt i kvartalet (labels)
        ax.xaxis.set_minor_locator(
            mdates.MonthLocator(bymonth=[2,5,8,11], bymonthday=15)
        )

        # Slå major labels fra
        ax.xaxis.set_major_formatter(mdates.DateFormatter(''))
        ax.margins(x=0)

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
    filepath = os.path.join(settings.MEDIA_ROOT, 'charts', filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight', format='png')
    plt.close()

##engangsbrug
def aktiepris_close_til_db():
    tickers = aktier.objects.values("ticker")
    for tick in tickers:
        try:    
            aktie = yf.Ticker(tick["ticker"])
            hist = aktie.history(period="max")
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

def aktiekursudvikling(aktie_navn):
    aktiepriser_qs = aktiepriser.objects.filter(selskab__selskab=aktie_navn).order_by('dato')
    en_uge_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=7))
    en_maaned_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=30))
    seks_maaneder_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=180))
    et_år_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=365))
    fem_år_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=365*5))
    ti_år_udvikling = aktiepriser_qs.filter(dato__gte=dt.date.today() - dt.timedelta(days=365*10))
    return {
        "1w": en_uge_udvikling, "1m": en_maaned_udvikling, "6m": seks_maaneder_udvikling, "1y": et_år_udvikling, "5y": fem_år_udvikling, "10y": ti_år_udvikling
    }

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