import os
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Mini servidor HTTP para atender às exigências de porta do Render
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# 2. Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O @QuickBookrosaBot está online e operando na nuvem!")

def main():
    token = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"

    # Inicia o servidor web secundário
    Thread(target=run_web_server, daemon=True).start()
    print("Servidor web secundário iniciado na porta HTTP...")

    try:
        # Constrói a aplicação
        application = Application.builder().token(token).build()
        application.add_handler(CommandHandler("start", start))

        print("Iniciando o bot do Telegram em modo Polling...")
        application.run_polling()
    except Exception as e:
        print(f"ERRO CRTICO AO INICIAR O BOT: {e}")

if __name__ == '__main__':
    main()
