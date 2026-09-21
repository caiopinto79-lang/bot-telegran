import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Token de Acesso do Mercado Pago configurado diretamente
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# PÁGINA 1: Início (Redes Sociais + Botão +18)
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
            padding: 35px 25px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.7);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
            border: 1px solid #334155;
        }
        .avatar-placeholder {
            width: 80px;
            height: 80px;
            background: linear-gradient(135deg, var(--accent), #cbd5e1);
            border-radius: 50%;
            margin: 0 auto 15px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 12px rgba(244, 63, 94, 0.3);
        }
        h1 {
            font-size: 24px;
            margin-bottom: 5px;
            color: var(--text-main);
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 25px;
        }
        .section-title {
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin: 25px 0 12px 0;
            text-align: left;
            border-bottom: 1px solid #334155;
            padding-bottom: 6px;
            font-weight: 600;
        }
        .link-button {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            width: 100%;
            padding: 14px;
            margin-bottom: 12px;
            border-radius: 10px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            box-sizing: border-box;
            transition: all 0.25s ease;
            cursor: pointer;
            border: none;
        }
        .link-button:hover {
            opacity: 0.92;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }
        .btn-instagram { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .btn-tiktok { background-color: #000000; border: 1px solid #334155; }
        .btn-kwai { background-color: #ff5722; }
        .btn-adult-main { background-color: var(--accent); font-size: 15px; margin-top: 20px; box-shadow: 0 4px 15px rgba(244, 63, 94,.4); }
    </style>
</head>
<body>
    <div class="container">
        <div class="avatar-placeholder">I</div>
        <h1>Iasmin</h1>
        <p class="subtitle">Bem-vindo(a) aos meus links oficiais</p>

        <div class="section-title">Redes Sociais</div>
        <a href="https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj" target="_blank" class="link-button btn-instagram">📸 Instagram Oficial</a>
        <a href="https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE" target="_blank" class="link-button btn-tiktok">🎵 TikTok Oficial</a>
        <a href="https://k.kwai.com/u/@mc.iasmin_ofc/z0YdoxCi" target="_blank" class="link-button btn-kwai">⚡ Kwai Oficial</a>

        <div class="section-title">Conteúdo Exclusivo</div>
        <a href="/conteudos" class="link-button btn-adult-main" onclick="return confirmarIdade(event)">🔥 CONTEÚDO +18</a>
    </div>

    <script>
        function confirmarIdade(event) {
            const maior = confirm("Atenção: Este site contém material adulto (+18).\n\nVocê confirma que tem 18 anos ou mais?");
            if (!maior) {
                event.preventDefault();
                return false;
            }
            return true;
        }
    </script>
</body>
</html>
"""

# PÁGINA 2: Conteúdos Exclusivos (Com o Privacy em Laranja na primeira opção)
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
            padding: 35px 25px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.7);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
            border: 1px solid #334155;
        }
        h1 {
            font-size: 24px;
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
            border-radius: 10px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            box-sizing: border-box;
            transition: all 0.25s ease;
            cursor: pointer;
            border: none;
        }
        .link-button:hover {
            opacity: 0.92;
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }
        .btn-privacy { background-color: #ff7300; font-size: 15px; border: 2px solid #ff9133; }
        .btn-preview { background-color: #229ED9; }
        .btn-vip { background-color: #10b981; }
        .btn-voltar { background-color: #334155; color: var(--text-muted); font-size: 13px; padding: 10px; margin-top: 15px; }
        .btn-voltar:hover { color: #fff; background-color: #475569; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Área Restrita</h1>
        <p class="subtitle">Escolha uma das opções abaixo</p>

        <a href="https://privacy.com.br/profile/MCiasmin" target="_blank" class="link-button btn-privacy">🔥 Privacy</a>
        <a href="https://t.me/+A_pQQ1vDeY9kY2Yx" target="_blank" class="link-button btn-preview">💬 Canal de Prévias (Grátis no Telegram)</a>
        <a href="/checkout-vip" class="link-button btn-vip">🚀 Canal VIP Telegram (Acesso Direto - R$ 29,90)</a>

        <a href="/" class="link-button btn-voltar">⬅ Voltar à Página Inicial</a>
    </div>
</body>
</html>
"""

# PÁGINA 3: Tela de Pagamento do Canal VIP (Pix com QR Code Visual + Copia e Cola)
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
            padding: 35px 25px;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.7);
            width: 100%;
            max-width: 450px;
            box-sizing: border-box;
            text-align: center;
            margin: 20px;
            border: 1px solid #334155;
        }
        h1 {
            font-size: 22px;
            margin-bottom: 5px;
            color: var(--accent);
        }
        p.subtitle {
            color: var(--text-muted);
            font-size: 13px;
            margin-bottom: 20px;
        }
        .vip-box {
            background: rgba(244, 63, 94, 0.05);
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
            text-align: center;
        }
        .qrcode-img {
            width: 180px;
            height: 180px;
            border-radius: 8px;
            background: #fff;
            padding: 5px;
            margin: 10px auto;
            display: block;
        }
        textarea {
            width: 100%;
            height: 65px;
            background: var(--bg-color);
            color: var(--success);
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 8px;
            font-size: 11px;
            resize: none;
            box-sizing: border-box;
            margin-bottom: 8px;
            text-align: center;
        }
        .nav-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        .link-button {
            display: block;
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            font-size: 12px;
            box-sizing: border-box;
            text-align: center;
            border: none;
            cursor: pointer;
        }
        .btn-voltar { background-color: #334155; color: var(--text-muted); }
        .btn-voltar:hover { color: #fff; background-color: #475569; }
        .btn-home { background-color: #1e293b; border: 1px solid #475569; color: var(--text-muted); }
        .btn-home:hover { color: #fff; background-color: #334155; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Checkout Canal VIP</h1>
        <p class="subtitle">Preencha para gerar o Pix automático (R$ 29,90)</p>

        <div class="vip-box">
            <div id="form-pagamento">
                <input type="text" id="nome" placeholder="Seu Nome Completo" required>
                <input type="email" id="email" placeholder="Seu E-mail" required>
                <button class="action-btn" onclick="gerarPix()">Gerar Pix Agora</button>
            </div>

            <div id="resultado-pix">
                <p style="color: var(--success); font-weight: bold; font-size: 12px; margin-bottom: 4px;">Escaneie o QR Code ou Copie o Código:</p>
                <img id="qrcode-tag" class="qrcode-img" src="" alt="QR Code Pix">
                
                <textarea id="copia-cola" readonly></textarea>
                <button onclick="copiarPix()" class="action-btn" style="background-color: #10b981; padding: 10px; font-size: 13px;">Copiar Código Pix</button>
            </div>
        </div>

        <div class="nav-buttons">
            <a href="/conteudos" class="link-button btn-voltar">⬅ Voltar aos Conteúdos</a>
            <a href="/" class="link-button btn-home">🏠 Início</a>
        </div>
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
                    
                    if(data.qr_code_base64) {
                        document.getElementById('qrcode-tag').src = "data:image/jpeg;base64," + data.qr_code_base64;
                    }
                    
                    document.getElementById('resultado-pix').style.display = 'block';
                } else {
                    alert('Erro ao gerar pagamento: ' + data.detalhes);
                    btn.innerText = "Gerar Pix Agora";
                    btn.disabled = false;
                }
            } catch (error) {
                alert('Erro de conexão. Tente novamente.');
                btn.innerText = "Gerar Pix Agora";
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
        payment_response = result.get("response", {})
        
        qr_code = ""
        if "point_of_interaction" in payment_response:
            qr_code = payment_response["point_of_interaction"].get("transaction_data", {}).get("qr_code", "")
        if not qr_code and "transaction_data" in payment_response:
            qr_code = payment_response["transaction_data"].get("qr_code", "")

        qr_code_base64 = ""
        if "point_of_interaction" in payment_response:
            qr_code_base64 = payment_response["point_of_interaction"].get("transaction_data", {}).get("qr_code_base64", "")

        payment_id = payment_response.get("id")

        if not qr_code:
            return jsonify({"status": "erro", "detalhes": "O Mercado Pago não retornou o código QR/Pix. Verifique a resposta da API."}), 400

        return jsonify({
            "status": "sucesso",
            "payment_id": payment_id,
            "qr_code": qr_code,
            "qr_code_base64": qr_code_base64
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
