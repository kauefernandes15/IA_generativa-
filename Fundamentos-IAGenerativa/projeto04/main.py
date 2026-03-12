from groq import Groq
from dotenv import load_dotenv
import os

from tools import (
    data_atual,
    calcular_idade,
    converter_temperatura,
    calcular_imc
)

from memory_manager import (
    carregar_memoria,
    salvar_memoria,
    adicionar_mensagem,
    limpar_memoria
)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")

client = Groq(api_key=api_key)
historico_mensagens = carregar_memoria()

PERSONA = {
    "role": "system",
    "content": "Você é um assistente amigável, educado e objetivo."
}

if len(historico_mensagens) == 0:
    historico_mensagens.append(PERSONA)


def chat(pergunta):
    global historico_mensagens

    adicionar_mensagem(historico_mensagens, {
        "role": "user",
        "content": pergunta
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=historico_mensagens
    )

    resposta = response.choices[0].message.content
    adicionar_mensagem(historico_mensagens, {
        "role": "assistant",
        "content": resposta
    })

    salvar_memoria(historico_mensagens)
    return resposta

print("Assistente iniciado. Digite 'sair' para encerrar.")

while True:
    pergunta = input("\nVocê: ")

    if pergunta.lower() in ["sair", "exit", "quit"]:
        print("Encerrando assistente.")
        break

    if pergunta == "/limpar":
        limpar_memoria()
        historico_mensagens = [PERSONA]
        print("Assistente: Memória da conversa apagada.")
        continue

    if "data" in pergunta.lower():
        resposta = f"Hoje é {data_atual()}"
        print("Assistente:", resposta)
        continue

    if "idade" in pergunta.lower():
        ano = int(input("Digite seu ano de nascimento: "))
        idade = calcular_idade(ano)
        print("Assistente:", f"Você tem aproximadamente {idade} anos.")
        continue

    if "temperatura" in pergunta.lower():
        valor = float(input("Digite a temperatura em Celsius: "))
        resultado = converter_temperatura(valor)
        print("Assistente:", f"{valor}°C equivalem a {resultado}°F")
        continue

    if "imc" in pergunta.lower():
        peso = float(input("Peso (kg): "))
        altura = float(input("Altura (m): "))
        imc = calcular_imc(peso, altura)
        print("Assistente:", f"Seu IMC é {imc:.2f}")
        continue

    resposta = chat(pergunta)
    print("Assistente:", resposta)