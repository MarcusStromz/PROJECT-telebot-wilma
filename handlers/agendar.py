from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from services.fluxo import fluxo
from services.agendamentos import horarios_disponiveis, salvar_agendamento
from datetime import datetime

HORARIOS_FIXOS = [f"{h:02d}:00" for h in range(8, 12)] + [f"{h:02d}:00" for h in range(13, 19)]

def criar_teclado_opcoes(opcoes):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for op in opcoes:
        markup.row(KeyboardButton(op))
    return markup

def iniciar_agendamento(bot, message):
    fluxo.set_estado(message.chat.id, "aguardando_categoria")
    opcoes = ["/Sobrancelha", "/Facial", "/OutrosProcedimentos"]
    bot.send_message(
        message.chat.id,
        "Escolha uma categoria para agendar:",
        reply_markup=criar_teclado_opcoes(opcoes)
    )

def registrar_agendar(bot):
    @bot.message_handler(commands=['agendar'])
    def agendar_servico(message):
        iniciar_agendamento(bot, message)

    @bot.message_handler(commands=['Sobrancelha'])
    def opcoes_sobrancelha(message):
        fluxo.set_estado(message.chat.id, "servico_sobrancelha")
        opcoes = [
            "/Design Personalizado",
            "/Design e Henna",
            "/Design Reconstrutivo",
            "/Design Recons + Henna",
            "Micropigmentação"
        ]
        bot.send_message(message.chat.id, "Escolha um serviço de sobrancelha:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(commands=['Facial'])
    def opcoes_facial(message):
        fluxo.set_estado(message.chat.id, "servico_facial")
        opcoes = ["/Detox Facial", "/Dermaplaning"]
        bot.send_message(message.chat.id, "Escolha um serviço facial:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(commands=['OutrosProcedimentos'])
    def opcoes_outros(message):
        fluxo.set_estado(message.chat.id, "servico_outros")
        opcoes = ["/Lash Lifting", "/Depilação de Buço", "/Buço + Queixo", "Depilação Axila"]
        bot.send_message(message.chat.id, "Escolha um serviço:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(func=lambda msg: fluxo.get_estado(msg.chat.id) in ["servico_sobrancelha", "servico_facial", "servico_outros"])
    def apos_escolher_servico(message):
        fluxo.set_estado(message.chat.id, "pos_servico")
        opcoes = ["Escolher outro serviço", "Agendar Horario"]
        bot.send_message(
            message.chat.id,
            f"Serviço selecionado: {message.text}\nO que você gostaria de fazer a seguir:",
            reply_markup=criar_teclado_opcoes(opcoes)
        )

    @bot.message_handler(func=lambda msg: msg.text == "Escolher outro serviço")
    def escolher_novamente(message):
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "Agendar Horario")
    def escolher_horario(message):
        fluxo.set_estado(message.chat.id, "servico_selecionado")
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        horarios = horarios_disponiveis(data_hoje, HORARIOS_FIXOS)
        if horarios:
            bot.send_message(
                message.chat.id,
                "Escolha um horário clicando em um botão abaixo:",
                reply_markup=criar_teclado_opcoes(horarios)
            )
        else:
            bot.send_message(message.chat.id, "Desculpe, todos os horários estão ocupados hoje.")

    @bot.message_handler(func=lambda msg: fluxo.get_estado(msg.chat.id) == "servico_selecionado")
    def receber_horario(message):
        horario = message.text.strip()
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        if horario in horarios_disponiveis(data_hoje, HORARIOS_FIXOS):
            salvar_agendamento(data_hoje, horario, message.chat.id)
            fluxo.resetar(message.chat.id)
            bot.send_message(message.chat.id, f"✅ Agendamento confirmado para hoje às {horario}. Obrigado!")
        else:
            bot.send_message(message.chat.id, "❌ Horário inválido ou já reservado. Tente outro horário.")
