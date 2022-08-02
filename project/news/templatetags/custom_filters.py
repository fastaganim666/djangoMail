from django import template


register = template.Library()
stop = ("Денис", "денис")

@register.filter()
def censor(value):
   for word in stop:
      value = value.replace(word, '***')
   return f'{value}'