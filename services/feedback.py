import json
import os

FEEDBACKS_FILE = "feedbacks.json"

def salvar_feedback(chat_id, feedback):
    """Salva feedback no arquivo JSON."""
    dados = {}
    # Se arquivo existir, carrega dados existentes
    if os.path.exists(FEEDBACKS_FILE):
        with open(FEEDBACKS_FILE, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                dados = {}
    
    # Adiciona feedback ao chat_id
    if str(chat_id) not in dados:
        dados[str(chat_id)] = []
    
    dados[str(chat_id)].append(feedback)

    # Salva de volta no arquivo
    with open(FEEDBACKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
