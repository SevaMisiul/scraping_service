cyrillic_letters = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'j',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'ssh',
    'ъ': '`',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'ju',
    'я': 'ja',
}


def from_cyrillic_to_latin(text: str):
    text = text.replace(' ', '_').lower()
    latin_text = ''
    for ch in text:
        latin_text += cyrillic_letters.get(ch, ch)
    return latin_text
