from django.shortcuts import render
from matplotlib import ticker
from .models import aktier, aktiepriser, ai_news_summary, annotation
from .databehandling import get_plot

# Create your views here.

def base_url(request):
    aktier_list = aktier.objects.values_list("selskab", flat=True)
    annotation_data = annotation.objects.values_list("annotation_text", "dato_fra")
    ai_news_summary_list = ai_news_summary.objects.all()
    #print(aktier_list)
    aktiepriser_list = aktiepriser.objects.all()
    #print(aktiepriser_list[0])
    #stocks_data = get_stocks_data()
    charts = {}

    for hver_aktie in aktier_list: 
          print(hver_aktie)
          data = aktiepriser_list.filter(selskab__selskab=hver_aktie).order_by('dato')
          annotation_filtreret = annotation_data.filter(selskab__selskab=hver_aktie)
          chart = get_plot(
               data.values_list('dato', flat=True), 
               data.values_list('pris_close', flat=True),
               annotation_filtreret.values_list("annotation_text", "dato_fra"))
          charts[hver_aktie] = chart
    return render(request, 'stocks/base_url.html', {'charts': charts, 'aktier': aktier_list})


#     for selskab, data in stocks_data.items():
#             chart = get_plot(data.index, data["Close"])
#             charts[selskab] = chart