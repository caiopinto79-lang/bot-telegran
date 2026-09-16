import sqlite3
import asyncio
from datetime import datetime, timedelta
import os
from aiohttp import web
import mercadopago
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)




sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_TOKEN"))
PLANOS = {
    "plano_mensal": {"nome": "Plano Mensal (30 dias)", "valor": 10.00, "dias": 30},
    "plano_semestral": {"nome": "Plano Semestral (180 dias)", "valor": 45.00, "dias": 180},
    "plano_anual": {"nome": "Plano Anual (365 dias)", "valor": 79.00, "dias": 365}
}

def iniciar_db():
    conn = sqlite3.connect("clientes_novo.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            user_id INTEGER PRIMARY KEY,
            nome TEXT,
            status TEXT,
            data_expiracao TEXT,
            payment_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    mensagem = (
        f"Olá, {user.first_name}! 😈\n\n"
        "**Seja muito bem-vindo ao nosso espaço VIP exclusivo! 🔥**\n\n"
        "Você está a um clique de liberar acesso total aos conteúdos mais desejados, "
        "fotos e vídeos exclusivos sem nenhum tipo de censura.\n\n"
        "🔒 **Acesso 100% via Pix, rápido, seguro e liberado na hora.**\n\n"
        "👇 **Escolha o seu plano abaixo:**"
    )
    keyboard = [
        [InlineKeyboardButton("🟢 Plano Mensal (30 dias) — R$ 10,00", callback_data="plano_mensal")],
        [InlineKeyboardButton("🔥 Semestral (180 dias) — R$ 45,00", callback_data="plano_semestral")],
        [InlineKeyboardButton("💎 Anual (365 dias) — R$ 79,00", callback_data="plano_anual")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(mensagem, reply_markup=reply_markup, parse_mode="Markdown")

async def processar_opcao_plano(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plano_chave = query.data
    plano = PLANOS.get(plano_chave)
    if not plano:
        await query.edit_message_text("Opção inválida.")
        return

    payment_data = {
        "transaction_amount": plano["valor"],
        "description": f"VIP - {plano['nome']}",
        "payment_method_id": "pix",
        "payer": {
            "email": f"user_{query.from_user.id}@telegram.com",
            "first_name": query.from_user.first_name,
        }
    }

    result = sdk.payment().create(payment_data)
    payment = result.get("response", {})

    if "point_of_interaction" not in payment:
        await query.edit_message_text("❌ Ocorreu um erro ao gerar o Pix. Tente novamente em alguns instantes.")
        return

    pix_code = payment["point_of_interaction"]["transaction_data"]["qr_code"]
    payment_id = payment["id"]

    texto_pix = (
        f"✅ *Pix Gerado com Sucesso!*\n\n"
        f"📌 *Plano Selecionado:* {plano['nome']}\n"
        f"💰 *Valor:* R$ {plano['valor']:.2f}\n\n"
        f"Copie o código Pix Copia e Cola abaixo e pague no aplicativo do seu banco:\n\n"
        f"`{pix_code}`\n\n"
        f"_O seu acesso ao Grupo VIP será liberado automaticamente em poucos segundos após a confirmação do pagamento._"
    )

    await query.edit_message_text(texto_pix, parse_mode="Markdown")
    asyncio.create_task(monitorar_pagamento(payment_id, query.from_user.id, query.from_user.first_name, plano, context))

async def monitorar_pagamento(payment_id, user_id, user_nome, plano, context):
    tentativas = 0
    while tentativas < 60:
        await asyncio.sleep(30)
        try:
            res = sdk.payment().get(payment_id)
            status = res["response"].get("status")
            if status == "approved":
                data_expiracao = datetime.now() + timedelta(days=plano["dias"])
                data_str = data_expiracao.strftime("%Y-%m-%d %H:%M:%S")

                conn = sqlite3.connect("clientes_novo.db")
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO clientes (user_id, nome, status, data_expiracao, payment_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, user_nome, "ativo", data_str, str(payment_id)))
                conn.commit()
                conn.close()

                link_invite = await context.bot.create_chat_invite_link(chat_id=GRUPO_VIP_ID, member_limit=1)
                mensagem_sucesso = (
                    "🎉 *Pagamento Confirmado!*\n\n"
                    f"Sua assinatura do **{plano['nome']}** foi ativada com sucesso.\n\n"
                    f"👉 [CLIQUE AQUI PARA ENTRAR NO GRUPO VIP]({link_invite.invite_link})\n\n"
                    f"_Seu acesso é individual e válido por {plano['dias']} dias. Aproveite!_"
                )
                await context.bot.send_message(chat_id=user_id, text=mensagem_sucesso, parse_mode="Markdown")
                break
        except Exception:
            pass
        tentativas += 1

async def checar_expiracoes(app: Application):
    while True:
        try:
            conn = sqlite3.connect("clientes_novo.db")
            cursor = conn.cursor()
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute('SELECT user_id, nome FROM clientes WHERE status = "ativo" AND data_expiracao <= ?', (agora,))
            vencidos = cursor.fetchall()

            for user_id, nome in vencidos:
                try:
                    await app.bot.ban_chat_member(chat_id=GRUPO_VIP_ID, user_id=user_id)
                    await app.bot.unban_chat_member(chat_id=GRUPO_VIP_ID, user_id=user_id)
                    cursor.execute('UPDATE clientes SET status = "expirado" WHERE user_id = ?', (user_id,))
                    conn.commit()
                    await app.bot.send_message(chat_id=user_id, text="⚠️ *Seu período de acesso ao Grupo VIP encerrou.*\n\nPara renovar sua assinatura, basta digitar /start a qualquer momento!", parse_mode="Markdown")
                except Exception:
                    pass
            conn.close()
        except Exception:
            pass
        await asyncio.sleep(30)

async def post_init(app: Application):
    asyncio.create_task(checar_expiracoes(app))

async def handle(request):
    return web.Response(text="Bot VIP rodando perfeitamente!")

async def web_server():
    app_web = web.Application()
    app_web.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app_web)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.AppSite(runner, "0.0.0.0", port)
    await site.start()

def main():
    iniciar_db()
    app = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(processar_opcao_plano))
    
    # Inicia o servidor web em segundo plano e roda o bot
    import asyncio
    loop = asyncio.get_event_loop()
    loop.create_task(web_server())
    
    print("Bot e Servidor web iniciados com sucesso!")
    app.run_polling()

if __name__ == "__main__":
    main()
