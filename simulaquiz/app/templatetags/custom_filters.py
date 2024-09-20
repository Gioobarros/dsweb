# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Retorna o valor do dicionário para a chave fornecida."""
    return dictionary.get(key)
