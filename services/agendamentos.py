import json
from os.path import exists
from services.fluxo import fluxo

ARQUIVO = "agendamentos.json"

def carregar_agendamentos():
    if not exists(ARQUIVO):
        return {}
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar_agendamento(data, hora, chat_id):
    dados = carregar_agendamentos()
    if data not in dados:
        dados[data] = {}

    dados[data][hora] = {
        "chat_id": chat_id,
        "nome": fluxo.get_nome(chat_id),
        "telefone": fluxo.get_telefone(chat_id),
        "servico": fluxo.get_servico(chat_id)
    }

    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

def horarios_disponiveis(data, todos_horarios):
    dados = carregar_agendamentos()
    ocupados = dados.get(data, {})
    return [hora for hora in todos_horarios if hora not in ocupados]
