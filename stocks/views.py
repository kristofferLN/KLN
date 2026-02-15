import os
from django.shortcuts import render
from matplotlib import ticker
from .models import aktier, aktiepriser, ai_news_summary, annotation
from .databehandling import get_plot
from .fordelingsmotor import byg_fokus
from django.utils.text import slugify
from django.conf import settings
from datetime import date, timedelta


# Create your views here.

def base_url(request):
    aktier_list = aktier.objects.values_list("selskab", flat=True)
    annotation_data = annotation.objects.values_list("annotation_text", "dato_fra", "selskab__selskab", "tidsperiode")
    ai_news_summary_list = ai_news_summary.objects.all()
    #print(aktier_list)
    aktiepriser_list = aktiepriser.objects.all()
    #print(aktiepriser_list[0])
    #stocks_data = get_stocks_data()
    charts = {}
    
    today = date.today()

    for hver_aktie in aktier_list:
        # Filter data for denne aktie
        data = aktiepriser_list.filter(selskab__selskab=hver_aktie)

        annotation_alle = [a for a in annotation_data if a[2] == hver_aktie]

        safe_name = slugify(hver_aktie)
          #filename = f"{safe_name}_10y.png"

          # 1 måned
        filename_1m = f"{safe_name}_1m.png"
        filepath_1m = os.path.join(settings.MEDIA_ROOT, 'charts', filename_1m)
        if not os.path.exists(filepath_1m):
            last_month = today - timedelta(days=30)
            data_1m = data.filter(dato__gte=last_month)
            annot_1m = [(tekst, dato) for tekst, dato, selskab, tidsperiode in annotation_alle if tidsperiode == "1m"]
            print("1m annotations for", hver_aktie, annot_1m)
            get_plot(
                data_1m.values_list('dato', flat=True),
                data_1m.values_list('pris_close', flat=True),
                annot_1m,
                filename_1m
            )
        # 1 år
        filename_1y = f"{safe_name}_1y.png"
        filepath_1y = os.path.join(settings.MEDIA_ROOT, 'charts', filename_1y)
        if not os.path.exists(filepath_1y):
            last_year = today - timedelta(days=365)
            data_1y = data.filter(dato__gte=last_year)
            annot_1y = [(tekst, dato) for tekst, dato, selskab, tidsperiode in annotation_alle if tidsperiode == "1"]
            print("1y annotations for", hver_aktie, annot_1y)
            get_plot(
                data_1y.values_list('dato', flat=True),
                data_1y.values_list('pris_close', flat=True),
                annot_1y,
                filename_1y
            )
          
        charts[hver_aktie] = {
              "1m": f"/media/charts/{filename_1m}",
              "1y": f"/media/charts/{filename_1y}"
          }

        
        fokus = byg_fokus(18)
    
    print("BASE_DIR:", settings.BASE_DIR)
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    print("exists media_root?", os.path.exists(settings.MEDIA_ROOT))
    print("exists charts dir?", os.path.exists(os.path.join(settings.MEDIA_ROOT, "charts")))
    print("sample file exists?", os.path.exists(os.path.join(settings.MEDIA_ROOT, "charts", "ambu-as_1m.png")))


    return render(request, 'stocks/base_url.html', {'aktier': aktier_list, 'charts': charts, 'fokus_data': fokus})


#     for selskab, data in stocks_data.items():
#             chart = get_plot(data.index, data["Close"])
#             charts[selskab] = chart