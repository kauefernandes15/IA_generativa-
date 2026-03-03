from llm_client import gerar_resposta
from validator import (
    parse_json,
    validate_required_field,
    validate_allowed_category,
    safe_fallback,
    ValidationError
)

CATEGORIAS = ["Suporte", "Vendas", "Financeiro", "Geral"]


def classificar_mensagem(mensagem, temperature=0.2):
    prompt = f"""
Classifique a mensagem abaixo em uma das seguintes categorias: {', '.join(CATEGORIAS)}.
Retorne apenas um JSON no formato:
{{
    "categoria": "nome_categoria"
}}

Mensagem: "{mensagem}"
"""

    try:
        resposta = gerar_resposta(prompt, temperature)

        data = parse_json(resposta)
        validate_required_field(data)
        data["categoria"] = data["categoria"].strip().title()

        validate_allowed_category(data, CATEGORIAS)

        return data

    except ValidationError as e:
        print(f"[VALIDATION ERROR] {e}")
        return safe_fallback()

    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")
        return safe_fallback()