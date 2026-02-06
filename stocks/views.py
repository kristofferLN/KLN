from django.shortcuts import render
from .models import aktier

# Create your views here.

def base_url(request):
    aktier_list = aktier.objects.all()
    return render(request, 'stocks/base_url.html', {'aktier': aktier_list})