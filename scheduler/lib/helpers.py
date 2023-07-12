from datetime import datetime


def get_current_month_name():
    return datetime.now().strftime('%B')


def get_current_year_name():
    return datetime.now().strftime('%Y')


def replace_key_words(x):
    key_word_replacements = {
        '<month>': get_current_month_name(),
        '<year>': get_current_year_name(),
        '<date>': datetime.now().strftime('%Y-%m-%d'),
    }

    for word, replacement in key_word_replacements.items():
        if word in x:
            x = x.replace(word, replacement)

    return x

