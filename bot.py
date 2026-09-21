import os
import requests

# Seu token oficial do BotFather
TELEGRAM_BOT_TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"


def processar_update_telegram(data):
  """Função que recebe os dados do Telegram e processa o comando /ativar"""
  if "message" in data:
    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    # Comando de boas-vindas /start
    if text == "/start":
      enviar_mensagem(
          chat_id,
          "🤖 *Central da Agência Conectada!*\n\nEnvie sua senha no formato:"
          " `/ativar SUA-SENHA` para liberar o seu acesso.",
      )

    # Comando /ativar <senha>
    elif text.startswith("/ativar"):
      partes = text.split(" ")
      if len(partes) < 2:
        enviar_mensagem(
            chat_id,
            "⚠️ Formato inválido.\nUse o exemplo: `/ativar VIP-XXXX-XXXX`",
        )
        return

      senha_informada = partes[1].strip()

      # Resposta de validação inicial para testar o bot funcionando
      enviar_mensagem(
          chat_id,
          f"🔍 Senha recebida com sucesso: `{senha_informada}`\n\nTudo"
          " funcionando perfeitamente!",
      )


def enviar_mensagem(chat_id, texto):
  """Função auxiliar para enviar mensagens de volta no chat"""
  url = f"{TELEGRAM_API_URL}/sendMessage"
  payload = {"chat_id": chat_id, "text": texto, "parse_mode": "Markdown"}
  requests.post(url, json=payload)
