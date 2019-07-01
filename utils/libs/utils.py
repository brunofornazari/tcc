"""
utils.py

Utils.py é responsável por fazer a verificação de atributos de um objetos. Ele realiza uma operação booleana para identificar se
o objeto retornado pertence ao devido processo em que participa.
"""

def check_attribute(object, property):
    for attribute in object:
        if attribute == property: return True

    return False
