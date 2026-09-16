import os
import sqlite3
import logging
import asyncio
import threading
from datetime import datetime, timedelta
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuração de Logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Banco de Dados
def iniciar_db():
    conn = sqlite3.connect("clientes.novo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            nome TEXT,
            plano TEXT,
            data_expiracao TEXT,
            payment_id TEXT
        )
    """)
    conn.commit()
    conn.close()

# Servidor Web para o Render (Health Check)
async def handle(request):
    return web.Response(text="Bot VIP rodando perfeitamente!")

async def web_server():
    app_web = web.Application()
    app_web.router.add_get("/", handle)
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

def rodar_web_server():
    # Cria um event loop isolado para a thread do servidor web
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(web_server())

# Funções do Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [
        [InlineKeyboardButton("Plano Mensal", callback_data="mensal")],
        [InlineKeyboardButton("Plano Anual", callback_data="anual")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    await update.message.reply_text("Olá! Escolha o seu plano abaixo:", reply_markup=reply_markup)

async def processar_opcao_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plano = query.data
    user_id = update.effective_user.id
    user_nome = update.effective_user.first_name
    
    # Exemplo de lógica de liberação e cadastro que você já utilizava
    dias = 30 if plano == "mensal" else 365
    data_expiracao = datetime.now() + timedelta(days=dias)
    data_str = data_expiracao.strftime("%Y-%m-%d %H:%M:%S")
    
    # Salvando no banco de dados SQLite
    conn = sqlite3.connect("clientes.novo.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO clientes (telegram_id, nome, plano, data_expiracao, payment_id)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, user_nome, plano, data_str, "simulado_123"))
    conn.commit()
    conn.close()
    
    # Mensagem de sucesso
    mensagem_sucesso = (
        f"✅ **Pagamento Confirmado!**\n\n"
        f"Sua assinatura **{plano}** foi ativada com sucesso!\n"
        f"👉 CLIQUE AQUI PARA ENTRAR NO GRUPO VIP: (link do convite)\n"
        f"Seu acesso individual é válido por {dias} dias. Aproveite!"
    )
    
    try:
        await context.bot.send_message(chat_id=user_id, text=mensagem_sucesso, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")

# Inicialização Principal
def main():
    iniciar_db()
    
    # Inicia o servidor web em uma thread separada para o Render não derrubar o bot
    t = threading.Thread(target=rodar_web_server, daemon=True)
    t.start()
    print("Servidor web iniciado em background.")

    # Constrói e executa o bot de forma oficial e segura (v20+)
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(processar_opcao_plano))
    
    print("Bot do Telegram iniciado com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()
