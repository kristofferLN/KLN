from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    if isinstance(d, dict):
        return d.get(key, '')
    return None

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)