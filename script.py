import os
import time
import sqlite3
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Credenciais oficiais
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
TELEGRAM_BOT_TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_CHAT_ID = "-1002130298013"

# Cole aqui o link oficial e permanente do seu grupo do Telegram
LINK_GRUPO_OFICIAL = "https://t.me/+SEU_LINK_DO_GRUPO_AQUI"

DB_NAME = "agencia_bot.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT UNIQUE,
            link_convite TEXT,
            status TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agência Bot - Acesso Exclusivo</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: rgba(24, 24, 27, 0.95); padding: 35px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
        h2 { color: #ff2a6d; margin-bottom: 15px; font-size: 24px; }
        p { font-size: 14px; color: #a1a1aa; margin-bottom: 20px; line-height: 1.5; }
        .btn { background-color: #ff2a6d; color: white; border: none; padding: 14px 20px; border-radius: 10px; font-size: 16px; cursor: pointer; width: 100%; font-weight: bold; transition: background 0.2s; margin-top: 10px; text-decoration: none; display: inline-block; }
        .btn:hover { background-color: #e01b5d; }
        .btn-secundario { background-color: #27272a; border: 1px solid #3f3f46; color: #fff; }
        .btn-secundario:hover { background-color: #3f3f46; }
        .hidden { display: none; }
        
        .pix-box { background: #121215; padding: 20px; border-radius: 12px; border: 1px solid #27272a; margin-top: 15px; text-align: left; }
        .qrcode-img { width: 160px; height: 160px; margin: 0 auto 15px auto; border-radius: 8px; background: #fff; padding: 6px; display: block; border: 3px solid #ff2a6d; }
        .chave-copia { background: #18181b; border: 1px dashed #52525b; color: #f1f1f1; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px; word-break: break-all; margin-bottom: 10px; max-height: 70px; overflow-y: auto; }
        
        .status-aguardando { color: #ff2a6d; font-weight: bold; font-size: 13px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Etapa 1: Verificação de Idade -->
        <div id="step-age">
            <h2>⚠️ Acesso Restrito (+18)</h2>
            <p>Este espaço contém material exclusivo. Confirma que você tem 18 anos ou mais para prosseguir?</p>
            <button class="btn" onclick="goToPix()">Sim, tenho 18 anos ou mais</button>
            <button class="btn btn-secundario" onclick="alert('Acesso negado.');">Não tenho</button>
        </div>

        <!-- Etapa 2: Vitrine e Geração do Pix -->
        <div id="step-pix-init" class="hidden">
            <h2>🔥 Grupo VIP Exclusivo</h2>
            <p>Tenha acesso completo ao nosso canal fechado por 30 dias com atualizações diárias.</p>
            <div style="font-size: 24px; font-weight: bold; color: #00e676; margin-bottom: 20px;">R$ 1,00 <span style="font-size: 12px; color: #a1a1aa; font-weight: normal;">/ teste de acesso</span></div>
            <button class="btn" onclick="gerarPagamentoPix()">Gerar Pix de R$ 1,00</button>
        </div>

        <!-- Etapa 3: Exibição do QR Code e Pix Copia e Cola -->
        <div id="step-pagamento" class="hidden">
            <h2>💳 Pagamento Pix</h2>
            <p>Escaneie o QR Code ou copie a chave abaixo para liberar o acesso instantaneamente:</p>
            
            <div class="pix-box">
                <img id="qrCodeImg" class="qrcode-img" src="" alt="QR Code Pix">
                <div class="chave-copia" id="textoChavePix">Carregando chave...</div>
                <button class="btn btn-secundario" style="padding: 8px; font-size: 12px; margin: 0;" onclick="copiarChave()">📋 Copiar Pix Copia e Cola</button>
            </div>

            <p id="statusPagamento" class="status-aguardando">⏳ Aguardando a aprovação do pagamento...</p>
        </div>

        <!-- Etapa 4: Sucesso -->
        <div id="step-success" class="hidden">
            <h2>🎉 Pagamento Aprovado!</h2>
            <p>O seu pagamento foi confirmado com sucesso. Clique abaixo para entrar no grupo:</p>
            <a id="linkTelegram" href="" target="_blank" class="btn">🚀 Entrar no Grupo do Telegram Agora</a>
            <p style="font-size: 11px; color: #71717a; margin-top: 15px;">⚠️ Aproveite agora. Ao fechar esta página, o acesso expira.</p>
        </div>
    </div>

    <script>
        let paymentId = null;
        let checkInterval = null;

        function goToPix() {
            document.getElementById('step-age').classList.add('hidden');
            document.getElementById('step-pix-init').classList.remove('hidden');
        }

        function copiarChave() {
            let texto = document.getElementById('textoChavePix').innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert('Chave Pix copiada com sucesso!');
            });
        }

        async function gerarPagamentoPix() {
            document.getElementById('step-pix-init').classList.add('hidden');
            document.getElementById('step-pagamento').classList.remove('hidden');
            
            try {
                let response = await fetch('/criar-pagamento', { method: 'POST' });
                let data = await response.json();

                if (data.error) {
                    alert('Erro: ' + data.error);
                    location.reload();
                    return;
                }

                paymentId = data.id;
                document.getElementById('textoChavePix').innerText = data.qr_code;
                document.getElementById('qrCodeImg').src = 'data:image/png;base64,' + data.qr_code_base64;

                checkInterval = setInterval(verificarStatus, 4000);
            } catch (err) {
                alert('Erro de conexão ao gerar o Pix.');
                location.reload();
            }
        }

        async function verificarStatus() {
            if (!paymentId) return;

            try {
                let response = await fetch(`/verificar-pagamento/${paymentId}`);
                let data = await response.json();

                if (data.status === 'approved') {
                    clearInterval(checkInterval);
                    document.getElementById('linkTelegram').href = data.link_grupo;
                    document.getElementById('step-pagamento').classList.add('hidden');
                    document.getElementById('step-success').classList.remove('hidden');
                }
            } catch (err) {
                console.log('Verificando...');
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/criar-pagamento', methods=['POST'])
def criar_pagamento():
    url = "https://api.mercadopago.com/v1/payments"
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
        "X-Idempotency-Key": os.urandom(16).hex()
    }
    
    payload = {
        "transaction_amount": 1.00,
        "description": "Acesso VIP - 30 Dias",
        "payment_method_id": "pix",
        "payer": {
            "email": "cliente@agenciabot.com"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()

    if response.status_code not in [200, 201]:
        return jsonify({"error": res_data.get("message", "Erro ao conectar com o Mercado Pago")}), 400

    point_of_interaction = res_data.get("point_of_interaction", {})
    transaction_data = point_of_interaction.get("transaction_data", {})

    return jsonify({
        "id": res_data.get("id"),
        "qr_code": transaction_data.get("qr_code"),
        "qr_code_base64": transaction_data.get("qr_code_base64")
    })

@app.route('/verificar-pagamento/<int:payment_id>', methods=['GET'])
def verificar_pagamento(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {"Authorization": f"Bearer {MP_ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"status": "pending"})

    res_data = response.json()
    status = res_data.get("status")
    
    link_convite = LINK_GRUPO_OFICIAL if status == 'approved' else ""

    return jsonify({
        "status": status,
        "link_grupo": link_convite
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
