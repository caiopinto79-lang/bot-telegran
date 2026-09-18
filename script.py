import os
import mercadopago
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Credenciais do Mercado Pago configuradas via variáveis de ambiente no Render
MP_ACCESS_TOKEN = os.environ.get("MP_ACCESS_TOKEN", "SEU_ACCESS_TOKEN_DO_MERCADO_PAGO")
sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

# Mini site com a estrutura visual original solicitada
HTML_INDEX = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP Book Rosa - Acesso Exclusivo</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #1e293b;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            width: 100%;
            max-width: 420px;
            box-sizing: border-box;
            text-align: center;
        }
        h1 {
            font-size: 22px;
            margin-bottom: 5px;
            color: #38bdf8;
        }
        p {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .social-buttons {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .btn-social {
            flex: 1;
            padding: 10px;
            border-radius: 6px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            font-size: 13px;
        }
        .btn-instagram { background-color: #E1306C; }
        .btn-telegram { background-color: #229ED9; }
        
        input {
            width: 100%;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 6px;
            border: 1px solid #334155;
            background: #0f172a;
            color: #fff;
            box-sizing: border-box;
        }
        button {
            background-color: #0284c7;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 6px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover { background-color: #0ea5e9; }
        #resultado-pix {
            margin-top: 20px;
            display: none;
        }
        textarea {
            width: 100%;
            height: 80px;
            background: #0f172a;
            color: #38bdf8;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            resize: none;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>VIP Book Rosa</h1>
        <p>Acesse nossos conteúdos exclusivos e garanta sua vaga.</p>
        
        <div class="social-buttons">
            <a href="https://instagram.com" target="_blank" class="btn-social btn-instagram">Instagram</a>
            <a href="https://t.me" target="_blank" class="btn-social btn-telegram">Canal Telegram</a>
        </div>

        <div id="form-pagamento">
            <input type="text" id="nome" placeholder="Seu Nome Completo" required>
            <input type="email" id="email" placeholder="Seu E-mail" required>
            <button onclick="gerarPix()">Gerar Pagamento Pix (R$ 29,90)</button>
        </div>

        <div id="resultado-pix">
            <p style="color: #34d399; font-weight: bold; font-size: 13px;">Pix Gerado com Sucesso!</p>
            <p style="font-size: 11px; color: #94a3b8;">Copie o código Pix copia e cola abaixo:</p>
            <textarea id="copia-cola" readonly></textarea>
            <button onclick="copiarPix()" style="margin-top: 10px; background-color: #10b981;">Copiar Código Pix</button>
            
            <!-- [PONTO DE ADAPTAÇÃO FUTURA DO BOT] Linhas de redirecionamento para o bot serão inseridas aqui -->
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
            }
        }

        function copiarPix() {
            const copyText = document.getElementById("copia-cola");
            copyText.select();
            document.execCommand("copy");
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
        h1 { color: #34d399; }
        p { color: #94a3b8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pagamento Confirmado!</h1>
        <p>Obrigado pela sua compra. O seu pagamento foi processado com sucesso.</p>
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
            "description": "Acesso VIP Book Rosa",
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
                # [PONTO DE ADAPTAÇÃO FUTURA DO BOT] O gatilho de notificação para o bot será conectado aqui
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
