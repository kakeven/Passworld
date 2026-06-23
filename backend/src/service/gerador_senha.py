import random


def gerador(qtd=10,letras=True,numeros=True,esp=True):

    alfabeto = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") if letras else []
    caracteres_especiais = list("!@#$%^&*()-_=+[];:.<>/?|`~") if esp else []
    numeros_ = list("0123456789") if numeros else []
    
    todos = numeros_ + alfabeto + caracteres_especiais
    senha=random.choices(todos,k=qtd)
    senha_formatada = "".join(senha)
    return senha_formatada



