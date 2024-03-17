import re
from deep_translator import GoogleTranslator


def translate(text: str) -> str:
    return GoogleTranslator(source='en', target='ru').translate(text)


def prepare_price(price_str: str):
    if price_str == 'Free':
        return 0
    if price_str is None:
        return None

    price_str = price_str.replace(' TL', '').replace('.', '')
    if ',' in price_str:
        price_str = price_str.split(',')[0]
        return int(price_str) + 1
    return int(price_str)


def transliterate_cyrillic_to_latin(title):
    letters = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z',
        'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z',
        'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ь': '', 'Ы': 'Y', 'Ъ': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', '®': '', '™': ''
    }
    transliterated = ''.join(letters.get(c, c) for c in title)

    transliterated = re.sub(r"[^\w\s-]", "", transliterated)
    transliterated = transliterated.replace(" ", "-")
    transliterated = transliterated.lower()

    return transliterated
