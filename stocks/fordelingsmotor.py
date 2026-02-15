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

def hent_ai_nyhedsopsummering(aktie):
    qs = ai_news_summary.objects.filter(selskab=aktie) ##der er kun en i databasen så skriver ikke mere kode.
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:   
        tekst = f"{obj.summary_text[:150]}..."
        items.append(tekst)
    return items

def byg_seneste_kursmål(aktie):
    qs = kursmaal.objects.filter(selskab=aktie, dato=date.today())
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        tekst = f"Nyt kursmål fra {obj.analytiker}: {obj.kursmål_pris} DKK - {obj.anbefaling}"
        items.append(tekst)
    return items

def byg_seneste_nyt(aktie):
    qs = nyheder_links.objects.filter(selskab=aktie)
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        tekst = f"{obj.created_at.strftime('%H:%M')} - {obj.titel} ({obj.site})"
        items.append(tekst)
    return items

def byg_seneste_debat(aktie):
    qs = debat.objects.filter(selskab=aktie, created_at__date=date.today())
    obj_liste = list(qs)
    items = []
    for obj in obj_liste:
        tekst = f"{obj.created_at.strftime('%H:%M')} - {obj.bruger}: {obj.tekst[:140]}..."
        items.append(tekst) 
    return items

def byg_fokus(aktie):
    feed = []
    feed.extend(hent_ai_nyhedsopsummering(aktie))
    feed.extend(byg_seneste_kursmål(aktie))
    feed.extend(byg_seneste_nyt(aktie))
    feed.extend(byg_seneste_debat(aktie))
    return feed
    # Her kan du tilføje logik for at opsummere og formatere disse data til visning i din app.

# from stocks.models import kursmål
# from stocks.fordelingsmotor import byg_seneste_kursmål
# byg_seneste_kursmål(17)
