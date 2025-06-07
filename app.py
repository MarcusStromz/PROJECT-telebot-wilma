import telebot
import dotenv
import time
from os import getenv

from handlers.start import registrar_start
from handlers.catalogo import registrar_catalogo
from handlers.agendar import registrar_agendar
from handlers.suporte import registrar_suporte
from services.fluxo import fluxo  

dotenv.load_dotenv()
TOKEN_TELEGRAM = getenv("TOKEN_TELEGRAM")
print(TOKEN_TELEGRAM)

bot = telebot.TeleBot(TOKEN_TELEGRAM)


registrar_start(bot)
registrar_catalogo(bot)
registrar_agendar(bot)
registrar_suporte(bot)
# registrar_mensagens(bot)

@bot.message_handler(func=lambda m: True)
def debug_all(message):
    print(f"[DEBUG_ALL] texto recebido: {repr(message.text)}")
    
if __name__ == '__main__':
    print("[BOT INICIADO] Aguardando interações...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"[ERRO] {e}. Reiniciando bot em 5 segundos...")

            try:
                chat_ids = fluxo.todos_chat_ids()
                for chat_id in chat_ids:
                    try:
                        bot.send_message(chat_id, "⚠️ Tivemos uma falha temporária. Tente novamente.")
                    except Exception as err:
                        print(f"[ERRO ao notificar {chat_id}]: {err}")
            except Exception as err_list:
                print(f"[ERRO ao recuperar chat_ids]: {err_list}")

            time.sleep(5)