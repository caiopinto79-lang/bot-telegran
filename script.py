import os
import telebot
import requests
from flask import Flask, request, jsonify

# ==================== CONFIGURAÇÕES ====================
# Insira os seus tokens e chaves reais aqui ou use variáveis de ambiente
TELEGRAM_TOKEN = "SEU_TOKEN_DO_BOT_AQUI"
MERCADO_PAGO_ACCESS_TOKEN = "SEU_ACCESS_TOKEN_DO_MERCADO_PAGO_AQUI"

# ID do seu canal VIP (ex: -100xxxxxxxxxx)
TELEGRAM_CHANNEL_ID = "-100SEU_ID_DO_CANAL_AQUI"

# ID do seu chat/grupo pessoal se quiser receber notificações de vendas (opcional)
NOTIFICATION_CHAT_ID = "SEU_CHAT_ID_PESSOAL_AQUI"

# Inicializa o Bot do Telegram e o Flask
bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)


# ==================== ROTAS DO FLASK (SITE / WEBHOOK) ====================

@app.route('/')
def home():
    return "Servidor rodando com sucesso! O Bot e o Mercado Pago estão integrados."

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Rota que recebe as notificações (webhooks) do Mercado Pago quando um pagamento muda de status.
    """
    try:
        data = request.get_json()
        print("Notificação recebida do Mercado Pago:", data)
        
        # O Mercado Pago pode enviar diferentes tipos de notificações
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                # Consulta os detalhes do pagamento na API do Mercado Pago
                headers = {
                    'Authorization': f'Bearer {MERCADO_PAGO_ACCESS_TOKEN}'
                }
                response = requests.get(f'https://api.mercadopago.com/v1/payments/{payment_id}', headers=headers)
                
                if response.status_code == 200:
                    payment_info = response.json()
                    status = payment_info.get('status')
                    external_reference = payment_info.get('external_reference') # Aqui podemos passar o ID/Username do Telegram do cliente
                    
                    print(f"Pagamento {payment_id} status: {status} | Ref: {external_reference}")
                    
                    # Se o pagamento foi aprovado com sucesso
                    if status == 'approved':
                        # Se você salvou o ID do usuário do Telegram no external_reference, 
                        # pode gerar e enviar o link automaticamente para ele aqui:
                        if external_reference and external_reference.isdigit():
                            chat_id_cliente = int(external_reference)
                            gerar_e_enviar_convite(chat_id_cliente)
                        
                        # Notifica você no chat pessoal
                        if NOTIFICATION_CHAT_ID:
                            try:
                                bot.send_message(
                                    NOTIFICATION_CHAT_ID, 
                                    f"✅ Venda Aprovada!\nID do Pagamento: {payment_id}\nCliente Ref: {external_reference}"
                                )
                            except Exception as e:
                                print(f"Erro ao enviar notificação interna: {e}")
                                
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"Erro no processamento do webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== FUNÇÕES DO TELEGRAM ====================

def gerar_e_enviar_convite(chat_id):
    """
    Gera um link de convite de uso único com validade (ex: 24 horas) para o canal VIP
    e envia diretamente para o chat do cliente no Telegram.
    """
    try:
        # Cria um link de convite que expira em 1 dia (86400 segundos) e permite apenas 1 uso
        invite_link = bot.create_chat_invite_link(
            chat_id=TELEGRAM_CHANNEL_ID,
            expire_date=None, # Ou coloque um timestamp unix se preferir data fixa
            member_limit=1    # Link de uso único
        )
        
        link_url = invite_link.invite_link
        
        mensagem = (
            "🎉 Pagamento confirmado com sucesso!\n\n"
            "Muito obrigado pela sua assinatura. Aqui está o seu link exclusivo e de uso único "
            "para entrar no nosso canal VIP:\n\n"
            f"{link_url}\n\n"
            "⚠️ *Atenção:* Este link é pessoal e expira após o primeiro uso."
        )
        
        bot.send_message(chat_id, mensagem, parse_mode="Markdown")
        print(f"Link de convite enviado com sucesso para o chat ID: {chat_id}")
        
    except Exception as e:
        print(f"Erro ao gerar link de convite para o chat {chat_id}: {e}")
        try:
            bot.send_message(
                chat_id, 
                "✅ Seu pagamento foi aprovado, mas tivemos um pequeno problema ao gerar o link automático. "
                "Por favor, entre em contato com o suporte informando o comprovante para liberar seu acesso."
            )
        except:
            pass


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """
    Mensagem de boas-vindas quando o usuário interage com o bot no Telegram.
    """
    texto = (
        "Olá! Seja bem-vindo(a).\n\n"
        "Este bot gerencia as assinaturas dos canais VIP.\n"
        "Após realizar o seu pagamento pelo link de checkout, seu acesso será liberado automaticamente aqui!"
    )
    bot.reply_to(message, texto)


# ==================== INICIALIZAÇÃO DO SERVIDOR ====================

if __name__ == '__main__':
    # O Render ou servidores web costumam usar a porta especificada na variável de ambiente PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
