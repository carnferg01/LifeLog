
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    return value.as_widget(attrs={'class': css_class})

# @register.filter(name='add_attr')
# def add_attr(field, arg):
#     attr, val = arg.split(':')
#     return field.as_widget(attrs={attr: val})