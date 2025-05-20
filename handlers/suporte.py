def registrar_suporte(bot):
    @bot.message_handler(commands=['suporte'])
    def suporte(message):
        bot.send_message(message.chat.id, "Você escolheu Suporte. Como posso ajudar?")
