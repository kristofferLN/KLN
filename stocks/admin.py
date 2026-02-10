from django.contrib import admin
from .models import aktier, aktiepriser
# Register your models here.

admin.site.register(aktier)
list_display = ('selskab', 'ticker')
list_filter = ('selskab', 'ticker')
search_fields = ('selskab', 'ticker')

admin.site.register(aktiepriser)
list_display = ('selskab', 'dato', 'pris_close')
list_filter = ('selskab', 'dato')
search_fields = ('selskab', 'dato')