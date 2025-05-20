from handlers.agendar import iniciar_agendamento
from services.log import info
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def teclado_catalogo():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton("📋 Escolher Serviço"), KeyboardButton("🏠 Menu Principal"))
    return markup

def enviar_catalogo_pdf(bot, message):
    info(f"[CATÁLOGO] {message.chat.id} - Enviando catálogo.")
    try:
        with open('C:/Users/marcu/Downloads/Catálogo Sobrancelha s.pdf', 'rb') as catalogo:
            bot.send_document(message.chat.id, catalogo)
        bot.send_message(
            message.chat.id,
            "Escolha uma das opções abaixo:",
            reply_markup=teclado_catalogo()
        )
    except Exception as e:
        info(f"[ERRO CATÁLOGO] {e}")
        bot.send_message(message.chat.id, "Desculpe, não conseguimos enviar o catálogo no momento.")

def registrar_catalogo(bot):
    @bot.message_handler(commands=['catalogo'])
    def ver_catalogo(message):
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "📋 Escolher Serviço")
    def escolher_servico(message):
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
    def voltar_menu(message):
        bot.send_message(message.chat.id, "/start")
