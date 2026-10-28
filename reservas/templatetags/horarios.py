from django import template

register = template.Library()


@register.filter
def letra_horario(numero):
    return "ABCDEF"[numero - 1]
