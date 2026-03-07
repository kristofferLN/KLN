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

def hent_ai_nyhedsopsummering(aktie):
    qs = ai_news_summary.objects.filter(selskab=aktie) ##der er kun en i databasen så skriver ikke mere kode.
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        items.append({
            "tid": obj.created_at.strftime('%H:%M'),
            "tekst": f"{obj.summary_text[:150]}...",
            "type": "ai_nyhed"
        })
    return items

def hent_opsummering_relevante_nyheder(aktie):
    items = []
    df = pd.read_excel("aktie_nyheder_summaries.xlsx")
    data =df.loc[0, aktie]
    items.append({
        "tid": None,
        "tekst": f"{data}",
        "type": "opsummering_relevante_nyheder"
    })
    return items

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
    feed.extend(hent_ai_nyhedsopsummering(aktie))
    feed.extend(byg_seneste_kursmål(aktie))
    feed.extend(byg_seneste_nyt(aktie))
    feed.extend(byg_seneste_debat(aktie))
    feed.extend(hent_opsummering_relevante_nyheder(aktie))
    return feed
    # Her kan du tilføje logik for at opsummere og formatere disse data til visning i din app.

# from stocks.models import kursmål
# from stocks.fordelingsmotor import byg_seneste_kursmål
# byg_seneste_kursmål(17)
