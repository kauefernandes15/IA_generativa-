from groq import Groq
from dotenv import load_dotenv
import os
from prompt import build_system_prompt

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"
def generate_response(contexto, pergunta):

    system_prompt = build_system_prompt()

    user_prompt = f"""
RESPONDA APENAS usando o contexto abaixo.

Se a resposta não estiver no contexto, responda:

{{
"status": "não encontrado"
}}

CONTEXTO:
{contexto}


PERGUNTA:
{pergunta}


LEMBRE-SE:

- Não invente respostas
- Use somente o contexto
- Seja objetivo
- Retorne JSON válido
"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {"role": "system", "content": system_prompt},

            {"role": "user", "content": user_prompt}

        ],

        temperature=0.1
    )

    return response.choices[0].message.content