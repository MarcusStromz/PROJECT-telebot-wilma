import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from services.fluxo import fluxo
from handlers.catalogo import enviar_catalogo_pdf
from handlers.agendar import iniciar_agendamento

OP_CATALOGO = "📄 Catálogo"
OP_AGENDAR  = "🗒️ Agendar"
OP_SUPORTE  = "💬 Suporte"

ultimo_contato = {}

def criar_teclado_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton(OP_CATALOGO), KeyboardButton(OP_AGENDAR))
    markup.row(KeyboardButton(OP_SUPORTE))
    return markup

def saudacao(bot, message):
    """Função de saudação que roda em /start e na primeira mensagem sem estado."""
    chat_id = message.chat.id
    agora = time.time()
    
    if fluxo.get_nome(chat_id) and fluxo.get_telefone(chat_id):
        # Usuário já cadastrado → vai para o menu
        bot.send_message(
            chat_id,
            f"Bem-vindo de volta, {fluxo.get_nome(chat_id)}!\n"
            "Escolha uma opção para continuar:",
            reply_markup=criar_teclado_principal()
        )
        fluxo.set_estado(chat_id, "menu")
    else:
        # Primeiro contato → pede o nome
        fluxo.set_estado(chat_id, "aguardando_nome")
        bot.send_message(
            chat_id,
            "Olá! Eu sou a Wilma Santana, designer de sobrancelhas e micropigmentação.\n\n"
            "Para começar, qual é o seu nome? 😊",
            reply_markup=ReplyKeyboardRemove()
        )
    
    ultimo_contato[chat_id] = agora

def registrar_start(bot):
    # 1) /start dispara a saudação
    @bot.message_handler(commands=['start'])
    def on_start(message):
        saudacao(bot, message)

    # 2) Qualquer mensagem inicial (estado vazio) também dispara a saudação
    @bot.message_handler(func=lambda m: not fluxo.get_estado(m.chat.id))
    def on_any_before_start(message):
        saudacao(bot, message)

    # 3) Recebe o nome
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "aguardando_nome")
    def receber_nome(message):
        chat_id = message.chat.id
        fluxo.set_nome(chat_id, message.text.strip())
        fluxo.set_estado(chat_id, "aguardando_telefone")
        ultimo_contato[chat_id] = time.time()
        bot.send_message(
            chat_id,
            "Perfeito! Agora me diga o seu melhor número para contato:",
            reply_markup=ReplyKeyboardRemove()
        )

    # 4) Recebe o telefone e mostra menu
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "aguardando_telefone")
    def receber_telefone(message):
        chat_id = message.chat.id
        fluxo.set_telefone(chat_id, message.text.strip())
        fluxo.set_estado(chat_id, "menu")
        ultimo_contato[chat_id] = time.time()
        bot.send_message(
            chat_id,
            f"Obrigada, {fluxo.get_nome(chat_id)}! 😊\n"
            "Agora escolha uma opção abaixo para continuar:",
            reply_markup=criar_teclado_principal()
        )

    # 5) Menu principal: Catálogo
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_CATALOGO)
    def acionar_catalogo(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        enviar_catalogo_pdf(bot, message)

    # 6) Menu principal: Agendar
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_AGENDAR)
    def acionar_agendar(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        iniciar_agendamento(bot, message)

    # 7) Menu principal: Suporte
    @bot.message_handler(func=lambda m: fluxo.get_estado(m.chat.id) == "menu" and m.text == OP_SUPORTE)
    def acionar_suporte(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()
        bot.send_message(
            message.chat.id,
            "📢 Para suporte, envie uma mensagem para: https://wa.me/5581999999999",
            reply_markup=ReplyKeyboardRemove()
        )

    # 8) Handler de timeout (após 10min sem interação), roda por último
    @bot.message_handler(func=lambda m: True, group=100)
    def verificar_timeout(message):
        chat_id = message.chat.id
        agora = time.time()
        ultima = ultimo_contato.get(chat_id, 0)

        if fluxo.get_estado(chat_id) != "aguardando_nome" and (agora - ultima) > 600:
            fluxo.set_estado(chat_id, "aguardando_nome")
            bot.send_message(
                chat_id,
                "Voltou ao início por inatividade. Qual é o seu nome? 😊",
                reply_markup=ReplyKeyboardRemove()
            )

        ultimo_contato[chat_id] = agora
