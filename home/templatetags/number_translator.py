from django import template
from django.template.defaultfilters import stringfilter

NUMBER_MAP = {
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}

register = template.Library()

def translate_num_eng_to_nep(value):
    translated_value = ""
    for char in value:
        try:
            translated_value+=NUMBER_MAP[char]
        except KeyError:
            translated_value+=char
    return translated_value
    

""" Get food choices from the value """
@register.filter()
@stringfilter
def number_translator(value, lang_code):
    if lang_code == "ne":
        return translate_num_eng_to_nep(value)
    return value