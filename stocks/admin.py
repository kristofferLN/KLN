from django.contrib import admin
from .models import aktier, aktiepriser, nyheder_links, ai_news_summary, annotation, debat, kursmaal
# Register your models here.

@admin.register(aktier)
class AktierAdmin(admin.ModelAdmin):
    list_display = ('selskab', 'ticker', 'paavirkningsfaktorer')
    list_filter = ('selskab', 'ticker')
    search_fields = ('selskab', 'ticker')
    list_editable = ('paavirkningsfaktorer',)

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

@admin.register(annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ('selskab', 'dato_fra', 'dato_til', 'pris_paa_dato_fra', 'annotation_text', 'tidsperiode', 'forced_y_position')
    list_filter = ('selskab', 'dato_fra', 'dato_til')
    search_fields = ('selskab', 'annotation_text')
    list_editable = ('dato_fra', 'dato_til', 'pris_paa_dato_fra', 'annotation_text', 'tidsperiode', 'forced_y_position')

admin.site.register(debat)
list_display = ('bruger', 'tekst', 'created_at')
list_filter = ('bruger', 'created_at')
search_fields = ('bruger', 'tekst')

admin.site.register(kursmaal)
list_display = ('selskab', 'dato', 'kursmål_pris', 'anbefaling', 'analytiker')
list_filter = ('selskab', 'dato', 'anbefaling', 'analytiker')
search_fields = ('selskab', 'dato', 'kursmål_pris', 'anbefaling', 'analytiker')