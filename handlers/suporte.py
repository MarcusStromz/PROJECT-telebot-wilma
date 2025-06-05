# handlers/suporte.py

from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from services.fluxo import fluxo

OP_ESCOLHER = "Escolher Serviço"
OP_MENU     = "Menu Principal"

def criar_teclado_principal():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton(OP_ESCOLHER), KeyboardButton(OP_MENU))
    return markup

def enviar_menu_principal(bot, message):
    fluxo.resetar(message.chat.id)
    bot.send_message(
        message.chat.id,
        "🔄 Você voltou ao menu principal. Escolha uma opção:",
        reply_markup=criar_teclado_principal()
    )

def registrar_suporte(bot):
    @bot.message_handler(commands=['suporte'])
    def suporte_command(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        bot.send_message(message.chat.id, "Você escolheu Suporte. Como posso ajudar?")

    @bot.message_handler(func=lambda msg: msg.text == OP_MENU)
    def suporte_menu_principal(message):
        bot.clear_step_handler_by_chat_id(message.chat.id)
        print("[DEBUG] Menu Principal clicado por", message.chat.id)
        enviar_menu_principal(bot, message)
