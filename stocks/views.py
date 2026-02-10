from django.shortcuts import render
from matplotlib import ticker
from .models import aktier
from .databehandling import get_plot, get_stocks_data

# Create your views here.

def base_url(request):
    aktier_list = aktier.objects.all()
    stocks_data = get_stocks_data()
    charts = {}
    for selskab, data in stocks_data.items():
            chart = get_plot(data.index, data["Close"])
            charts[selskab] = chart
    return render(request, 'stocks/base_url.html', {'charts': charts, 'aktier': aktier_list})
