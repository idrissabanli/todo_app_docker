from django.template.defaultfilters import slugify
from unidecode import unidecode


def utf_slugify(value):
   return slugify(unidecode(value.replace(u'ə', 'e').replace(u'Ə', 'e').replace('ı', 'i')))