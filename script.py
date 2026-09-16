import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Configura os logs para aparecerem direitinho no Render
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

    # Constrói a aplicação do bot
    app = ApplicationBuilder().token(token).build()
    
    # Adiciona o comando /start
    app.add_handler(CommandHandler("start", start))

    print("Iniciando o bot em modo Polling...")
    
    # Inicia o polling diretamente (sem servidor web pesado para evitar conflito)
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
