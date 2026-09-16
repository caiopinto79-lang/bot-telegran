import os
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Servidor HTTP simples para o Render achar que é um site e manter a porta aberta
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Olá! O @QuickBookrosaBot está online e funcionando perfeitamente!")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("ERRO: TELEGRAM_TOKEN não configurado!")
        return

    # Inicia o servidor web em uma linha separada em segundo plano
    Thread(target=run_web_server, daemon=True).start()

    # Inicialização do bot via Updater
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))

    print("Iniciando o bot em modo Updater Polling com servidor web integrado...")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
