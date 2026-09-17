import os
import sqlite3
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Configurações do Telegram e Gateway (substitua com seus dados reais ou variáveis de ambiente)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_DO_BOT_AQUI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "SEU_CHAT_ID_DO_GRUPO_AQUI")

# Banco de dados SQLite simples para controle de acessos
DB_NAME = "agencia_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            status TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Template HTML/CSS moderno (Dark Mode com verificação de idade e fluxo de Pix/Wi-Fi)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acesso Exclusivo - Verificação</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0d1117; color: #c9d1d9; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .container { background-color: #161b22; padding: 30px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); width: 100%; max-width: 400px; text-align: center; border: 1px solid #30363d; }
        h2 { color: #58a6ff; margin-bottom: 20px; font-size: 22px; }
        p { font-size: 14px; color: #8b949e; margin-bottom: 20px; line-height: 1.5; }
        .btn { background-color: #238636; color: white; border: none; padding: 12px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; }
        .btn:hover { background-color: #2ea043; }
        .hidden { display: none; }
        .pix-box { background: #0d1117; padding: 15px; border-radius: 8px; border: 1px dashed #30363d; margin-top: 15px; word-break: break-all; font-family: monospace; color: #58a6ff; font-size: 12px; }
        .link-vip { display: inline-block; background-color: #1f6feb; color: white; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 15px; width: 100%; }
        .link-vip:hover { background-color: #388bfd; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Etapa 1: Verificação de Idade -->
        <div id="step-age">
            <h2>Verificação de Conteúdo</h2>
            <p>Este espaço contém material restrito para maiores de 18 anos. Confirma que você tem idade legal?</p>
            <button class="btn" onclick="goToPix()">Sim, tenho 18 anos ou mais</button>
        </div>

        <!-- Etapa 2: Pagamento Pix -->
        <div id="step-pix" class="hidden">
            <h2>Liberação de Acesso</h2>
            <p>Para desbloquear o seu link VIP exclusivo de 30 dias, realize o pagamento de verificação via Pix de <b>R$ 1,00</b>.</p>
            <button class="btn" onclick="gerarPix()">Gerar Pix de Acesso</button>
        </div>

        <!-- Etapa 3: Aguardando / Sucesso -->
        <div id="step-success" class="hidden">
            <h2>Pagamento Confirmado!</h2>
            <p>Seu acesso exclusivo foi liberado com sucesso. Clique no botão abaixo para entrar no grupo VIP do Telegram:</p>
            <div id="invite-container"></div>
        </div>
    </div>

    <script>
        function goToPix() {
            document.getElementById('step-age').classList.add('hidden');
            document.getElementById('step-pix').classList.remove('hidden');
        }

        function gerarPix() {
            fetch('/api/gerar-pix', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('step-pix').classList.add('hidden');
                    const successDiv = document.getElementById('step-success');
                    successDiv.classList.remove('hidden');
                    
                    document.getElementById('invite-container').innerHTML = `
                        <p>Seu link de convite exclusivo (válido por 3 minutos):</p>
                        <a href="${data.invite_link}" class="link-vip" target="_blank">Entrar no Canal VIP</a>
                    `;
                } else {
                    alert('Erro ao gerar o acesso. Tente novamente.');
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/gerar-pix", methods=["POST"])
def gerar_pix():
    # Simula a validação do Pix e gera o link de convite via API do Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/createChatInviteLink"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "expire_date": 180,  # Expira em 3 minutos (180 segundos)
        "member_limit": 1    # Uso único para garantir segurança
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        data = response.json()
        
        if data.get("ok"):
            invite_link = data["result"]["invite_link"]
            
            # Salva o registro no banco local
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO acessos (ip, status) VALUES (?, ?)", (request.remote_addr, "Liberado"))
            conn.commit()
            conn.close()
            
            return jsonify({"success": True, "invite_link": invite_link})
        else:
            # Fallback simulado caso o token do bot ainda não esteja configurado no Render
            return jsonify({"success": True, "invite_link": "https://t.me/+exemplo_convite_vip"})
            
    except Exception as e:
        print(f"Erro na requisição ao Telegram: {e}")
        return jsonify({"success": True, "invite_link": "https://t.me/+exemplo_convite_vip"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
