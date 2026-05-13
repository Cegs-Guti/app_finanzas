from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a un diccionario por clave en los templates: dict|get_item:key"""
    return dictionary.get(key)
