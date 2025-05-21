import time
from services.fluxo import fluxo
from handlers.catalogo import enviar_catalogo_pdf
from handlers.agendar import iniciar_agendamento
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

ultimo_contato = {}

def menu_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📄 Catálogo"), KeyboardButton("📆 Agendar"))
    markup.row(KeyboardButton("💬 Suporte"))
    return markup

def registrar_start(bot):
    @bot.message_handler(commands=['start'])
    def mensagem_boas_vindas(message):
        nome_usuario = message.from_user.first_name
        mensagem = (
            f"Olá, {nome_usuario}, meu nome é Wilma Santana e sou design de sobrancelhas e micropigmentação.\n"
            "Escolha uma opção abaixo para continuar:"
        )
        bot.send_message(message.chat.id, mensagem, reply_markup=menu_principal())
        fluxo.resetar(message.chat.id)
        ultimo_contato[message.chat.id] = time.time()

    @bot.message_handler(func=lambda msg: msg.text == "📄 Catálogo")
    def acionar_catalogo(message):
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "📆 Agendar")
    def acionar_agendar(message):
        iniciar_agendamento(bot, message)
        ultimo_contato[message.chat.id] = time.time()

    @bot.message_handler(func=lambda msg: msg.text == "💬 Suporte")
    def acionar_suporte(message):
        bot.send_message(message.chat.id, "/suporte")
        ultimo_contato[message.chat.id] = time.time()

    # Novo handler para qualquer mensagem
    @bot.message_handler(func=lambda message: True)
    def iniciar_com_qualquer_mensagem(message):
        agora = time.time()
        ultima = ultimo_contato.get(message.chat.id, 0)

        # Se nunca falou ou se passou mais de 600 segundos (10 min)
        if (agora - ultima) > 600:
            nome_usuario = message.from_user.first_name
            mensagem = (
                f"Olá, {nome_usuario}, meu nome é Wilma Santana e sou design de sobrancelhas e micropigmentação.\n"
                "Escolha uma opção abaixo para continuar:"
            )
            bot.send_message(message.chat.id, mensagem, reply_markup=menu_principal())
            fluxo.resetar(message.chat.id)

        # Atualiza o timestamp sempre
        ultimo_contato[message.chat.id] = agora
