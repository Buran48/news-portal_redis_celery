from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

BAD_WORDS = [
    'редиска', 'сосиска', 'плох', 'дурак', 'идиот',
    'тупой', 'урод', 'гад', 'сволочь'
]


@register.filter()
@stringfilter
def censor(value):
    if not isinstance(value, str):
        raise ValueError(f"Фильтр нельзя применять к {type(value)}")

    result = value

    for bad_word in BAD_WORDS:
        words_in_text = result.split()
        for i, text_word in enumerate(words_in_text):
            if bad_word.lower() in text_word.lower():
                first_letter = text_word[0]
                censored_word = first_letter + '*' * (len(text_word) - 1)
                words_in_text[i] = censored_word

        result = ' '.join(words_in_text)

    return result