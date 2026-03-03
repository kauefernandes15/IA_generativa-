from retriever import SimpleRetriever
from llm_client import generate_response
from security import detect_prompt_injection
from validator import validate_json
import json
import os

def carregar_documentos(caminho):

    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho_completo = os.path.join(base_dir, caminho)

    with open(caminho_completo, "r", encoding="utf-8") as f:

        texto = f.read()

    # Divide por blocos (melhor para RAG)
    documentos = texto.split("\n\n")

    return documentos

def main():

    print("Sistema RAG iniciado")
    documentos = carregar_documentos(
        "conhecimento/conhecimento.txt"
    )

    # Inicializa retriever (Embeddings em memória)
    retriever = SimpleRetriever(documentos)
    while True:

        pergunta = input("\nPergunta (ou 'sair'): ")

        if pergunta.lower() == "sair":
            print("Encerrado")
            break

        # Proteção Prompt Injection
        if detect_prompt_injection(pergunta):

            resposta_segura = {
                "status": "não encontrado",
                "resposta": "Tentativa de manipulação detectada."
            }

            print(
                json.dumps(
                    resposta_segura,
                    indent=2,
                    ensure_ascii=False
                )
            )

            continue

        # Busca RAG
        resultados = retriever.retrieve(
            pergunta,
            top_k=3
        )

        contexto = "\n".join(resultados)

        # Chamada LLM
        resposta = generate_response(
            contexto,
            pergunta
        )

        # Validação JSON
        try:

            valido, data = validate_json(resposta)

            print(
                json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False
                )
            )

        except Exception as erro:

            print(
                json.dumps(
                    {
                        "status": "erro",
                        "resposta": str(erro)
                    },
                    indent=2,
                    ensure_ascii=False
                )
            )

if __name__ == "__main__":
    main()