from django.shortcuts import render
from .models import aktier
from .databehandling import get_plot, get_novo_nordisk_data

# Create your views here.

def base_url(request):
    aktier_list = aktier.objects.all()
    novo_data = get_novo_nordisk_data()
    chart = get_plot(novo_data.index, novo_data["Close"])
    return render(request, 'stocks/base_url.html', {'aktier': aktier_list, 'chart': chart})

