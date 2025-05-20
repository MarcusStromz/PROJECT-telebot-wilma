ADMIN_CHAT_ID = 1589796179
from handlers.catalogo import enviar_catalogo_pdf
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from services.fluxo import fluxo
from handlers.agendar import iniciar_agendamento

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

    @bot.message_handler(func=lambda msg: msg.text == "📄 Catálogo")
    def acionar_catalogo(message):
        bot.send_message(message.chat.id, "/catalogo")

    @bot.message_handler(func=lambda msg: msg.text == "📆 Agendar")
    def acionar_agendar(message):
        from handlers.agendar import iniciar_agendamento
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "💬 Suporte")
    def acionar_suporte(message):
        bot.send_message(message.chat.id, "/suporte")

    # Novo handler para iniciar interação com qualquer mensagem
    @bot.message_handler(func=lambda message: True)
    def iniciar_com_qualquer_mensagem(message):
        if not fluxo.get_estado(message.chat.id):
            nome_usuario = message.from_user.first_name
            mensagem = (
                f"Olá, {nome_usuario}, meu nome é Wilma Santana e sou design de sobrancelhas e micropigmentação.\n"
                "Escolha uma opção abaixo para continuar:"
            )
            bot.send_message(message.chat.id, mensagem, reply_markup=menu_principal())
            fluxo.set_estado(message.chat.id, "inicio")

