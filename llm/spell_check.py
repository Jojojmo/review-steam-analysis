import json
import re
import logging.config

from ollama import chat
from pydantic import BaseModel, Field

from save_utils import Save

logging.config.fileConfig('logging.ini')
logger = logging.getLogger('root')



class Spell_check(BaseModel):
    correct_text: str = Field(..., description="Texto que foi Corrigido")



SYSTEM_PROMPT = """
Você é um sistema altamente especializado em revisão e correção ortográfica, gramatical e estilística de textos. 
Sua tarefa é revisar o texto fornecido com atenção cuidadosa aos seguintes aspectos:

1. Corrigir erros ortográficos.
2. Ajustar a gramática para garantir clareza e correção.
3. Melhorar a estrutura das frases sem alterar o significado do texto original.
4. Garantir que o texto esteja fluido e formal, sempre respeitando o contexto fornecido.

Ao corrigir o texto, mantenha o tom e a intenção originais. Não adicione interpretações ou informações adicionais que não estejam presentes no texto inicial.
Seu objetivo é fornecer um texto corrigido que seja claro, coeso e gramaticalmente correto.
"""


def spell_check(input_text):
    response = chat(
        messages=[
            {
            'role': 'system',
            'content': SYSTEM_PROMPT
            },
        {
            'role': 'user',
            'content': input_text,
        },
        ],
        model='llama3.1', 
        format=Spell_check.model_json_schema(),
    )
    try:
        json_data = json.loads(response.message.content)
        return Spell_check.model_validate_json(json.dumps(json_data))
    except json.JSONDecodeError as e:
        logger.error("Erro ao decodificar JSON: %s", e)
        return Spell_check.model_validate_json({"correct_text": input_text})



pattern_espacial_char = re.compile(r"[^\wÀ-ÖØ-öø-ÿÇç.,;:!?()\"%\s]", re.IGNORECASE)


@Save
def use_model(obj):
    text = re.sub(pattern_espacial_char, "", obj["texto_review"])
    if text != "":
        processed_text = spell_check(text)
        obj["processed_text"] = processed_text.correct_text #.model_dump()
    else:
        obj["processed_text"] = ""
    return obj


if __name__ == '__main__':
    from pathlib import Path

    content_path = Path(r'data\reviews_raw.json')
    file_path = Path(r'data\reviews_processed_llm.json')
    last_save_file = Path(r'llm\last_save.txt')

    with open(r"data\bucket.json", encoding="utf-8") as file:
        list_reviews = json.load(file)

    use_model(content_path, file_path, last_save_file, batch=5, final_range=len(list_reviews)) 


print("Finalizado!")