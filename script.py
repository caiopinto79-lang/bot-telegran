import os
import time
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24) # Necessário para controlar sessões de segurança

# Links reais das redes sociais da Iasmin
INSTAGRAM_LINK = "https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj"
TIKTOK_LINK = "https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE"
KWAI_LINK = "https://k.kwai.com/u/@mc.iasmin_ofc/xM6daWCD"

# Links das plataformas +18 (substitua pelos links reais quando tiver)
PRIVACY_LINK = "#"
TELEGRAM_PREVIAS_LINK = "#"
TELEGRAM_VIP_LINK = "#"

# Dicionário temporário para controle de bloqueio por IP (armazena o timestamp de liberação)
ip_blocklist = {}

def verificar_bloqueio():
    ip = request.remote_addr
    if ip in ip_blocklist:
        tempo_restante = ip_blocklist[ip] - time.time()
        if tempo_restante > 0:
            return int(tempo_restante / 60) + 1 # Retorna os minutos restantes
        else:
            del ip_blocklist[ip] # Expirou o tempo, remove da lista
    return 0

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
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: rgba(24, 24, 27, 0.95); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
        
        .avatar { width: 90px; height: 90px; border-radius: 50%; background: #ff2a6d; margin: 0 auto 15px auto; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: bold; color: #fff; border: 3px solid rgba(255,42,109,0.4); }
        h1 { color: #fff; font-size: 22px; margin-bottom: 5px; }
        .bio { font-size: 13px; color: #a1a1aa; margin-bottom: 25px; }
        
        .btn { background-color: #ff2a6d; color: white; border: none; padding: 14px 20px; border-radius: 12px; font-size: 15px; cursor: pointer; width: 100%; font-weight: bold; transition: all 0.2s; margin-top: 12px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 15px rgba(255,42,109,0.3); }
        .btn:hover { background-color: #e01b5d; transform: translateY(-2px); }
        
        .btn-social { background-color: #18181b; border: 1px solid #27272a; color: #f1f1f1; }
        .btn-social:hover { background-color: #27272a; border-color: #ff2a6d; }
        
        .btn-adult { background: linear-gradient(135deg, #ff2a6d, #9d4edd); box-shadow: 0 4px 15px rgba(157,78,221,0.4); }
        .btn-adult:hover { opacity: 0.9; }
        
        .divider { height: 1px; background: rgba(255,255,255,0.08); margin: 25px 0; }
        .section-title { font-size: 14px; color: #a1a1aa; margin-bottom: 10px; text-align: left; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    </style>
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

        <div class="section-title">Conteúdos Exclusivos</div>
        <a href="/aviso-idade" class="btn btn-adult">🔥 Conteúdos +18 (Privacy & VIP)</a>
    </div>
</body>
</html>
""", instagram=INSTAGRAM_LINK, tiktok=TIKTOK_LINK, kwai=KWAI_LINK)

# --- PÁGINA 2: AVISO DE MAIORIDADE (IDADE) ---
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
            <style>
                * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
                .container { background: rgba(24, 24, 27, 0.95); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
                h2 { color: #ff2a6d; margin-bottom: 15px; font-size: 22px; }
                p { font-size: 14px; color: #a1a1aa; margin-bottom: 20px; line-height: 1.5; }
                .btn { background-color: #27272a; color: white; border: 1px solid #3f3f46; padding: 12px 20px; border-radius: 12px; font-size: 14px; cursor: pointer; width: 100%; text-decoration: none; display: inline-block; font-weight: bold; }
                .btn:hover { background-color: #3f3f46; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>⛔ Acesso Temporariamente Indisponível</h2>
                <p>O acesso a esta área foi restrito para este dispositivo devido à negação da idade mínima.</p>
                <p>Tente novamente em aproximadamente <b>{{ min }} minuto(s)</b>.</p>
                <a href="/" class="btn">Voltar para a Página Inicial</a>
            </div>
        </body>
        </html>
        """, min=minutos_bloqueio)

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verificação de Idade</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
            .container { background: rgba(24, 24, 27, 0.95); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
            h2 { color: #ff2a6d; margin-bottom: 15px; font-size: 22px; }
            p { font-size: 14px; color: #a1a1aa; margin-bottom: 25px; line-height: 1.5; }
            .btn { background-color: #ff2a6d; color: white; border: none; padding: 14px 20px; border-radius: 12px; font-size: 15px; cursor: pointer; width: 100%; font-weight: bold; transition: all 0.2s; margin-top: 12px; text-decoration: none; display: inline-block; box-shadow: 0 4px 15px rgba(255,42,109,0.3); }
            .btn:hover { background-color: #e01b5d; }
            .btn-secundario { background-color: #27272a; border: 1px solid #3f3f46; color: #fff; box-shadow: none; }
            .btn-secundario:hover { background-color: #3f3f46; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⚠️ Conteúdo Restrito (+18)</h2>
            <p>Este ambiente contém material adulto exclusivo para maiores de 18 anos.<br><br>Você confirma que tem 18 anos ou mais?</p>
            <a href="/acesso-autorizado" class="btn">Sim, tenho 18 anos ou mais</a>
            <a href="/bloquear-acesso" class="btn btn-secundario">Não tenho</a>
        </div>
    </body>
    </html>
    """)

# --- ROTA: BLOQUEIO DE IP (5 MINUTOS) ---
@app.route("/bloquear-acesso")
def bloquear_acesso():
    ip = request.remote_addr
    # Bloqueia o IP por 300 segundos (5 minutos)
    ip_blocklist[ip] = time.time() + 300
    return redirect(url_for('aviso_idade'))

# --- ROTA: ACESSO AUTORIZADO ÀS PLATAFORMAS ---
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
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
            .container { background: rgba(24, 24, 27, 0.95); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
            
            .avatar { width: 80px; height: 80px; border-radius: 50%; background: #ff2a6d; margin: 0 auto 15px auto; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: bold; color: #fff; border: 3px solid rgba(255,42,109,0.4); }
            h1 { color: #fff; font-size: 20px; margin-bottom: 5px; }
            .bio { font-size: 13px; color: #a1a1aa; margin-bottom: 25px; }
            
            .btn { background-color: #ff2a6d; color: white; border: none; padding: 14px 20px; border-radius: 12px; font-size: 15px; cursor: pointer; width: 100%; font-weight: bold; transition: all 0.2s; margin-top: 12px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 15px rgba(255,42,109,0.3); }
            .btn:hover { background-color: #e01b5d; transform: translateY(-2px); }
            
            .btn-privacy { background-color: #00aff0; box-shadow: 0 4px 15px rgba(0,175,240,0.3); }
            .btn-privacy:hover { background-color: #0091d0; }
            
            .btn-telegram { background-color: #229ed9; box-shadow: 0 4px 15px rgba(34,158,217,0.3); }
            .btn-telegram:hover { background-color: #1b85b8; }
            
            .btn-vip { background-color: #00e676; color: #000; box-shadow: 0 4px 15px rgba(0,230,118,0.3); }
            .btn-vip:hover { background-color: #00c853; }
            
            .back-link { display: inline-block; margin-top: 20px; font-size: 13px; color: #a1a1aa; text-decoration: none; }
            .back-link:hover { color: #fff; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="avatar">I</div>
            <h1>Área Exclusiva +18</h1>
            <div class="bio">Escolha abaixo onde deseja acessar os conteúdos da Iasmin:</div>

            <a href="{{ privacy }}" target="_blank" class="btn btn-privacy">💙 Assinar no Privacy</a>
            <a href="{{ previas }}" target="_blank" class="btn btn-telegram">💬 Telegram de Prévias</a>
            <a href="{{ vip }}" target="_blank" class="btn btn-vip">👑 Canal VIP Telegram</a>

            <br>
            <a href="/" class="back-link">← Voltar para a página inicial</a>
        </div>
    </body>
    </html>
    """, privacy=PRIVACY_LINK, previas=TELEGRAM_PREVIAS_LINK, vip=TELEGRAM_VIP_LINK)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
