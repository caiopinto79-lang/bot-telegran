import os
import logging
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Mini servidor HTTP para responder ao Render e manter a porta ativa
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running!")

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# 2. Configuração de logs para acompanhar tudo no console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 3. Função do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O @QuickBookrosaBot está online e funcionando perfeitamente no Render!")

def main():
    # Pega o token seguro das variáveis de ambiente do Render (ou usa o padrão)
    token = os.getenv("TELEGRAM_TOKEN", "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc")
    
    if not token:
        print("ERRO: TELEGRAM_TOKEN não configurado!")
        return

    # Inicia o servidor web em segundo plano para liberar a porta do Render
    Thread(target=run_web_server, daemon=True).start()
    print("Servidor web secundário iniciado na porta HTTP...")

    # Constrói o bot com a API moderna validada
    application = Application.builder().token(token).build()
    
    # Registra o comando
    application.add_handler(CommandHandler("start", start))

    print("Iniciando o bot do Telegram em modo Polling...")
    
    # Roda o bot de forma contínua
    application.run_polling()

if __name__ == '__main__':
    main()
