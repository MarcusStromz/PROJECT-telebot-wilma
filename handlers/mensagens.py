def registrar_mensagens(bot):
    @bot.message_handler(func=lambda message: message.text and 'bom dia' in message.text.lower())
    def responder_bom_dia(message):
        nome_usuario = message.from_user.first_name
        resposta = f"Olá, {nome_usuario}. Em que posso ajudar?"
        bot.reply_to(message, resposta)
