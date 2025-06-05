# handlers/catalogo.py

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from handlers.agendar import iniciar_agendamento
from handlers.suporte import enviar_menu_principal

OP_ESCOLHER = "Escolher Serviço"
OP_MENU     = "Menu Principal"

def teclado_catalogo():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton(OP_ESCOLHER), KeyboardButton(OP_MENU))
    return markup

def enviar_catalogo_pdf(bot, message):
    bot.send_message(
        message.chat.id,
        "📄 Aqui está o catálogo, acesse o link abaixo:\n\n"
        "https://drive.google.com/file/d/1mlmP6mVOx5lNMofjTr8QHdJyqH7X7Xe8/view?usp=sharing",
        reply_markup=teclado_catalogo()
    )

def registrar_catalogo(bot):
    @bot.message_handler(commands=['catalogo'])
    def ver_catalogo(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.send_message(message.chat.id, "Carregando catálogo…", reply_markup=ReplyKeyboardRemove())
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == OP_ESCOLHER)
    def escolher_servico(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        print("[DEBUG] Escolher Serviço clicado por", message.chat.id)
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == OP_MENU)
    def menu_principal(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        print("[DEBUG] Menu Principal clicado por", message.chat.id)
        enviar_menu_principal(bot, message)
