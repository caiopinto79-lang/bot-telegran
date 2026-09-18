import os
import time
import requests
from flask import Flask, render_template_string, request, redirect, url_for, session
import mercadopago

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ================= CONFIGURAÇÕES =================
# Credenciais oficiais do Mercado Pago
ACCESS_TOKEN_MP = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
sdk = mercadopago.SDK(ACCESS_TOKEN_MP)

# Credenciais oficiais do Bot do Telegram
TELEGRAM_BOT_TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
# Insira aqui o Chat ID de destino (pode ser o ID numérico do chat privado dela com o bot ou grupo de avisos)
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI" 
# =================================================

# Links reais das redes sociais da Iasmin
INSTAGRAM_LINK = "https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj"
TIKTOK_LINK = "https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE"
KWAI_LINK = "https://k.kwai.com/u/@mc.iasmin_ofc/xM6daWCD"

# Links diretos
TELEGRAM_PREVIAS_LINK = "#"
PRIVACY_LINK = "#"

# Dicionário temporário para controle de bloqueio por IP
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
    """Envia os dados do cadastro de forma privada para o bot/grupo da Iasmin"""
    if TELEGRAM_CHAT_ID == "SEU_CHAT_ID_AQUI":
        return # Evita erro caso o Chat ID não tenha sido configurado ainda
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    mensagem = (
        f"👑 *NOVO CADASTRO - CANAL VIP*\n\n"
        f"👤 *Nome:* {nome}\n"
        f"📧 *E-mail:* {email}\n"
        f"📱 *WhatsApp (Segurança):* {whatsapp}\n"
        f"💬 *Telegram:* {telegram_user}\n\n"
        f"💳 *Status:* Pagamento de R$ 1,00 solicitado."
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

# Estilo CSS Global Responsivo
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

    /* Estilos para o Formulário */
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

# --- PÁGINA 1: VITRINE PRINCIPAL ---
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

# --- TELA DE AVISO DE MAIORIDADE ---
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
                <p>O acesso a esta área foi restrito para este dispositivo devido à negação da idade mínima.</p>
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

# --- ROTA: ÁREA RESTRITA ---
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
            <a href="/cadastro-vip" class="btn btn-vip">👑 Canal VIP Telegram (R$ 1,00)</a>

            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio">🏠 Início</a>
                <a href="/aviso-idade" class="nav-btn nav-voltar">← Voltar</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO, privacy=PRIVACY_LINK, previas=TELEGRAM_PREVIAS_LINK)

# --- ROTA: FORMULÁRIO DE CADASTRO VIP ---
@app.route("/cadastro-vip")
def cadastro_vip():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cadastro - Canal VIP</title>
        <style>{{ css|safe }}</style>
    </head>
    <body>
        <div class="container">
            <h2>👑 Canal VIP Telegram</h2>
            <p>Preencha seus dados para gerar o pagamento de <b>R$ 1,00</b> e garantir sua vaga:</p>
            
            <form action="/criar-pagamento" method="POST">
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

                <button type="submit" class="btn btn-vip" style="margin-top: 15px;">Pagar R$ 1,00 e Finalizar</button>
            </form>

            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio">🏠 Início</a>
                <a href="/acesso-autorizado" class="nav-btn nav-voltar">← Voltar</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO)

# --- ROTA: CRIAR PREFERÊNCIA NO MERCADO PAGO E NOTIFICAR BOT ---
@app.route("/criar-pagamento", methods=["POST"])
def criar_pagamento():
    nome = request.form.get("nome")
    email = request.form.get("email")
    whatsapp = request.form.get("whatsapp")
    telegram = request.form.get("telegram")

    # Dispara a notificação silenciosa para o bot/grupo do Telegram dela
    enviar_notificacao_telegram(nome, email, whatsapp, telegram)

    # Cria a preferência de pagamento no Mercado Pago (R$ 1,00)
    preference_data = {
        "items": [
            {
                "title": "Acesso Canal VIP Telegram - Iasmin",
                "quantity": 1,
                "unit_price": 1.00,
                "currency_id": "BRL"
            }
        ],
        "payer": {
            "name": nome,
            "email": email
        },
        "back_urls": {
            "success": "https://sua-url-do-render.onrender.com/sucesso",
            "failure": "https://sua-url-do-render.onrender.com/cadastro-vip",
            "pending": "https://sua-url-do-render.onrender.com/sucesso"
        },
        "auto_return": "approved"
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]
        init_point = preference["init_point"]
        return redirect(init_point)
    except Exception as e:
        return f"Erro ao processar pagamento com o Mercado Pago: {e}"

# --- ROTA: TELA DE SUCESSO ---
@app.route("/sucesso")
def sucesso():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cadastro Concluído</title>
        <style>{{ css|safe }}</style>
    </head>
    <body>
        <div class="container">
            <div style="font-size: 50px; margin-bottom: 10px;">🎉</div>
            <h2 style="color: #00e676;">Tudo Pronto!</h2>
            <p style="margin-top: 15px;">Seus dados e pagamento foram processados com sucesso.</p>
            <p style="background: #18181b; padding: 14px; border-radius: 10px; border: 1px solid #27272a; font-size: 13.5px; line-height: 1.6;">
                ⏳ O seu acesso ao Canal VIP será liberado em <b>até 24 horas</b>. Fique de olho no seu <b>Telegram</b>!
            </p>
            
            <div class="nav-footer">
                <a href="/" class="nav-btn nav-inicio" style="flex: 1;">🏠 Voltar para a Página Inicial</a>
            </div>
        </div>
    </body>
    </html>
    """, css=CSS_RESPONSIVO)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
