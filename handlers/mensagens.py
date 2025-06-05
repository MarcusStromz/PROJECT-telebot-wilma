# handlers/mensagens.py

def registrar_mensagens(bot):
    @bot.message_handler(
        func=lambda msg: msg.text and 'bom dia' in msg.text.lower(),
        content_types=['text'],
        group=100  # roda *depois* de todos os handlers de grupo 0 (fluxo, catálogo etc)
    )
    def responder_bom_dia(message):
        nome_usuario = message.from_user.first_name
        resposta = f"Olá, {nome_usuario}. Em que posso ajudar?"
        bot.reply_to(message, resposta)
