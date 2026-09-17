import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

SITE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agência Bot - Plataforma Oficial</title>
    <style>
        /* Configuração Global e Fundo com Textura Sutil / Camada Estilizada */
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

        /* Container Expansivo Responsivo */
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

        /* Oculta e exibe telas de forma dinâmica */
        .tela { display: none; }
        .tela.ativa { display: block; }

        /* Logo Agência Bot Discreto e Elegante no Topo */
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

        /* Botões de Ação Modernos */
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

        /* Área do Pix / Mercado Pago */
        .pix-box {
            background: #121215;
            border: 1px solid #27272a;
            padding: 25px;
            border-radius: 14px;
            margin: 20px 0;
        }
        .qrcode-mock {
            width: 170px;
            height: 170px;
            background: #fff;
            margin: 0 auto 15px auto;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #000;
            font-weight: bold;
            font-size: 13px;
            border: 4px solid #ff2a6d;
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

        /* Responsividade para Computadores e Celulares */
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

    <!-- TELA 2: Vitrine do Grupo VIP + Exibição do Processo -->
    <div id="tela-home" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>🔥 Grupo VIP Exclusivo</h2>
        <p>Tenha acesso direto ao nosso canal fechado com atualizações diárias e conteúdo sem censura.</p>

        <div class="badge-aviso">
            💡 <b>Como funciona:</b> Após realizar o pagamento via Pix ou Mercado Pago, o sistema reconhece a transação e libera instantaneamente o link de acesso exclusivo de uso único para você entrar no grupo com apenas um clique.
        </div>

        <div style="font-size: 28px; font-weight: bold; color: #00e676; margin-bottom: 25px;">
            R$ 49,90 <span style="font-size: 13px; color: #a1a1aa; font-weight: normal;">/ acesso mensal</span>
        </div>

        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-pagamento')">Realizar Pagamento do Acesso</button>
    </div>

    <!-- TELA 3: Pagamento (QR Code / Copia e Cola) -->
    <div id="tela-pagamento" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>💳 Pagamento Seguro</h2>
        <p>Escaneie o QR Code com o aplicativo do seu banco ou utilize a chave Pix (Copia e Cola).</p>

        <div class="pix-box">
            <div class="qrcode-mock">
                [ QR CODE PIX ]
            </div>
            <div class="chave-copia" id="textoChavePix">
                00020126580014br.gov.bcb.pix0136agencia-bot-pagamento-exemplo5204000053039865802BR5913Agencia Bot6009Sao Paulo63041C9C
            </div>
            <button class="btn-opcao" style="padding: 10px; font-size: 13px; margin-bottom: 0;" onclick="copiarChavePix()">📋 Copiar Chave Pix</button>
        </div>

        <p style="font-size: 13px; color: #71717a; margin-top: 15px;">Assim que efetuar o pagamento, clique no botão abaixo para simular a confirmação automática pelo Mercado Pago:</p>
        <button class="btn-opcao btn-destaque" onclick="simularReconhecimentoMercadoPago()">Simular Pagamento Aprovado</button>
        <button class="btn-opcao" style="background: transparent; border: none; color: #a1a1aa;" onclick="mostrarTela('tela-home')">⬅ Voltar</button>
    </div>

    <!-- TELA 4: Processando / Reconhecendo Pagamento -->
    <div id="tela-processando" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>🔄 Processando Transação...</h2>
        <p>Aguarde um instante enquanto o Mercado Pago valida o seu Pix e libera a sua credencial exclusiva.</p>
        <div style="font-size: 40px; margin: 30px 0;">⚡</div>
    </div>

    <!-- TELA 5: Sucesso - Link Único Liberado Automaticamente -->
    <div id="tela-sucesso" class="container tela">
        <div class="logo-agencia">Plataforma Oficial • <span>Agência Bot</span></div>
        <h2>🎉 Pagamento Aprovado com Sucesso!</h2>
        <p>Identificamos sua transação instantaneamente. Seu link exclusivo de uso único foi gerado.</p>

        <a href="https://t.me/seu_grupo_vip_agencia_bot" target="_blank" class="btn-opcao btn-destaque" style="font-size: 18px; padding: 20px; margin-top: 20px;">
            🚀 Entrar no Grupo do Telegram Agora
        </a>
        <p style="font-size: 12px; color: #71717a; margin-top: 15px;">Este link expira automaticamente após o primeiro uso por motivos de segurança.</p>
    </div>

    <script>
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

        function simularReconhecimentoMercadoPago() {
            // Vai para a tela de processamento automático
            mostrarTela('tela-processando');
            
            // Simula o tempo de resposta da API do Mercado Pago validando o Pix (2.5 segundos) e libera o botão do Telegram
            setTimeout(() => {
                mostrarTela('tela-sucesso');
            }, 2500);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return SITE_HTML

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        texto_recebido = data['message'].get('text', '')
        resposta = f"Olá! Recebi sua mensagem: '{texto_recebido}'."
        requests.post(TELEGRAM_URL, json={'chat_id': chat_id, 'text': resposta})
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
