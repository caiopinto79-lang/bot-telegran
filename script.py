import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Token de Acesso do Mercado Pago configurado diretamente
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# PÁGINA 1: Início (Redes Sociais com Ícones + Botão +18)
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
            gap: 12px;
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
        .link-button svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
            flex-shrink: 0;
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
        
        <!-- Instagram -->
        <a href="https://www.instagram.com/iasmin_cavala?stkn=aGQ4MmYwd3ZrcnNj" target="_blank" class="link-button btn-instagram">
            <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            Instagram Oficial
        </a>

        <!-- TikTok -->
        <a href="https://www.tiktok.com/@ofc.mc.iasmin?_r=1&_t=ZS-99pBqgIckoE" target="_blank" class="link-button btn-tiktok">
            <svg viewBox="0 0 24 24"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 .88.13V9.4a6.84 6.84 0 0 0-1-.05A6.33 6.33 0 0 0 5 20.1a6.34 6.34 0 0 0 10.86-4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-1-.1z"/></svg>
            TikTok Oficial
        </a>

        <!-- Kwai -->
        <a href="https://k.kwai.com/u/@mc.iasmin_ofc/z0YdoxCi" target="_blank" class="link-button btn-kwai">
            <svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-3.5 13.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5zM8.5 14.5h-2v-5h2v5zm1.5-6.5h-5V6h5v2z"/></svg>
            Kwai Oficial
        </a>

        <div class="section-title">Conteúdo Exclusivo</div>
        <a href="/conteudos" class="link-button btn-adult-main" onclick="return confirmarIdade(event)">
            <svg viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            🔥 CONTEÚDO +18
        </a>
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

# PÁGINA 2: Conteúdos Exclusivos (Com ícone de coração estilizado perfeito para o Privacy)
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
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
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
        .link-button svg {
            width: 20px;
            height: 20px;
            fill: currentColor;
            flex-shrink: 0;
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

        <!-- Privacy (Com ícone de coração/assinatura alinhado) -->
        <a href="https://privacy.com.br/profile/MCiasmin" target="_blank" class="link-button btn-privacy">
            <svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            Privacy
        </a>

        <!-- Canal de Prévias (Telegram) -->
        <a href="https://t.me/+A_pQQ1vDeY9kY2Yx" target="_blank" class="link-button btn-preview">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.03-1.99 1.27-5.62 3.72-.53.36-1.01.54-1.44.53-.47-.02-1.37-.26-2.03-.48-.82-.27-1.47-.42-1.42-.88.03-.24.37-.49 1.02-.75 3.99-1.74 6.65-2.89 7.98-3.46 3.8-1.63 4.59-1.92 5.1-1.93.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.13-.04.28z"/></svg>
            Canal de Prévias
        </a>

        <!-- Canal VIP (Telegram) -->
        <a href="/checkout-vip" class="link-button btn-vip">
            <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.2-.08-.06-.19-.04-.27-.02-.12.03-1.99 1.27-5.62 3.72-.53.36-1.01.54-1.44.53-.47-.02-1.37-.26-2.03-.48-.82-.27-1.47-.42-1.42-.88.03-.24.37-.49 1.02-.75 3.99-1.74 6.65-2.89 7.98-3.46 3.8-1.63 4.59-1.92 5.1-1.93.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.13-.04.28z"/></svg>
            Canal VIP (R$ 29,90)
        </a>

        <a href="/" class="link-button btn-voltar">⬅ Voltar à Página Inicial</a>
    </div>
</body>
</html>
"""

# PÁGINA 3: Tela de Pagamento do Canal VIP
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
