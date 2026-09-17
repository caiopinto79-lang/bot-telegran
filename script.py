import os
import threading
from flask import Flask
import telebot

# 1. Configuração do Token do Telegram
# Dica: Você pode colar o seu token direto aqui entre as aspas para testar no PyCharm,
# ou configurar nas variáveis de ambiente do seu computador/servidor.
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "COLE_SEU_TOKEN_AQUI_SE_QUISER")

bot = telebot.TeleBot(TOKEN)

# 2. Configuração do Servidor Web (Flask) para manter a aplicação viva na nuvem
app = Flask(__name__)


@app.route('/')
def home():
    return "Agência Bot está rodando com sucesso e online!"


def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# 3. Comandos do Telegram do seu Bot
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    nome_usuario = message.from_user.first_name
    texto = (
        f"Olá, {nome_usuario}! Seja muito bem-vindo(a) à **Agência Bot**.\n\n"
        "Como posso te ajudar hoje? Escolha uma das opções abaixo:\n"
        "/produtos - Ver catálogo e ofertas\n"
        "/ajuda - Falar com o suporte"
    )
    bot.reply_to(message, texto, parse_mode="Markdown")


@bot.message_handler(commands=['produtos', 'catalogo'])
def listar_produtos(message):
    texto = (
        "🛍️ **Catálogo Disponível:**\n\n"
        "• Linha de Cosméticos e Perfumaria\n"
        "• Assinaturas de Canais e Streaming\n\n"
        "Entre em contato para consultar valores e disponibilidade!"
    )
    bot.reply_to(message, texto, parse_mode="Markdown")


@bot.message_handler(commands=['ajuda'])
def enviar_ajuda(message):
    bot.reply_to(message, "Se precisar de suporte, envie sua dúvida por aqui que logo responderemos.")


# 4. Execução Simultânea (Servidor Web + Bot)
if __name__ == "__main__":
    # Inicia o servidor web em segundo plano (Thread)
    web_thread = threading.Thread(target=run_web_server)
    web_thread.daemon = True
    web_thread.start()

    print("Servidor web e Agência Bot iniciados com sucesso! Pressiona Ctrl+C para parar.")

    # Inicia o bot do Telegram (escutando as mensagens)
    bot.infinity_polling()
