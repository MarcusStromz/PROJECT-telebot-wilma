import telebot
import dotenv
import time
from os import getenv

from handlers.start import registrar_start
from handlers.catalogo import registrar_catalogo
from handlers.agendar import registrar_agendar
from handlers.suporte import registrar_suporte
from handlers.mensagens import registrar_mensagens

dotenv.load_dotenv()
TOKEN_TELEGRAM = getenv("TOKEN_TELEGRAM")
print(TOKEN_TELEGRAM)

bot = telebot.TeleBot(TOKEN_TELEGRAM)

# ✅ Ajuste na ordem: registrar_catalogo antes do start
registrar_agendar(bot)
registrar_catalogo(bot)  # ⬅️ IMPORTANTE
registrar_start(bot)
registrar_suporte(bot)
registrar_mensagens(bot)

if __name__ == '__main__':
    print("[BOT INICIADO] Aguardando interações...")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"[ERRO] {e}. Reiniciando bot em 5 segundos...")
            time.sleep(5)
