## AI opsummering
## hvis nyt kursmål i dag, så her
## seneste nyhed
## godt debatindlæg (anbefalet bruger, likes, eller markeret af admin)
## seneste debatindlæg
## ..fyld med nyheder... sorteret efter tid

## Tjek om nyt kursmål offentliggjort efter [lukketidspunkt seneste handelsdag] i går, og hvis ja, vis, hvis flere, opsummer
## seneste nyhed

from .models import aktier, aktiepriser, nyheder_links, annotation, debat, kursmaal, ai_news_summary
from datetime import date
import pandas as pd
import requests
from openai import OpenAI
import os




# setip gnews api searching for "Novo Nordisk" news, and print the title of the first article
def gnews_novo():    
    api_key = "394ef32e882df51a02ee747880d9aaa0"
    url = "https://gnews.io/api/v4/search"
    params = {
        "q": "Novo Nordisk",
        "token": api_key,
        "lang": "en",
        "max": 3}
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    artikler =  data['articles']
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY2"))
    summarization_response = openai_client.chat.completions.create(
        model="gpt-5.2-chat-latest",
        messages=[
            {"role": "system", "content": "Du skal opsummere følgende nyheder til én samlet tekst på ca. to linjer"},
            {"role": "user", "content": f"Du skal opsummere følgende nyheder til én samlet tekst på ca. to linjer: {artikler}. Hvis tidspunkt eller medie er vigtigt, må du gerne inddrage det i opsummeringen."}
        ]
    )
    opsamlet_novo = summarization_response.choices[0].message.content
    items = []
    items.append({
            "tid": date.today(),
            "tekst": f"{opsamlet_novo}",
            "type": "novo_nyhed"
    })
    return items

def gnews_novo_makro():
    api_key = "394ef32e882df51a02ee747880d9aaa0"
    params_top_headlines = {
        "country": "us",
        "token": api_key,
        "lang": "en",
        "max": 5
    }
    response_top_headlines = requests.get("https://gnews.io/api/v4/top-headlines", params=params_top_headlines)
    data_top_headlines = response_top_headlines.json()
    artikler_top_headlines = data_top_headlines['articles']
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY2"))
    summarization_makro_response = openai_client.chat.completions.create(
        model="gpt-5.2-chat-latest",
        messages=[
            {"role": "system", "content": "Du skal give et bud på påvirkning for Novo Nordisk"},
            {"role": "user", "content": f"Du skal give et bud på påvirkning for Novo Nordisk og Novo Nordisk aktie ud fra følgende artikler: {artikler_top_headlines}. Du skal opsummere svaret på to linjer og kun returnere dette. De specifikke Novo Nordisk nyheder har jeg et andet sted, så have gerne det store helikopterperspektiv til denne opgave."}
        ]
    )
    opsamlet_novo_makro = summarization_makro_response.choices[0].message.content
    items = []
    items.append({
            "tid": date.today(),
            "tekst": f"{opsamlet_novo_makro}",
            "type": "novo_nyhed_global"
    })
    return items

novo_nyt = pd.read_excel("novo_news.xlsx", sheet_name="Ark1")

def gnews_novo_excel():
    items = []
    items.append({
        'tid': date.today(),
        'tekst': f"{novo_nyt.loc[0, 'novo_news']}",
        "type": "novo_nyhed"
    })
    return items

def gnews_novo_makro_excel():
    items = []
    items.append({
        'tid': date.today(),
        'tekst':f"{novo_nyt.loc[0, 'novo_news_makro']}",
        'type': "novo_nyhed_global"
    })
    return items

novo_tre_nyheder = pd.read_excel("novo_news.xlsx", sheet_name="Ark2")
novo_tre_nyheder["time"] = pd.to_datetime(novo_tre_nyheder["time"])
def get_tre_novo_nyheder():
    items = []
    for index, row in novo_tre_nyheder.iterrows():
        items.append({
            'tid': row['time'].strftime('%H:%M'),
            'tekst': f"{row['title']} ({row['medie']})",
            'type': "novo_tre_nyheder"
        })
    return items











# def hent_ai_nyhedsopsummering(aktie):
#     qs = ai_news_summary.objects.filter(selskab=aktie) ##der er kun en i databasen så skriver ikke mere kode.
#     obj_liste = list(qs)
#     items = []
#     for obj in obj_liste:
#         items.append({
#             "tid": obj.created_at.strftime('%H:%M'),
#             "tekst": f"{obj.summary_text[:150]}...",
#             "type": "ai_nyhed"
#         })
#     return items

# def hent_opsummering_relevante_nyheder(aktie):
#     items = []
#     df = pd.read_excel("aktie_nyheder_summaries.xlsx")
#     data =df.loc[0, aktie]
#     items.append({
#         "tid": None,
#         "tekst": f"{data}",
#         "type": "opsummering_relevante_nyheder"
#     })
#     return items

def byg_seneste_kursmål(aktie):
    qs = kursmaal.objects.filter(selskab=aktie).order_by('-dato')[:2]
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        items.append({
            "tid": None,
            "tekst": f"Nyt kursmål fra {obj.analytiker}: {obj.kursmaal_pris} DKK - {obj.anbefaling}",
            "type": "kursmål"
        })
    return items

def byg_seneste_nyt(aktie):
    qs = nyheder_links.objects.filter(selskab=aktie)
    items = []

    for obj in qs:
        items.append({
            "tid": obj.created_at.strftime('%H:%M'),
            "tekst": f"{obj.titel} ({obj.site})",
            "type": "nyhed"
        })

    return items

def byg_seneste_debat(aktie):
    qs = debat.objects.filter(selskab=aktie).order_by('-created_at')[:2]
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        items.append({
            "tid": obj.created_at.strftime('%H:%M'),
            "tekst": f"{obj.bruger}: {obj.tekst[:140]}",
            "type": "debat"
        })
    return items

def byg_fokus(aktie):
    feed = []
    feed.extend(gnews_novo_excel())
    feed.extend(gnews_novo_makro_excel())
    feed.extend(byg_seneste_kursmål(aktie))
    feed.extend(get_tre_novo_nyheder())
    #feed.extend(byg_seneste_nyt(aktie))
    feed.extend(byg_seneste_debat(aktie))
    return feed
    # Her kan du tilføje logik for at opsummere og formatere disse data til visning i din app.

# from stocks.models import kursmål
# from stocks.fordelingsmotor import byg_seneste_kursmål
# byg_seneste_kursmål(17)
