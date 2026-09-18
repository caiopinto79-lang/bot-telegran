import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Configuração de Logs para monitorar erros no terminal/servidor
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do Bot do Telegram (Certifique-se que está configurado nas variáveis de ambiente ou cole aqui)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_AQUI")
# ID opcional: se deixar vazio ou em branco, ele tenta detetar o grupo automaticamente se interagir lá
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user
    text = update.message.text if update.message and update.message.text else ""

    logger.log(logging.INFO, f"Mensagem recebida de {user.first_name} no chat {chat.id}: {text}")

    # Responde ao comando do usuário
    await update.message.reply_text("⏳ A processar o seu acesso exclusivo ao Grupo VIP...")

    # Define qual chat usar (se o ID global estiver vazio, usa o chat atual onde o usuário chamou)
    target_chat_id = TELEGRAM_CHANNEL_ID if TELEGRAM_CHANNEL_ID else chat.id

    try:
        # Tenta criar o link de convite automático
        invite_link = await context.bot.create_chat_invite_link(
            chat_id=target_chat_id,
            member_limit=1 # Link de uso único para maior segurança
        )
        
        # Envia o link gerado com sucesso
        await update.message.reply_text(
            f"✅ **Pagamento Aprovado / Acesso Liberado!**\n\n"
            f"Aqui está o seu link exclusivo para entrar no canal:\n{invite_link.invite_link}\n\n"
            f"⚠️ *Este link é de uso único.*",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        logger.error(f"Erro ao gerar link: {e}")
        await update.message.reply_text(
            "❌ O bot encontrou uma restrição ao buscar o link automático. "
            "Certifique-se de que o bot é Administrador do grupo com permissão para 'Convidar usuários via link'."
        )

def main():
    if TELEGRAM_BOT_TOKEN == "SEU_TOKEN_AQUI":
        print("ERRO: Você precisa definir o TOKEN do seu bot do Telegram!")
        return

    # Constrói a aplicação do bot
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Ouve qualquer mensagem de texto enviada para o bot
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Bot rodando com sucesso e pronto para gerar acessos!")
    application.run_polling()

if __name__ == '__main__':
    main()
