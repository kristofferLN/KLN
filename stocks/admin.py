from django.contrib import admin
from .models import aktier
# Register your models here.

admin.site.register(aktier)
list_display = ('selskab', 'ticker')
list_filter = ('selskab', 'ticker')
search_fields = ('selskab', 'ticker')