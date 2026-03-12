import json
import os

ARQUIVO_MEMORIA = "memoria.json"
LIMITE_MEMORIA = 10

def carregar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_memoria(memoria):
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

def adicionar_mensagem(memoria, mensagem):
    memoria.append(mensagem)

    if len(memoria) > LIMITE_MEMORIA:
        memoria.pop(1)

def limpar_memoria():
    if os.path.exists(ARQUIVO_MEMORIA):
        os.remove(ARQUIVO_MEMORIA)