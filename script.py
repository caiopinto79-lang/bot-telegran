import os
import time
import threading
import requests
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify
import mercadopago
import telebot

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ================= CONFIGURAÇÕES =================
ACCESS_TOKEN_MP = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
sdk = mercadopago.SDK(ACCESS_TOKEN_MP)

TELEGRAM_BOT_TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI" # Seu chat ID pessoal opcional para avisos

# ID do seu Grupo VIP (Ex: -100xxxxxxxxxx). O bot precisa ser ADM com permissão de convidar via link!
TELEGRAM_CHANNEL_ID = "-100SEU_ID_DO_GRUPO_AQUI" 

# Inicializa o Bot do Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

LINK_DIRETO_BOT = "https://t.me/QuickBookrosaBot?text=Quero%20meu%20acesso%20ao%20Canal%20VIP"
# =================================================

INSTAGRAM_LINK = "https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj"
TIKTOK_LINK = "https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE"
KWAI_LINK = "https://k.kwai.com/u/@mc.iasmin_ofc/xM6daWCD"

TELEGRAM_PREVIAS_LINK = "#"
PRIVACY_LINK = "#"

ip_blocklist = {}

def verificar_bloqueio():
    ip = request.remote_addr
    if ip in ip_blocklist:
        tempo_restante = ip_blocklist[ip] - time.time()
        if tempo_restante > 0:
            return int(tempo_restante / 60) + 1
        else:
            del ip_blocklist[ip]
    return 0

def enviar_notificacao_telegram(nome, email, whatsapp, telegram_user):
    if TELEGRAM_CHAT_ID == "SEU_CHAT_ID_AQUI":
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    mensagem = (
        f"👑 *NOVO CADASTRO - GRUPO VIP*\n\n"
        f"👤 *Nome:* {nome}\n"
        f"📧 *E-mail:* {email}\n"
        f"📱 *WhatsApp:* {whatsapp}\n"
        f"💬 *Telegram:* {telegram_user}\n\n"
        f"💳 *Status:* Pix de R$ 1,00 gerado (Aguardando pagamento)."
    )
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"Erro ao enviar notificação para o Telegram: {e}")

# ================= LÓGICA DO BOT DO TELEGRAM =================
@bot.message_handler(func=lambda message: True)
def responder_mensagens(message):
    texto = message.text.lower()
    chat_id = message.chat.id
    
    if "/start" in texto:
        bot.reply_to(
            message, 
            "Olá! Seja bem-vindo(a) ao atendimento automatizado da Iasmin.\n\n"
            "Assim que o seu pagamento for aprovado no site, clique no botão para receber seu link de acesso exclusivo ao Grupo VIP!"
        )
        return

    if "quero" in texto or "acesso" in texto or "vip" in texto:
        bot.send_message(chat_id, "⏳ A processar o seu acesso exclusivo ao Grupo VIP...")

        try:
            # Puxa o link de convite oficial do grupo configurado
            invite_link = bot.export_chat_invite_link(chat_id=TELEGRAM_CHANNEL_ID)
            
            resposta = (
                f"🎉 **Acesso Liberado com Sucesso!**\n\n"
                f"Muito obrigado pelo apoio! Aqui está o seu link de convite exclusivo para o Grupo VIP:\n\n"
                f"👉 {invite_link}\n\n"
                f"⚠️ *Atenção:* Este link é oficial e pessoal. Não compartilhe com outras pessoas!"
            )
            bot.send_message(chat_id, resposta, parse_mode="Markdown")
            print(f"✅ Link do grupo enviado com sucesso para o chat ID: {chat_id}")
            
        except Exception as e:
            erro_msg = str(e)
            print(f"❌ ERRO AO GERAR LINK DO GRUPO: {erro_msg}")
            bot.send_message(
                chat_id, 
                "❌ O bot encontrou uma restrição ao buscar o link automático. "
                "Certifique-se de que o ID do grupo está correto e que o bot é Administrador com permissão para 'Convidar usuários via link'."
            )

def rodar_bot_telegram():
    print("🤖 Bot do Telegram iniciado e a escutar mensagens...")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Aviso: Bot reiniciou devido a desconexão temporária: {e}")
            time.sleep(5)
# ==============================================================

CSS_RESPONSIVO = """
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 16px; }
    .container { background: rgba(24, 24, 27, 0.95); padding: 30px 20px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 420px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
    .avatar { width: 85px; height: 85px; border-radius: 50%; background: #ff2a6d; margin: 0 auto 15px auto; display: flex; align-items: center; justify-content: center; font-size: 34px; font-weight: bold; color: #fff; border: 3px solid rgba(255,42,109,0.4); }
    h1, h2 { color: #fff; font-size: 21px; margin-bottom: 8px; }
    .bio, p { font-size: 13.5px; color: #a1a1aa; margin-bottom: 20px; line-height: 1.5; }
    .btn { background-color: #ff2a6d; color: white; border: none; padding: 13px 18px; border-radius: 12px; font-size: 14.5px; cursor: pointer; width: 100%; font-weight: bold; transition: all 0.2s; margin-top: 10px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 15px rgba(255,42,109,0.3); }
    .btn:hover { background-color: #e01b5d; transform: translateY(-1px); }
    .btn-social { background-color: #18181b; border: 1px solid #27272a; color: #f1f1f1; }
    .btn-social:hover { background-color: #27272a; border-color: #ff2a6d; }
    .btn-adult { background: linear-gradient(135deg, #ff2a6d, #9d4edd); box-shadow: 0 4px 15px rgba(157,78,221,0.4); }
    .btn-secundario { background-color: #27272a; border: 1px solid #3f3f46; color: #fff; box-shadow: none; }
    .btn-secundario:hover { background-color: #3f3f46; }
    .btn-privacy { background-color: #00aff0; box-shadow: 0 4px 15px rgba(0,175,240,0.3); }
    .btn-telegram { background-color: #229ed9; box-shadow: 0 4px 15px rgba(34,158,217,0.3); }
    .btn-vip { background-color: #00e676; color: #000; box-shadow: 0 4px 15px rgba(0,230,118,0.3); }
    .btn-vip:hover { background-color: #00c853; }
    .form-group { margin-bottom: 15px; text-align: left; }
    .form-group label { display: block; font-size: 12.5px; color: #a1a1aa; margin-bottom: 5px; font-weight: 600; }
    .form-control { width: 100%; padding: 12px; border-radius: 10px; background-color: #18181b; border: 1px solid #27272a; color: #fff; font-size: 14px; outline: none; transition: border-color 0.2s; }
    .form-control:focus { border-color: #00e676; }
    .divider { height: 1px; background: rgba(255,255,255,0.08); margin: 20px 0; }
    .section-title { font-size: 13px; color: #a1a1aa; margin-bottom: 8px; text-align: left; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .nav-footer { display: flex; gap: 8px; margin-top: 18px; width: 100%; }
    .nav-btn { flex: 1; padding: 10px; border-radius: 10px; font-size: 13px; font-weight: 600; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 6px; border: 1px solid #27272a; transition: background 0.2s; }
    .nav-inicio { background-color: #27272a; color: #fff; }
    .nav-inicio:hover { background-color: #3f3f46; border-color: #ff2a6d; }
    .nav-voltar { background-color: #18181b; color: #a1a1aa; }
    .nav-voltar:hover { background-color: #27272a; color: #fff; border-color: #ff2a6d; }
"""

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iasmin - Links Oficiais</title>
    <style>{{ css|safe }}</style>
</head>
<body>
    <div class="container">
        <div class="avatar">I</div>
        <h1>Iasmin</h1>
        <div class="bio">Bem-vindo(a) ao meu portal oficial! Fique por dentro de todas as novidades.</div>
        <div class="section-title">Redes Sociais</div>
        <a href="{{ instagram }}" target="_blank" class="btn btn-social">📸 Instagram Oficial</a>
        <a href="{{ tiktok }}" target="_blank" class="btn btn-social">🎬 TikTok</a>
        <a href="{{ kwai }}" target="_blank" class="btn btn-social">⚡ Kwai</a>
        <div class="divider"></div>
        <a href="/aviso-idade" class="btn btn-adult">🔥 Conteúdos +18 (Privacy & VIP)</a>
    </div>
</body>
</html>
""", css=CSS_RESPONSIVO, instagram=INSTAGRAM_LINK, tiktok=TIKTOK_LINK, kwai=KWAI_LINK)

@app.route("/aviso-idade")
def aviso_idade():
    minutos_bloqueio = verificar_bloqueio()
    if minutos_bloqueio > 0:
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Acesso Restrito</title>
            <style>{{ css|safe }}</style>
        </head>
        <body>
            <div class="container">
                <h2 style="color: #ff2a6d;">⛔ Acesso Temporariamente Indisponível</h2>
                <p>O acesso a esta área foi restrito devido à negação da idade mínima.</p>
                <p>Tente novamente em aproximadamente <b>{{ min }} minuto(s)</b>.</p>
                <div class="nav-footer">
                    <a href="/" class="nav-btn nav-inicio" style="flex: 1;">🏠 Início</a>
                </div>
            </div>
        </body>
        </html>
        """, css=CSS_RESPONSIVO, min=minutos_bloqueio)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verificação de Idade</title>
        <style>{{ css|safe }}</style>
    </head>
    <body>
        <div class="container">
            <h2>⚠️ Conteúdo Restrito (+18)</h2>
            <p>Este ambiente contém material adulto exclusivo para maiores de 18 anos.<br><br>Você confirma que tem 18 anos ou mais?</p>
            <a href="/acesso-autorizado" class="btn">Sim, tenho 18 anos ou mais</a>
            <a href="/bloquear-acesso" class="btn btn-secundario">Não tenho</a>
            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio">🏠 Início</a>
                <a href="/" class="nav-btn nav-voltar">← Voltar</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO)

@app.route("/bloquear-acesso")
def bloquear_acesso():
    ip = request.remote_addr
    ip_blocklist[ip] = time.time() + 300
    return redirect(url_for('aviso_idade'))

@app.route("/acesso-autorizado")
def acesso_autorizado():
    session['maior_idade'] = True
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Iasmin - Conteúdos Exclusivos</title>
        <style>{{ css|safe }}</style>
    </head>
    <body>
        <div class="container">
            <div class="avatar">I</div>
            <h1>Área Exclusiva +18</h1>
            <div class="bio">Escolha abaixo onde deseja acessar os conteúdos da Iasmin:</div>
            <a href="{{ privacy }}" target="_blank" class="btn btn-privacy">💙 Assinar no Privacy</a>
            <a href="{{ previas }}" target="_blank" class="btn btn-telegram">💬 Telegram de Prévias</a>
            <a href="/cadastro-vip" class="btn btn-vip">👑 Grupo VIP Telegram (Pix R$ 1,00)</a>
            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio">🏠 Início</a>
                <a href="/aviso-idade" class="nav-btn nav-voltar">← Voltar</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO, privacy=PRIVACY_LINK, previas=TELEGRAM_PREVIAS_LINK)

@app.route("/cadastro-vip")
def cadastro_vip():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cadastro - Grupo VIP</title>
        <style>{{ css|safe }}</style>
    </head>
    <body>
        <div class="container">
            <h2>👑 Grupo VIP Telegram</h2>
            <p>Preencha seus dados para gerar o Pix instantâneo de <b>R$ 1,00</b>:</p>
            <form action="/criar-pagamento-pix" method="POST">
                <div class="form-group">
                    <label>Seu Nome:</label>
                    <input type="text" name="nome" class="form-control" placeholder="Digite seu nome completo" required>
                </div>
                <div class="form-group">
                    <label>Seu E-mail:</label>
                    <input type="email" name="email" class="form-control" placeholder="seu@email.com" required>
                </div>
                <div class="form-group">
                    <label>Seu WhatsApp (Contato de Segurança):</label>
                    <input type="text" name="whatsapp" class="form-control" placeholder="Ex: 18999999999" required>
                </div>
                <div class="form-group">
                    <label>Seu @ do Telegram:</label>
                    <input type="text" name="telegram" class="form-control" placeholder="Ex: @seuusuario" required>
                </div>
                <button type="submit" class="btn btn-vip" style="margin-top: 15px;">Gerar Pix de R$ 1,00</button>
            </form>
            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio">🏠 Início</a>
                <a href="/acesso-autorizado" class="nav-btn nav-voltar">← Voltar</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO)

@app.route("/criar-pagamento-pix", methods=["POST"])
def criar_pagamento_pix():
    nome = request.form.get("nome")
    email = request.form.get("email")
    whatsapp = request.form.get("whatsapp")
    telegram = request.form.get("telegram")

    enviar_notificacao_telegram(nome, email, whatsapp, telegram)

    payment_data = {
        "transaction_amount": 1.00,
        "description": "Acesso Grupo VIP Telegram - Iasmin",
        "payment_method_id": "pix",
        "payer": {
            "email": email,
            "first_name": nome,
            "identification": {
                "type": "CPF",
                "number": "00000000000"
            }
        }
    }

    try:
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]
        
        payment_id = payment.get("id")
        point_of_interaction = payment.get("point_of_interaction", {})
        transaction_data = point_of_interaction.get("transaction_data", {})
        
        qr_code = transaction_data.get("qr_code", "Erro ao gerar código Pix")
        qr_code_base64 = transaction_data.get("qr_code_base64", "")

        return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pagamento Pix - Grupo VIP</title>
            <style>{{ css|safe }}</style>
        </head>
        <body>
            <div class="container" id="painel-pagamento">
                <h2>⚡ Pix Gerado com Sucesso!</h2>
                <p>Escaneie o QR Code ou copie o código abaixo para pagar <b>R$ 1,00</b>:</p>
                
                {% if qr_base64 %}
                <div style="background: #fff; padding: 12px; border-radius: 12px; display: inline-block; margin-bottom: 15px;">
                    <img src="data:image/png;base64,{{ qr_base64 }}" alt="QR Code Pix" style="width: 180px; height: 180px; display: block;">
                </div>
                {% endif %}

                <div class="form-group">
                    <label>Pix Copia e Cola:</label>
                    <textarea class="form-control" id="pixCode" rows="3" readonly style="resize: none; font-size: 11px;">{{ qr_code }}</textarea>
                </div>

                <button type="button" class="btn btn-vip" onclick="copiarPix()">📋 Copiar Código Pix</button>
                
                <p style="font-size: 11.5px; color: #00e676; margin-top: 15px;" id="status-texto">
                    ⏳ Aguardando confirmação do pagamento em tempo real...
                </p>

                <div class="nav-footer">
                    <a href="/" class="nav-btn nav-inicio" style="flex: 1;">🏠 Voltar ao Início</a>
                </div>
            </div>

            <script>
                function copiarPix() {
                    var copyText = document.getElementById("pixCode");
                    copyText.select();
                    copyText.setSelectionRange(0, 99999);
                    navigator.clipboard.writeText(copyText.value);
                    alert("Código Pix copiado com sucesso!");
                }

                const paymentId = "{{ payment_id }}";
                const linkBot = "{{ link_bot }}";

                const verificarPagamento = setInterval(async () => {
                    try {
                        let response = await fetch(`/checar-status/${paymentId}`);
                        let data = await response.json();

                        if (data.status === "approved") {
                            clearInterval(verificarPagamento);
                            
                            document.getElementById("painel-pagamento").innerHTML = `
                                <div style="font-size: 50px; margin-bottom: 10px;">🎉</div>
                                <h2 style="color: #00e676;">Pagamento Aprovado!</h2>
                                <p style="margin-top: 15px;">Seu pagamento de R$ 1,00 foi confirmado com sucesso.</p>
                                <p style="font-size: 13.5px; color: #a1a1aa; margin-bottom: 20px;">Clique no botão abaixo para abrir o bot e receber seu convite automático:</p>
                                <a href="${linkBot}" target="_blank" class="btn btn-telegram">💬 Abrir Bot e Receber Acesso</a>
                                <div class="nav-footer" style="margin-top: 20px;">
                                    <a href="/" class="nav-btn nav-inicio" style="flex: 1;">🏠 Página Inicial</a>
                                </div>
                            `;
                        }
                    } catch (error) {
                        console.error("Erro ao verificar status:", error);
                    }
                }, 4000);
            </script>
        </body>
        </html>
        """, css=CSS_RESPONSIVO, qr_code=qr_code, qr_base64=qr_code_base64, payment_id=payment_id, link_bot=LINK_DIRETO_BOT)

    except Exception as e:
        return f"Erro ao gerar o Pix via Mercado Pago: {e}"

@app.route("/checar-status/<payment_id>")
def checar_status(payment_id):
    try:
        payment_info = sdk.payment().get(payment_id)
        status = payment_info["response"].get("status")
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    print("🚀 A iniciar servidor web Flask...")
    
    # Inicia o bot do Telegram em segundo plano usando a biblioteca pyTelegramBotAPI
    t_bot = threading.Thread(target=rodar_bot_telegram, daemon=True)
    t_bot.start()
    print("✅ Thread do bot do Telegram iniciada com sucesso!")

    # Roda o site Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
