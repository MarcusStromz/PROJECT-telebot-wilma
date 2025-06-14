# handlers/start.py

import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from services.fluxo import fluxo
from handlers.catalogo import enviar_catalogo_pdf
from handlers.agendar import iniciar_agendamento

# Rótulos do menu
OP_CATALOGO = "📄 Catálogo"
OP_AGENDAR  = "🗒️ Agendar"
OP_SUPORTE  = "💬 Suporte"

# Guarda timestamp do último contato
ultimo_contato = {}

def criar_teclado_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton(OP_CATALOGO), KeyboardButton(OP_AGENDAR))
    markup.row(KeyboardButton(OP_SUPORTE))
    return markup

def registrar_start(bot):
    # 1) /start dispara saudação
    @bot.message_handler(commands=['start'])
    def on_start(message):
        chat_id = message.chat.id
        fluxo.resetar(chat_id)
        ultimo_contato[chat_id] = time.time()
        bot.send_message(
            chat_id,
            "Olá! Eu sou a Wilma Santana, designer de sobrancelhas e micropigmentação.\n\n"
            "Para começarmos, qual é o seu nome? 😊",
            reply_markup=ReplyKeyboardRemove()
        )
        fluxo.set_estado(chat_id, "aguardando_nome")

    # 2) Qualquer mensagem *sem estado* também dispara a saudação
    @bot.message_handler(func=lambda m: not fluxo.get_estado(m.chat.id))
    def on_any_before_start(message):
        on_start(message)

    # 3) Recebe o nome e já pede o telefone
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "aguardando_nome")
    def receber_nome(message):
        chat_id = message.chat.id
        fluxo.set_nome(chat_id, message.text.strip())
        fluxo.set_estado(chat_id, "aguardando_telefone")
        ultimo_contato[chat_id] = time.time()
        bot.send_message(
            chat_id,
            "Ótimo! Agora, qual é o seu número de telefone para contato?",
            reply_markup=ReplyKeyboardRemove()
        )

    # 4) Recebe o telefone e mostra o menu
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "aguardando_telefone")
    def receber_telefone(message):
        chat_id = message.chat.id
        fluxo.set_telefone(chat_id, message.text.strip())
        fluxo.set_estado(chat_id, "menu")
        ultimo_contato[chat_id] = time.time()
        bot.send_message(
            chat_id,
            f"Obrigada, {fluxo.get_nome(chat_id)}! 😊\n"
            "Escolha uma opção para continuar:",
            reply_markup=criar_teclado_principal()
        )

    # 5) Ações do menu principal
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_CATALOGO)
    def acionar_catalogo(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_AGENDAR)
    def acionar_agendar(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_SUPORTE)
    def acionar_suporte(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        bot.send_message(
            message.chat.id,
            "📢 Para suporte, envie uma mensagem para: https://wa.me/5581999999999",
            reply_markup=ReplyKeyboardRemove()
        )

    # 6) Timeout de inatividade (5 min), roda *por último* (group=100)
    @bot.message_handler(func=lambda m: True, group=100)
    def verificar_timeout(message):
        chat_id = message.chat.id
        agora = time.time()
        ultima = ultimo_contato.get(chat_id, 0)

        # Se passou >300s e não estamos pedindo nome
        if fluxo.get_estado(chat_id) != "aguardando_nome" and (agora - ultima) > 300:
            # reinicia tudo
            fluxo.resetar(chat_id)
            bot.send_message(
                chat_id,
                "Você ficou inativo por mais de 5 minutos. Vamos reiniciar o atendimento.\n\n"
                "Olá! Qual é o seu nome? 😊",
                reply_markup=ReplyKeyboardRemove()
            )
            fluxo.set_estado(chat_id, "aguardando_nome")

        ultimo_contato[chat_id] = agora
