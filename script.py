import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"Olá, {user_name}! O @QuickBookrosaBot está online e funcionando!")

async def handle(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main_async():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN não foi encontrado!")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))

    asyncio.create_task(web_server())

    await application.initialize()
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.start()
    
    print("Bot iniciado com sucesso via Polling!")
    
    await application.updater.start_polling()

    stop_event = asyncio.Event()
    await stop_event.wait()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        print("Bot interrompido manualmente.")

if __name__ == "__main__":
    main()
