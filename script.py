import os
import requests
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Credenciais oficiais do Mercado Pago
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"

# Link do Canal de Prévias do Telegram da Iasmin (substitua pelo link real quando quiser)
LINK_CANAL_PREVIAS = "https://t.me/+SEU_LINK_DO_CANAL_DE_PREVIAS"

# Links das Redes Sociais da Iasmin (substitua pelos perfis reais dela)
INSTAGRAM_LINK = "https://instagram.com/seus_perfil"
TIKTOK_LINK = "https://tiktok.com/@seus_perfil"
KWAI_LINK = "https://kwai.com/@seus_perfil"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iasmin - Links e Conteúdos</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0b0b0e; color: #f1f1f1; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: rgba(24, 24, 27, 0.95); padding: 35px 25px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); width: 100%; max-width: 450px; text-align: center; border: 1px solid rgba(255,255,255,0.08); }
        
        /* Perfil */
        .avatar { width: 90px; height: 90px; border-radius: 50%; background: #ff2a6d; margin: 0 auto 15px auto; display: flex; align-items: center; justify-content: center; font-size: 36px; font-weight: bold; color: #fff; border: 3px solid rgba(255,42,109,0.4); }
        h1 { color: #fff; font-size: 22px; margin-bottom: 5px; }
        .bio { font-size: 13px; color: #a1a1aa; margin-bottom: 25px; }

        h2 { color: #ff2a6d; margin-bottom: 15px; font-size: 20px; }
        p { font-size: 14px; color: #a1a1aa; margin-bottom: 20px; line-height: 1.5; }
        
        /* Botões */
        .btn { background-color: #ff2a6d; color: white; border: none; padding: 14px 20px; border-radius: 12px; font-size: 15px; cursor: pointer; width: 100%; font-weight: bold; transition: all 0.2s; margin-top: 12px; text-decoration: none; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 15px rgba(255,42,109,0.3); }
        .btn:hover { background-color: #e01b5d; transform: translateY(-2px); }
        
        .btn-social { background-color: #18181b; border: 1px solid #27272a; color: #f1f1f1; }
        .btn-social:hover { background-color: #27272a; border-color: #ff2a6d; }
        
        .btn-secundario { background-color: #27272a; border: 1px solid #3f3f46; color: #fff; }
        .btn-secundario:hover { background-color: #3f3f46; }
        
        .hidden { display: none; }
        
        /* Caixa do Pix */
        .pix-box { background: #121215; padding: 20px; border-radius: 12px; border: 1px solid #27272a; margin-top: 15px; text-align: left; }
        .qrcode-img { width: 150px; height: 150px; margin: 0 auto 15px auto; border-radius: 8px; background: #fff; padding: 6px; display: block; border: 3px solid #ff2a6d; }
        .chave-copia { background: #18181b; border: 1px dashed #52525b; color: #f1f1f1; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px; word-break: break-all; margin-bottom: 10px; max-height: 70px; overflow-y: auto; }
        
        .status-aguardando { color: #ff2a6d; font-weight: bold; font-size: 13px; margin-top: 15px; text-align: center; }
        .divider { height: 1px; background: rgba(255,255,255,0.08); margin: 25px 0; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Vitrine / Mini Site Principal da Iasmin -->
        <div id="step-home">
            <div class="avatar">I</div>
            <h1>Iasmin</h1>
            <div class="bio">Bem-vindo(a) ao meu portal oficial! Acompanhe minhas redes sociais abaixo.</div>

            <!-- Botões das Redes Sociais -->
            <a href="INSTAGRAM_URL_PLACEHOLDER" target="_blank" class="btn btn-social">📸 Instagram Oficial</a>
            <a href="TIKTOK_URL_PLACEHOLDER" target="_blank" class="btn btn-social">🎬 TikTok</a>
            <a href="KWAI_URL_PLACEHOLDER" target="_blank" class="btn btn-social">⚡ Kwai</a>

            <div class="divider"></div>

            <!-- Seção do Canal de Prévias via Pix -->
            <div style="background: rgba(255,42,109,0.05); border: 1px solid rgba(255,42,109,0.2); padding: 20px; border-radius: 14px;">
                <h3 style="color: #ff2a6d; font-size: 17px; margin-bottom: 8px;">🔥 Canal de Prévias VIP</h3>
                <p style="font-size: 13px; margin-bottom: 15px;">Tenha acesso liberado ao canal de prévias exclusivo.</p>
                <div style="font-size: 22px; font-weight: bold; color: #00e676; margin-bottom: 15px;">R$ 1,00 <span style="font-size: 11px; color: #a1a1aa; font-weight: normal;">/ acesso</span></div>
                <button class="btn" onclick="gerarPagamentoPix()">Liberar Acesso via Pix</button>
            </div>
        </div>

        <!-- Etapa de Pagamento (Pix) -->
        <div id="step-pagamento" class="hidden">
            <h2>💳 Pagamento Pix</h2>
            <p>Escaneie o QR Code ou copie a chave abaixo para liberar o acesso instantaneamente:</p>
            
            <div class="pix-box">
                <img id="qrCodeImg" class="qrcode-img" src="" alt="QR Code Pix">
                <div class="chave-copia" id="textoChavePix">Carregando chave...</div>
                <button class="btn btn-secundario" style="padding: 10px; font-size: 12px; margin: 0; width: 100%;" onclick="copiarChave()">📋 Copiar Pix Copia e Cola</button>
            </div>

            <p id="statusPagamento" class="status-aguardando">⏳ Aguardando a aprovação do pagamento...</p>
        </div>

        <!-- Etapa de Sucesso (Liberação do Canal) -->
        <div id="step-success" class="hidden">
            <h2>🎉 Pagamento Aprovado!</h2>
            <p>Obrigado! O seu pagamento foi confirmado com sucesso. Clique abaixo para entrar no canal de prévias:</p>
            <a id="linkTelegram" href="" target="_blank" class="btn" style="background-color: #00e676; color: #000;">🚀 Entrar no Canal de Prévias</a>
            <p style="font-size: 11px; color: #71717a; margin-top: 15px;">⚠️ Aproveite o conteúdo exclusivo!</p>
        </div>
    </div>

    <script>
        let paymentId = null;
        let checkInterval = null;

        function copiarChave() {
            let texto = document.getElementById('textoChavePix').innerText;
            navigator.clipboard.writeText(texto).then(() => {
                alert('Chave Pix copiada com sucesso!');
            });
        }

        async function gerarPagamentoPix() {
            document.getElementById('step-home').classList.add('hidden');
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

                // Checa o status do pagamento a cada 4 segundos
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
                    document.getElementById('linkTelegram').href = data.link_canal;
                    document.getElementById('step-pagamento').classList.add('hidden');
                    document.getElementById('step-success').classList.remove('hidden');
                }
            } catch (err) {
                console.log('Verificando status...');
            }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    rendered_html = HTML_TEMPLATE.replace("INSTAGRAM_URL_PLACEHOLDER", INSTAGRAM_LINK) \
                                 .replace("TIKTOK_URL_PLACEHOLDER", TIKTOK_LINK) \
                                 .replace("KWAI_URL_PLACEHOLDER", KWAI_LINK)
    return render_template_string(rendered_html)

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
        "description": "Acesso - Canal de Prévias Iasmin",
        "payment_method_id": "pix",
        "payer": {
            "email": "cliente@iasmin.com"
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
    
    link_canal = LINK_CANAL_PREVIAS if status == 'approved' else ""

    return jsonify({
        "status": status,
        "link_canal": link_canal
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
