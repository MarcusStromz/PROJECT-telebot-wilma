from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from services.fluxo import fluxo
from services.feedback import salvar_feedback
from services.agendamentos import horarios_disponiveis, salvar_agendamento
from datetime import datetime

HORARIOS_FIXOS = [f"{h:02d}:00" for h in range(8, 12)] + [f"{h:02d}:00" for h in range(13, 19)]

def criar_teclado_opcoes(opcoes):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for op in opcoes:
        markup.row(KeyboardButton(op))
    return markup

def iniciar_agendamento(bot, message):
    print("[DEBUG] iniciar_agendamento chamado!")
    fluxo.set_estado(message.chat.id, "aguardando_categoria")
    opcoes = ["Sobrancelha", "Facial", "Outros Procedimentos"]
    print(f"[DEBUG] Opções enviadas: {opcoes}")
    bot.send_message(
        message.chat.id,
        "Escolha uma categoria para agendar:",
        reply_markup=criar_teclado_opcoes(opcoes)
    )

def registrar_agendar(bot):
    @bot.message_handler(func=lambda msg: msg.text == "Sobrancelha")
    def opcoes_sobrancelha(message):
        print("[DEBUG] Handler Sobrancelha ativado")
        fluxo.set_estado(message.chat.id, "servico_sobrancelha")
        opcoes = [
            "Design Personalizado",
            "Design e Henna",
            "Design Reconstrutivo",
            "Design Recons + Henna",
            "Micropigmentação"
        ]
        bot.send_message(message.chat.id, "Escolha um serviço de sobrancelha:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(func=lambda msg: msg.text == "Facial")
    def opcoes_facial(message):
        fluxo.set_estado(message.chat.id, "servico_facial")
        opcoes = ["Detox Facial", "Dermaplaning"]
        bot.send_message(message.chat.id, "Escolha um serviço facial:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(func=lambda msg: msg.text == "Outros Procedimentos")
    def opcoes_outros(message):
        fluxo.set_estado(message.chat.id, "servico_outros")
        opcoes = ["Lash Lifting", "Depilação de Buço", "Buço + Queixo", "Depilação Axila"]
        bot.send_message(message.chat.id, "Escolha um serviço:", reply_markup=criar_teclado_opcoes(opcoes))

    @bot.message_handler(func=lambda msg: fluxo.get_estado(msg.chat.id) in ["servico_sobrancelha", "servico_facial", "servico_outros"])
    def apos_escolher_servico(message):
        fluxo.set_servico(message.chat.id, message.text)  
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
            fluxo.set_estado(message.chat.id, "aguardando_feedback")
            
            servico = fluxo.get_servico(message.chat.id)  # ✅ Recupera o serviço

            bot.send_message(
                message.chat.id,
                f"✅ Agendamento confirmado!\n\n📝 Serviço: {servico}\n🕒 Horário: {horario}.\n\nObrigado!"
            )
            
            opcoes_feedback = ["👍 Sim", "👎 Não"]
            bot.send_message(
                message.chat.id,
                "Gostaria de avaliar o atendimento com um feedback?",
                reply_markup=criar_teclado_opcoes(opcoes_feedback)
            )
        else:
            bot.send_message(message.chat.id, "❌ Horário inválido ou já reservado. Tente outro horário.")

    @bot.message_handler(func=lambda msg: fluxo.get_estado(msg.chat.id) == "aguardando_feedback" and msg.text in ["👍 Sim", "👎 Não"])
    def receber_feedback(message):
        resposta = message.text
        print(f"[DEBUG] Feedback recebido: {resposta}")

        if resposta == "👍 Sim":
            bot.send_message(
                message.chat.id,
                "Por favor, deixe seu feedback!",
                reply_markup=ReplyKeyboardRemove()
            )
            fluxo.set_estado(message.chat.id, "esperando_feedback_texto")
        else:
            bot.send_message(
                message.chat.id,
                "Obrigado! Se precisar, volte a entrar em contato.",
                reply_markup=ReplyKeyboardRemove()
            )
            fluxo.resetar(message.chat.id)


    @bot.message_handler(func=lambda msg: fluxo.get_estado(msg.chat.id) == "esperando_feedback_texto")
    def capturar_feedback_texto(message):
        feedback = message.text
        print(f"[DEBUG] Feedback detalhado: {feedback}")

        salvar_feedback(message.chat.id, feedback)

        bot.send_message(message.chat.id, "Agradecemos pelo seu feedback! Voltando ao menu principal.")
        fluxo.resetar(message.chat.id)
