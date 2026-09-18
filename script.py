import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Credenciais do Mercado Pago configuradas via variáveis de ambiente no Render
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_DO_MERCADO_PAGO")
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# Mini site completo com todas as redes sociais, conteúdos +18, prévias do Telegram e botões originais
HTML_INDEX = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Exclusivo - Links & Acessos VIP</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #f43f5e;
            --accent-hover: #e11d48;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #34d399;
            --social-ig: #E1306C;
            --social-tk: #000000;
            --social-kw: #FF6600;
            --social-tg: #229ED9;
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
            margin-bottom: 25px;
        }
        .section-title {
            font-size: 14px;
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
            padding: 12px;
            margin-bottom: 10px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 14px;
            box-sizing: border-box;
            transition: opacity 0.3s, transform 0.2s;
        }
        .link-button:hover {
            opacity: 0.9;
            transform: translateY(-2px);
        }
        .btn-instagram { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        .btn-tiktok { background-color: #010101; border: 1px solid #333; }
        .btn-kwai { background-color: #ff5722; }
        .btn-telegram-preview { background-color: var(--social-tg); }
        .btn-privacy { background-color: #00aff0; }

        .vip-box {
            background: rgba(244, 63, 94, 0.1);
            border: 1px dashed var(--accent);
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 12px;
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
    </style>
</head>
<body>
    <div class="container">
        <h1>Conteúdos Exclusivos</h1>
        <p class="subtitle">Acesse minhas redes, prévias e garanta sua vaga VIP</p>

        <!-- Redes Sociais -->
        <div class="section-title">Minhas Redes</div>
        <a href="https://instagram.com/SEU_USUARIO" target="_blank" class="link-button btn-instagram">📸 Instagram Oficial</a>
        <a href="https://tiktok.com/@SEU_USUARIO" target="_blank" class="link-button btn-tiktok">tiktok TikTok</a>
        <a href="https://kwai.com" target="_blank" class="link-button btn-kwai">⚡ Kwai</a>

        <!-- Conteúdos e Prévias -->
        <div class="section-title">Conteúdos +18 & Prévias</div>
        <a href="https://t.me/CANAL_PREVIAS" target="_blank" class="link-button btn-telegram-preview">💬 Grupo de Prévias (Telegram Grátis)</a>
        <a href="https://privacy.com.br/SEU_LINK" target="_blank" class="link-button btn-privacy">💎 Meu Privacy / Plataformas</a>

        <!-- Seção VIP / Mercado Pago -->
        <div class="vip-box">
            <div class="section-title" style="margin-top:0; border:none; color: var(--accent);">🔥 Canal VIP Definitivo</div>
            <p style="font-size: 12px; color: var(--text-muted); margin-bottom: 12px;">Acesso completo liberado direto no Bot após o pagamento (R$ 29,90)</p>
            
            <div id="form-pagamento">
                <input type="text" id="nome" placeholder="Seu Nome" required>
                <input type="email" id="email" placeholder="Seu E-mail" required>
                <button class="action-btn" onclick="gerarPix()">Gerar Pix de Acesso</button>
            </div>

            <div id="resultado-pix">
                <p style="color: var(--success); font-weight: bold; font-size: 12px; margin-bottom: 4px;">Pix Gerado com Sucesso!</p>
                <textarea id="copia-cola" readonly></textarea>
                <button onclick="copiarPix()" class="action-btn" style="background-color: #10b981; padding: 10px; font-size: 13px;">Copiar Código Pix</button>
                
                <!-- [PONTO DE ADAPTAÇÃO FUTURA DO BOT] Linha reservada para direcionar ao Bot do Telegram após confirmação -->
            </div>
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
            btn.innerText = "Gerando...";
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
                    btn.innerText = "Gerar Pix de Acesso";
                    btn.disabled = false;
                }
            } catch (error) {
                alert('Erro de conexão. Tente novamente.');
                btn.innerText = "Gerar Pix de Acesso";
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

HTML_SUCESSO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pagamento Aprovado</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; text-align: center; }
        .container { background-color: #1e293b; padding: 40px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); max-width: 400px; }
        h1 { color: #34d399; margin-bottom: 15px; }
        p { color: #94a3b8; font-size: 15px; margin-bottom: 20px; }
        .btn-telegram { background-color: #229ED9; color: white; text-decoration: none; padding: 12px 20px; border-radius: 6px; font-weight: bold; display: inline-block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pagamento Aprovado!</h1>
        <p>Obrigado. O seu pagamento foi processado com sucesso.</p>
        <a href="https://t.me/seu_bot_aqui" class="btn-telegram">Aceder ao Bot do Telegram</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/criar_pagamento', methods=['POST'])
def criar_pagamento():
    try:
        dados_cliente = request.json
        
        payment_data = {
            "transaction_amount": float(dados_cliente.get("valor", 29.90)),
            "description": "Acesso VIP Exclusivo",
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
                # [PONTO DE ADAPTAÇÃO FUTURA DO BOT] O gatilho que avisa o bot para liberar o acesso será conectado aqui
                print(f"[GATILHO] Pagamento aprovado! ID: {payment_id} | Email: {payer_email}")

        return jsonify({"status": "recebido"}), 200
    except Exception as e:
        return jsonify({"status": "erro", "detalhes": str(e)}), 500

@app.route('/sucesso')
def sucesso():
    return render_template_string(HTML_SUCESSO)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
