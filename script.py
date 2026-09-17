import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Credenciais e Configurações
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
TELEGRAM_BOT_TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
LINK_GRUPO_VIP = "https://t.me/+UG_uDePtRW9lOTg5"

SITE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agência Bot - Plataforma Oficial</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            background-color: #0b0b0e; 
            background-image: radial-gradient(circle at 50% 10%, #1a1a24 0%, #0b0b0e 70%);
            color: #f1f1f1; 
            margin: 0; 
            padding: 20px; 
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }

        .container { 
            width: 100%; 
            max-width: 850px; 
            background: rgba(24, 24, 27, 0.92); 
            backdrop-filter: blur(10px);
            padding: 35px; 
            border-radius: 18px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.9); 
            border: 1px solid rgba(255, 255, 255, 0.08); 
            box-sizing: border-box; 
            text-align: center;
        }

        .tela { display: none; }
        .tela.ativa { display: block; }

        .logo-agencia {
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: rgba(255, 255, 255, 0.4);
            font-weight: 700;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 12px;
            display: inline-block;
            width: 100%;
        }
        .logo-agencia span {
            color: #ff2a6d;
            text-shadow: 0 0 10px rgba(255, 42, 109, 0.3);
        }

        h2 { color: #ff2a6d; margin-top: 0; font-size: 26px; letter-spacing: -0.5px; }
        p { color: #a1a1aa; font-size: 15px; line-height: 1.6; margin-bottom: 25px; }

        .btn-opcao { 
            background: #27272a; 
            color: #fff; 
            border: 1px solid #3f3f46; 
            padding: 16px; 
            width: 100%; 
            border-radius: 12px; 
            font-size: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            margin-bottom: 15px; 
            display: block; 
            text-align: center; 
            box-sizing: border-box; 
            text-decoration: none; 
            transition: all 0.2s ease;
        }
        .btn-opcao:hover { background: #3f3f46; border-color: #ff2a6d; transform: translateY(-1px); }
        .btn-destaque { background: #ff2a6d; color: #fff; border: none; box-shadow: 0 4px 15px rgba(255, 42, 109, 0.4); }
        .btn-destaque:hover { background: #e01b5d; }

        .pix-box {
            background: #121215;
            border: 1px solid #27272a;
            padding: 25px;
            border-radius: 14px;
            margin: 20px 0;
        }
        
        .qrcode-img {
            width: 180px;
            height: 180px;
            margin: 0 auto 15px auto;
            border-radius: 10px;
            background: #fff;
            padding: 8px;
            box-sizing: border-box;
            border: 4px solid #ff2a6d;
            display: block;
        }

        .chave-copia {
            background: #18181b;
            border: 1px dashed #52525b;
            color: #f1f1f1;
            padding: 12px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
            margin-bottom: 12px;
            max-height: 80px;
            overflow-y: auto;
        }

        .badge-aviso {
            background: rgba(255, 42, 109, 0.1);
            border: 1px solid rgba(255, 42, 109, 0.3);
            color: #ff2a6d;
            padding: 12px;
            border-radius: 10px;
            font-size: 13px;
            margin-bottom: 20px;
            text-align: left;
        }

        @media (min-width: 768px) {
            .container { padding: 45px; }
        }
    </style>
</head>
<body>

    <!-- TELA 1: Verificação de Maioridade (+18) -->
    <div id="tela-idade" class="container tela ativa">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>⚠️ Acesso Restrito (+18)</h2>
        <p>Este espaço contém material adulto exclusivo. Para continuar e acessar o conteúdo, você deve confirmar que tem 18 anos ou mais.</p>
        
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-home')">Sim, tenho 18 anos ou mais</button>
        <button class="btn-opcao" onclick="alert('Acesso negado. É necessário ter mais de 18 anos.')" style="background:transparent; border-color:#333; color:#71717a;">Não tenho</button>
    </div>

    <!-- TELA 2: Vitrine do Grupo VIP -->
    <div id="tela-home" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>🔥 Grupo VIP Exclusivo</h2>
        <p>Tenha acesso direto ao nosso canal fechado com atualizações diárias e conteúdo sem censura.</p>

        <div class="badge-aviso">
            💡 <b>Modo de Teste:</b> Gere seu Pix de teste. Assim que o Mercado Pago reconhecer o pagamento de R$ 1,00, o seu acesso será liberado instantaneamente.
        </div>

        <div style="font-size: 28px; font-weight: bold; color: #00e676; margin-bottom: 25px;">
            R$ 1,00 <span style="font-size: 13px; color: #a1a1aa; font-weight: normal;">/ teste de acesso</span>
        </div>

        <button class="btn-opcao btn-destaque" onclick="gerarPagamentoPix()">Gerar Pix de R$ 1,00</button>
    </div>

    <!-- TELA 3: Pagamento (QR Code Real + Copia e Cola gerado pelo MP) -->
    <div id="tela-pagamento" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>💳 Reconhecimento Bancário</h2>
        <p>Escaneie o QR Code abaixo ou utilize a chave Pix Copia e Cola para realizar o teste de validação.</p>

        <div class="pix-box">
            <img id="qrCodeImg" class="qrcode-img" src="" alt="QR Code Pix">
            
            <div class="chave-copia" id="textoChavePix">Gerando chave Pix...</div>
            <button class="btn-opcao" style="padding: 10px; font-size: 13px; margin-bottom: 0;" onclick="copiarChavePix()">📋 Copiar Chave Pix</button>
        </div>

        <p id="statusPagamento" style="font-size: 13px; color: #ff2a6d; margin-top: 15px;">⏳ Aguardando o reconhecimento do pagamento...</p>
        <button class="btn-opcao" style="background: transparent; border: none; color: #a1a1aa; margin-top: 10px;" onclick="mostrarTela('tela-home')">⬅ Cancelar / Voltar</button>
    </div>

    <!-- TELA 4: Sucesso - Link Direto Fixo -->
    <div id="tela-sucesso" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>🎉 Pagamento Aprovado!</h2>
        <p>Identificamos a transação com sucesso através do Mercado Pago. Clique no botão abaixo para entrar no grupo:</p>

        <a href="https://t.me/+UG_uDePtRW9lOTg5" target="_blank" class="btn-opcao btn-destaque" style="font-size: 18px; padding: 20px; margin-top: 20px; display: block; text-decoration: none;">
            🚀 Entrar no Grupo do Telegram Agora
        </a>
        <p style="font-size: 12px; color: #71717a; margin-top: 15px;">Seu acesso é vitalício e exclusivo.</p>
    </div>

    <script>
        let paymentId = null;
        let checkInterval = null;

        function mostrarTela(idTela) {
            document.querySelectorAll('.tela').forEach(el => el.classList.remove('ativa'));
            document.getElementById(idTela).classList.add('ativa');
            window.scrollTo(0, 0);
        }

        function copiarChavePix() {
            let texto = document.getElementById('textoChavePix').innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert('Chave Pix copiada com sucesso!');
            }).catch(err => {
                alert('Erro ao copiar chave.');
            });
        }

        async function gerarPagamentoPix() {
            mostrarTela('tela-pagamento');
            document.getElementById('textoChavePix').innerText = "Gerando Pix exclusivo de teste...";
            
            try {
                let response = await fetch('/criar-pagamento', { method: 'POST' });
                let data = await response.json();

                if (data.error) {
                    alert('Erro ao gerar pagamento: ' + data.error);
                    mostrarTela('tela-home');
                    return;
                }

                paymentId = data.id;
                document.getElementById('textoChavePix').innerText = data.qr_code;
                document.getElementById('qrCodeImg').src = 'data:image/png;base64,' + data.qr_code_base64;

                // Inicia verificação automática a cada 4 segundos
                checkInterval = setInterval(verificarStatusPagamento, 4000);

            } catch (err) {
                alert('Erro de conexão com o servidor.');
                mostrarTela('tela-home');
            }
        }

        async function verificarStatusPagamento() {
            if (!paymentId) return;

            try {
                let response = await fetch(`/verificar-pagamento/${paymentId}`);
                let data = await response.json();

                if (data.status === 'approved') {
                    clearInterval(checkInterval);
                    mostrarTela('tela-sucesso');
                }
            } catch (err) {
                console.log('Verificando status...');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(SITE_HTML)

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
        "description": "Teste de Reconhecimento - Agência Bot",
        "payment_method_id": "pix",
        "payer": {
            "email": "teste@agenciabot.com"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    res_data = response.json()

    if response.status_code != 201 and response.status_code != 200:
        return jsonify({"error": res_data.get("message", "Erro desconhecido no Mercado Pago")}), 400

    point_of_interaction = res_data.get("point_of_interaction", {})
    transaction_data = point_of_interaction.get("transaction_data", {})

    qr_code = transaction_data.get("qr_code")
    qr_code_base64 = transaction_data.get("qr_code_base64")
    payment_id = res_data.get("id")

    return jsonify({
        "id": payment_id,
        "qr_code": qr_code,
        "qr_code_base64": qr_code_base64
    })

@app.route('/verificar-pagamento/<int:payment_id>', methods=['GET'])
def verificar_pagamento(payment_id):
    url = f"https://api.mercadopago.com/v1/payments/{payment_id}"
    headers = {
        "Authorization": f"Bearer {MP_ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return jsonify({"status": "pending"})

    res_data = response.json()
    status = res_data.get("status") # 'approved', 'pending', etc.

    return jsonify({
        "status": status,
        "link_grupo": LINK_GRUPO_VIP
    })

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
