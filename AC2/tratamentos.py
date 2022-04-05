import unidecode
import unicodedata

def tratar(txt):
    texto = unidecode.unidecode(txt).upper()
    return texto
