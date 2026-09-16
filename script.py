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

# 2. Configuração de logs para rastreamento no painel
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. Função assíncrona do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O @QuickBookrosaBot está online e operando na nuvem!")

def main():
    # Token oficial do bot
    token = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"

    # Inicia o servidor web secundário em segundo plano (Thread)
    Thread(target=run_web_server, daemon=True).start()
    print("Servidor web secundário iniciado na porta HTTP...")

    # Constrói a aplicação usando exclusivamente a API moderna Application.builder()
    application = Application.builder().token(token).build()
    
    # Registra o manipulador do comando /start
    application.add_handler(CommandHandler("start", start))

    print("Iniciando o bot do Telegram em modo Polling...")
    
    # Executa o bot continuamente
    application.run_polling()

if __name__ == '__main__':
    main()
