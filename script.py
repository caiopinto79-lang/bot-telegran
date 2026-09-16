import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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

    # Inicialização clássica e 100% estável
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Adiciona o comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    print("Iniciando o bot em modo Updater Polling...")
    
    # Inicia o bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
