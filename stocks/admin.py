from django.contrib import admin
from .models import aktier, aktiepriser, nyheder_links, ai_news_summary, annotation, debat
# Register your models here.

admin.site.register(aktier)
list_display = ('selskab', 'ticker')
list_filter = ('selskab', 'ticker')
search_fields = ('selskab', 'ticker')

admin.site.register(aktiepriser)
list_display = ('selskab', 'dato', 'pris_close')
list_filter = ('selskab', 'dato')
search_fields = ('selskab', 'dato')

admin.site.register(nyheder_links)
list_display = ('selskab', 'link', 'site', 'titel')
list_filter = ('selskab', 'site')
search_fields = ('selskab', 'site', 'titel')

admin.site.register(ai_news_summary)
list_display = ('selskab', 'summary_text', 'nyheds_type', 'created_at')
list_filter = ('selskab', 'nyheds_type', 'created_at')
search_fields = ('selskab', 'summary_text', 'nyheds_type')

admin.site.register(annotation)
list_display = ('selskab', 'dato_fra', 'dato_til', 'annotation_text')
list_filter = ('selskab', 'dato_fra', 'dato_til')
search_fields = ('selskab', 'annotation_text')
list_editable = ('selskab', 'dato_fra', 'dato_til', 'annotation_text')

admin.site.register(debat)
list_display = ('bruger', 'tekst', 'created_at')
list_filter = ('bruger', 'created_at')
search_fields = ('bruger', 'tekst')