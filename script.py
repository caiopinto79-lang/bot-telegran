import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Credenciais do Mercado Pago configuradas via variáveis de ambiente no Render
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_DO_MERCADO_PAGO")
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# Mini site completo com redes sociais, seções de conteúdos e botão preparado para o bot
HTML_INDEX = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Acesso - Conteúdos Exclusivos & VIP</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --accent: #38bdf8;
            --accent-hover: #0ea5e9;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #34d399;
            --social-ig: #E1306C;
            --social-tg: #229ED9;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        .header {
            text-align: center;
            padding: 40px 20px 20px 20px;
        }
        .header h1 {
            font-size: 26px;
            color: var(--accent);
            margin-bottom: 10px;
        }
        .header p {
            color: var(--text-muted);
            font-size: 15px;
            max-width: 600px;
            margin: 0 auto;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
        }
        .section-box {
            background-color: var(--card-bg);
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            width: 100%;
            box-sizing: border-box;
            margin-bottom: 25px;
        }
        .section-box h3 {
            color: var(--accent);
            margin-top: 0;
            font-size: 18px;
            border-bottom: 1px solid #334155;
            padding-bottom: 10px;
        }
        .social-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .btn-social {
            flex: 1;
            padding: 12px;
            border-radius: 6px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            text-align: center;
            font-size: 14px;
            transition: opacity 0.3s;
        }
        .btn-instagram { background-color: var(--social-ig); }
        .btn-telegram { background-color: var(--social-tg); }
        .btn-social:hover { opacity: 0.85; }
        
        .content-list {
            list-style: none;
            padding: 0;
            margin: 0 0 20px 0;
            color: var(--text-muted);
            font-size: 14px;
        }
        .content-list li {
            padding: 8px 0;
            border-bottom: 1px dashed #334155;
            display: flex;
            align-items: center;
        }
        .content-list li::before {
            content: "✨";
            margin-right: 8px;
        }
        
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 6px;
            border: 1px solid #334155;
            background: var(--bg-color);
            color: #fff;
            box-sizing: border-box;
            font-size: 14px;
        }
        button.action-btn {
            background-color: var(--accent);
            color: #0f172a;
            border: none;
            padding: 14px;
            width: 100%;
            border-radius: 6px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button.action-btn:hover {
            background-color: var(--accent-hover);
            color: #fff;
        }
        #resultado-pix {
            margin-top: 20px;
            display: none;
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 90px;
            background: var(--bg-color);
            color: var(--accent);
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            resize: none;
            box-sizing: border-box;
            margin-bottom: 10px;
        }
        .price-display {
            font-size: 22px;
            font-weight: bold;
            color: var(--success);
            margin-bottom: 15px;
            text-align: center;
        }
        /* Botão preparado para o Bot (Fase 2) */
        .bot-redirect-container {
            margin-top: 15px;
            display: none;
            text-align: center;
        }
        .btn-bot {
            background-color: var(--social-tg);
            color: white;
            text-decoration: none;
            display: inline-block;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 15px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Central de Conteúdos & Acesso VIP</h1>
        <p>Explore nossas redes e garanta seu acesso restrito à comunidade exclusiva.</p>
    </div>

    <div class="main-container">
        <!-- Caixa de Redes Sociais e Atalhos -->
        <div class="section-box">
            <h3>Nossas Redes</h3>
            <div class="social-buttons">
                <a href="https://instagram.com" target="_blank" class="btn-social btn-instagram">Instagram</a>
                <a href="https://telegram.org" target="_blank" class="btn-social btn-telegram">Canal Público</a>
            </div>
        </div>

        <!-- Caixa de Descrição de Conteúdos -->
        <div class="section-box">
            <h3>Conteúdos Disponíveis no VIP</h3>
            <ul class="content-list">
                <li>Atualizações diárias de materiais exclusivos</li>
                <li>Arquivos e mídias liberados sem restrições</li>
                <li>Grupo privado com total segurança</li>
                <li>Suporte dedicado via bot</li>
            </ul>
        </div>

        <!-- Caixa de Pagamento e Liberação -->
        <div class="section-box">
            <h3>Garantir Acesso Imediato</h3>
            <div class="price-display">R$ 29,90 <span style="font-size: 12px; color: var(--text-muted); font-weight: normal;">(Acesso Único)</span></div>
            
            <div id="form-pagamento">
                <input type="text" id="nome" placeholder="Seu Nome Completo" required>
                <input type="email" id="email" placeholder="Seu Melhor E-mail" required>
                <button class="action-btn" onclick="gerarPix()">Gerar Pagamento Pix</button>
            </div>

            <div id="resultado-pix">
                <p style="color: var(--success); font-weight: bold; margin-bottom: 5px;">Pix Gerado com Sucesso!</p>
                <p style="font-size: 12px; color: var(--text-muted); margin-top: 0;">Copie o código abaixo e pague no app do seu banco:</p>
                <textarea id="copia-cola" readonly></textarea>
                <button class="action-btn" onclick="copiarPix()" style="background-color: #10b981; color: white; padding: 10px;">Copiar Código Pix</button>
            </div>

            <!-- Botão preparado para futura integração com o bot (Fase 2) -->
            <div id="container-botao-bot" class="bot-redirect-container">
                <p style="font-size: 13px; color: var(--success); margin-bottom: 10px;">Pagamento confirmado!</p>
                <a href="https://t.me/seu_bot_aqui" target="_blank" class="btn-bot">Falar com o Bot para Receber Acesso</a>
            </div>
        </div>
    </div>

    <script>
        async function gerarPix() {
            const nome = document.getElementById('nome').value;
            const email = document.getElementById('email').value;

            if(!nome || !email) {
                alert('Por favor, preencha todos os campos.');
                return;
            }

            const btn = document.querySelector('#form-pagamento button');
            btn.innerText = "A gerar Pix...";
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
                    
                    // Exemplo: se quiser simular o botão do bot aparecendo após gerar (ou depois do webhook)
                    // document.getElementById('container-botao-bot').style.display = 'block';
                } else {
                    alert('Erro ao gerar pagamento: ' + data.detalhes);
                    btn.innerText = "Gerar Pagamento Pix";
                    btn.disabled = false;
                }
            } catch (error) {
                alert('Erro de conexão. Tente novamente.');
                btn.innerText = "Gerar Pagamento Pix";
                btn.disabled = false;
            }
        }

        function copiarPix() {
            const copyText = document.getElementById("copia-cola");
            copyText.select();
            copyText.setSelectionRange(0, 99999);
            navigator.clipboard.writeText(copyText.value);
            alert("Código Pix copiado para a área de transferência!");
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
        <p>Obrigado pela sua compra. O seu pagamento foi processado com sucesso.</p>
        <a href="https://t.me/seu_bot_aqui" class="btn-telegram">Ir para o Bot do Telegram</a>
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
            "description": "Acesso ao Grupo VIP - Telegram",
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

@app.route('/sucesso')
def sucesso():
    return render_template_string(HTML_SUCESSO)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
