import json

class ValidationError(Exception):
    pass

def parse_json(response_text: str) -> dict:
    try:
        data = json.loads(response_text)

        if not isinstance(data, dict):
            raise ValidationError("Resposta não é um objeto JSON válido.")

        return data

    except json.JSONDecodeError as e:
        raise ValidationError(f"JSON inválido: {str(e)}")


def validate_required_field(data: dict):
    if "categoria" not in data:
        raise ValidationError("Campo 'categoria' ausente no JSON.")


def validate_allowed_category(data: dict, allowed_categories: list):
    categoria = data.get("categoria")

    if not isinstance(categoria, str):
        raise ValidationError("Campo 'categoria' deve ser uma string.")

    if categoria not in allowed_categories:
        raise ValidationError(
            f"Categoria inválida: {categoria}. Permitidas: {allowed_categories}"
        )

def safe_fallback():
    return {
        "categoria": "Geral",
        "erro": True
    }