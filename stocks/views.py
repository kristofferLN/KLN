import os
from django.shortcuts import render
from matplotlib import ticker
from .models import aktier, aktiepriser, ai_news_summary, annotation, debat
from .databehandling import get_plot, aktiekursudvikling, de_seneste_nyheder_i_toppen
from .fordelingsmotor import byg_fokus
from django.utils.text import slugify
from django.conf import settings
from datetime import date, timedelta
from .forms import DebatForm
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.

def frontpage(request):
    return render(request, 'stocks/frontpage.html')

def stocks_frontpage(request):
    aktier_list = aktier.objects.values_list("selskab", flat=True)
    annot_1_y = annotation.objects.filter(tidsperiode="1y")
    annot_10_y = annotation.objects.filter(tidsperiode="10y")

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

        annot_1_y_selskab = annot_1_y.filter(selskab__selskab=hver_aktie)
        annot_10_y_selskab = annot_10_y.filter(selskab__selskab=hver_aktie)

        safe_name = slugify(hver_aktie)
          #filename = f"{safe_name}_10y.png"

          # 1 år
        filename_1y = f"{safe_name}_1y.png"
        filepath_1y = os.path.join(settings.MEDIA_ROOT, 'charts', filename_1y)
        if not os.path.exists(filepath_1y):
            last_year = today - timedelta(days=365)
            data_1y = data.filter(dato__gte=last_year)
            get_plot(
                data_1y.values_list('dato', flat=True),
                data_1y.values_list('pris_close', flat=True),
                annot_1_y_selskab,
                filename_1y,
                hver_aktie
            )
        # 10 år
        filename_10y = f"{safe_name}_10y.png"
        filepath_10y = os.path.join(settings.MEDIA_ROOT, 'charts', filename_10y)
        if not os.path.exists(filepath_10y):
            last_10_years = today - timedelta(days=3650)
            data_10y = data.filter(dato__gte=last_10_years)
            get_plot(
                data_10y.values_list('dato', flat=True),
                data_10y.values_list('pris_close', flat=True),
                annot_10_y_selskab,
                filename_10y,
                hver_aktie
            )
          
        charts[hver_aktie] = {
              "1y": f"/media/charts/{filename_1y}",
              "10y": f"/media/charts/{filename_10y}"
          }

        
        fokus = byg_fokus(18)
    aktiekursudvikling_data = aktiekursudvikling("Novo Nordisk B A/S")
    
    print("BASE_DIR:", settings.BASE_DIR)
    print("MEDIA_ROOT:", settings.MEDIA_ROOT)
    print("exists media_root?", os.path.exists(settings.MEDIA_ROOT))
    print("exists charts dir?", os.path.exists(os.path.join(settings.MEDIA_ROOT, "charts")))
    print("sample file exists?", os.path.exists(os.path.join(settings.MEDIA_ROOT, "charts", "ambu-as_1m.png")))


    debat_indhold = debat.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = DebatForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/stocks/')
    else:
        form = DebatForm()

    seneste_nyheder_i_toppen = de_seneste_nyheder_i_toppen()

    return render(request, 'stocks/stocks_frontpage.html', {'aktier': aktier_list, 'charts': charts, 'fokus_data': fokus, 'aktiekursudvikling_data': aktiekursudvikling_data, 'debat_form': form, 'debat': debat_indhold, 'seneste_nyheder_i_toppen': seneste_nyheder_i_toppen})


#     for selskab, data in stocks_data.items():
#             chart = get_plot(data.index, data["Close"])
#             charts[selskab] = chart