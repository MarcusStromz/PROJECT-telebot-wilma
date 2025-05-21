from handlers.agendar import iniciar_agendamento
from services.log import info
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def teclado_catalogo():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton("📋 Escolher Serviço"), KeyboardButton("🏠 Menu Principal"))
    return markup

def enviar_catalogo_pdf(bot, message):
    info(f"[CATÁLOGO] {message.chat.id} - Enviando link do catálogo.")
    
    link_catalogo = "https://drive.google.com/file/d/1mlmP6mVOx5lNMofjTr8QHdJyqH7X7Xe8/view?usp=sharing"  

    bot.send_message(
        message.chat.id,
        f"Aqui está o catálogo, você pode acessá-lo clicando no link abaixo:\n\n{link_catalogo}",
        reply_markup=teclado_catalogo()
    )

def registrar_catalogo(bot):
    @bot.message_handler(commands=['catalogo'])
    def ver_catalogo(message):
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "📄 Catálogo")
    def acionar_catalogo(message):
        enviar_catalogo_pdf(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "📋 Escolher Serviço")
    def escolher_servico(message):
        iniciar_agendamento(bot, message)

    @bot.message_handler(func=lambda msg: msg.text == "🏠 Menu Principal")
    def voltar_menu(message):
        bot.send_message(message.chat.id, "/start")
