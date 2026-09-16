import os
import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! O @QuickBookrosaBot está online e funcionando perfeitamente!")

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("ERRO: TELEGRAM_TOKEN não configurado!")
        return

    # Usando o construtor padrão da Application
    application = Application.builder().token(token).build()
    
    # Adiciona o comando /start
    application.add_handler(CommandHandler("start", start))

    print("Iniciando o bot em modo Polling...")
    
    # Inicia o polling de forma limpa e compatível
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
