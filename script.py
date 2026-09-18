import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Credenciais do Mercado Pago configuradas via variáveis de ambiente no Render
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_DO_MERCADO_PAGO")
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# PÁGINA 1: Início (Redes Sociais + Botão +18 com Alerta de Maioridade funcional corrigido)
HTML_INDEX = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iasmin - Links Oficiais</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #f43f5e;
            --accent-hover: #e11d48;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
        }
        h1 {
            font-size: 26px;
            margin-bottom: 5px;
            color: var(--accent);
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 25px;
        }
        .section-title {
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 20px 0 10px 0;
            text-align: left;
            border-bottom: 1px solid #334155;
            padding-bottom: 5px;
        }
        .link-button {
            display: block;
            width: 100%;
            padding: 14px;
            margin-bottom: 12px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 15px;
            box-sizing: border-box;
            transition: opacity 0.3s, transform 0.2s;
            cursor: pointer;
            border: none;
            text-align: center;
        }
        .link-button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }
        .btn-instagram { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .btn-tiktok { background-color: #010101; border: 1px solid #333; }
        .btn-kwai { background-color: #ff5722; }
        .btn-adult-main { background-color: var(--accent); font-size: 16px; margin-top: 15px; width: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Iasmin</h1>
        <p class="subtitle">Acesse minhas redes abaixo</p>

        <div class="section-title">Redes Sociais</div>
        <a href="https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj" target="_blank" class="link-button btn-instagram">📸 Instagram Oficial</a>
        <a href="https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE" target="_blank" class="link-button btn-tiktok">🎵 TikTok</a>
        <a href="https://kwai.com" target="_blank" class="link-button btn-kwai">⚡ Kwai</a>

        <!-- Botão corrigido usando elemento <button> nativo para garantir clique e funcionamento -->
        <button type="button" class="link-button btn-adult-main" onclick="verificarIdade()">🔥 CONTEÚDO +18</button>
    </div>

    <script>
        function verificarIdade() {
            const maior = confirm("Atenção: Este site contém material adulto (+18).\n\nVocê confirma que tem 18 anos ou mais e deseja continuar?");
            if (maior) {
                window.location.href = "/conteudos";
            }
        }
    </script>
</body>
</html>
"""

# PÁGINA 2: Conteúdos Exclusivos (Sequência: Privacy, Prévias, VIP)
HTML_CONTEUDOS = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iasmin - Conteúdos Exclusivos</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #f43f5e;
            --accent-hover: #e11d48;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
        }
        h1 {
            font-size: 26px;
            margin-bottom: 5px;
            color: var(--accent);
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 25px;
        }
        .link-button {
            display: block;
            width: 100%;
            padding: 14px;
            margin-bottom: 12px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 15px;
            box-sizing: border-box;
            transition: opacity 0.3s, transform 0.2s;
            cursor: pointer;
            border: none;
        }
        .link-button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }
        .btn-privacy { background-color: #00aff0; }
        .btn-preview { background-color: #229ED9; }
        .btn-vip { background-color: #10b981; }
        .btn-voltar { background-color: #475569; font-size: 13px; padding: 10px; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Iasmin</h1>
        <p class="subtitle">Área restrita - Conteúdos Exclusivos</p>

        <a href="https://privacy.com.br/SEU_LINK" target="_blank" class="link-button btn-privacy">💎 Privacy / Plataformas</a>
        <a href="https://t.me/SEU_GRUPO_PREVIAS" target="_blank" class="link-button btn-preview">💬 Canal de Prévias (Grátis)</a>
        <a href="/checkout-vip" class="link-button btn-vip">🚀 Canal VIP Telegram (R$ 29,90)</a>

        <a href="/" class="link-button btn-voltar">⬅ Voltar ao Início</a>
    </div>
</body>
</html>
"""

# PÁGINA 3: Tela de Pagamento do Canal VIP (Pix)
HTML_CHECKOUT = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iasmin - Canal VIP</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #f43f5e;
            --accent-hover: #e11d48;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #34d399;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 14px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.6);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 5px;
            color: var(--accent);
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 20px;
        }
        .vip-box {
            background: rgba(244, 63, 94, 0.08);
            border: 1px dashed var(--accent);
            border-radius: 10px;
            padding: 15px;
            text-align: left;
        }
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 6px;
            border: 1px solid #334155;
            background: var(--bg-color);
            color: #fff;
            box-sizing: border-box;
            font-size: 14px;
        }
        button.action-btn {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            font-size: 15px;
            transition: background 0.3s;
        }
        button.action-btn:hover { background-color: var(--accent-hover); }
        #resultado-pix {
            margin-top: 15px;
            display: none;
        }
        textarea {
            width: 100%;
            height: 75px;
            background: var(--bg-color);
            color: var(--success);
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 8px;
            font-size: 11px;
            resize: none;
            box-sizing: border-box;
            margin-bottom: 8px;
        }
        .link-button {
            display: block;
            width: 100%;
            padding: 10px;
            margin-top: 15px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 13px;
            box-sizing: border-box;
            text-align: center;
            border: none;
            cursor: pointer;
        }
        .btn-voltar { background-color: #475569; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Canal VIP Telegram</h1>
        <p class="subtitle">Liberação automática após o pagamento (R$ 29,90)</p>

        <div class="vip-box">
            <div id="form-pagamento">
                <input type="text" id="nome" placeholder="Seu Nome Completo" required>
                <input type="email" id="email" placeholder="Seu E-mail" required>
                <button class="action-btn" onclick="gerarPix()">Gerar Pix</button>
            </div>

            <div id="resultado-pix">
                <p style="color: var(--success); font-weight: bold; font-size: 12px; margin-bottom: 4px;">Pix Gerado com Sucesso!</p>
                <textarea id="copia-cola" readonly></textarea>
                <button onclick="copiarPix()" class="action-btn" style="background-color: #10b981; padding: 10px; font-size: 13px;">Copiar Código Pix</button>
            </div>
        </div>

        <a href="/conteudos" class="link-button btn-voltar">⬅ Voltar aos Conteúdos</a>
    </div>

    <script>
        async function gerarPix() {
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;

            if(!nome || !email) {
                alert('Por favor, preencha o nome e o e-mail.');
                return;
            }

            const btn = document.querySelector('#form-pagamento button');
            btn.innerText = "Gerando Pix...";
            btn.disabled = true;

            try {
                const response = await fetch('/criar_pagamento', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ nome, email, valor: 29.90 })
                });

                const data = await response.json();
                if(data.status === 'sucesso') {
                    document.getElementById('form-pagamento').style.display = 'none';
                    document.getElementById('copia-cola').value = data.qr_code;
                    document.getElementById('resultado-pix').style.display = 'block';
                } else {
                    alert('Erro ao gerar pagamento: ' + data.detalhes);
                    btn.innerText = "Gerar Pix";
                    btn.disabled = false;
                }
            } catch (error) {
                alert('Erro de conexão. Tente novamente.');
                btn.innerText = "Gerar Pix";
                btn.disabled = false;
            }
        }

        function copiarPix() {
            const copyText = document.getElementById("copia-cola");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(copyText.value);
            alert("Código Pix copiado com sucesso!");
        }
    </script>
</body>
</html>
"""

# Rotas do Navegador
@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/conteudos')
def conteudos():
    return render_template_string(HTML_CONTEUDOS)

@app.route('/checkout-vip')
def checkout_vip():
    return render_template_string(HTML_CHECKOUT)

# Rota de criação do Pix via Mercado Pago
@app.route('/criar_pagamento', methods=['POST'])
def criar_pagamento():
    try:
        dados_cliente = request.json
        
        payment_data = {
            "transaction_amount": float(dados_cliente.get("valor", 29.90)),
            "description": "Acesso Canal VIP Telegram - Iasmin",
            "payment_method_id": "pix",
            "payer": {
                "email": dados_cliente.get("email", "cliente@email.com"),
                "first_name": dados_cliente.get("nome", "Cliente")
            }
        }

        result = sdk.payment().create(payment_data)
        payment_response = result["response"]
        
        transaction_data = payment_response.get("point_of_interaction", {}).get("transaction_data", {})
        qr_code = transaction_data.get("qr_code", "")
        payment_id = payment_response.get("id")

        return jsonify({
            "status": "sucesso",
            "payment_id": payment_id,
            "qr_code": qr_code
        })

    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route('/webhook_pagamento', methods=['POST'])
def webhook_pagamento():
    try:
        data = request.json
        if data and data.get("type") == "payment":
            payment_id = data.get("data", {}).get("id")
            payment_info = sdk.payment().get(payment_id)
            payment_status = payment_info["response"].get("status")
            
            if payment_status == "approved":
                payer_email = payment_info["response"].get("payer", {}).get("email")
                print(f"[GATILHO] Pagamento aprovado! ID: {payment_id} | Email: {payer_email}")

        return jsonify({"status": "recebido"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
