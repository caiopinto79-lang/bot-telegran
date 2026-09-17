import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Token do seu bot do Telegram (se quiser configurar depois)
TOKEN = os.environ.get('TELEGRAM_TOKEN', 'SEU_TOKEN_AQUI')
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Código HTML/JS do site completo
SITE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agência Bot - Acesso Restrito</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 450px; margin: 40px auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.8); border: 1px solid #333; text-align: left; }
        h2 { color: #ff4081; margin-top: 0; text-align: center; font-size: 22px; }
        p { color: #b0bec5; font-size: 14px; line-height: 1.5; text-align: center; margin-bottom: 20px; }
        .btn-opcao { background: #2a2a2a; color: #fff; border: 1px solid #444; padding: 15px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-bottom: 12px; display: block; text-align: center; box-sizing: border-box; }
        .btn-opcao:hover { background: #333; border-color: #ff4081; }
        .btn-destaque { background: #ff4081; color: #fff; border: none; }
        .btn-destaque:hover { background: #e91e63; }
        .form-group { margin-bottom: 12px; }
        label { color: #b0bec5; font-size: 13px; display: block; margin-bottom: 5px; }
        .form-control { width: 100%; padding: 10px; background: #121212; border: 1px solid #444; color: #fff; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        .aviso-legal { background: rgba(255, 64, 129, 0.1); border-left: 3px solid #ff4081; padding: 10px; font-size: 12px; color: #b0bec5; margin-bottom: 15px; border-radius: 0 6px 6px 0; line-height: 1.4; }
        .tela { display: none; }
        .tela.ativa { display: block; }
        .product { background: #2a2a2a; border: 1px solid #333; padding: 12px; margin: 10px 0; border-radius: 8px; }
        .product h3 { margin: 0 0 5px 0; color: #fff; font-size: 16px; }
        .product p { color: #b0bec5; font-size: 13px; margin: 0 0 8px 0; text-align: left; }
        .price { color: #00e676; font-weight: bold; font-size: 15px; margin-bottom: 8px; }
        button.comprar { background: #ff4081; color: white; border: none; padding: 8px 12px; width: 100%; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <div id="tela-escolha" class="container ativa">
        <h2>🔥 Agência Bot</h2>
        <p>Selecione o seu perfil de acesso para continuar:</p>
        <button class="btn-opcao btn-destaque" onclick="irParaCriador()">👩‍🦰 Sou Criador(a) / Profissional</button>
        <button class="btn-opcao" onclick="irParaConsumidor()">🛍️ Sou Consumidor(a) / Cliente</button>
    </div>

    <div id="tela-criador-menu" class="container tela">
        <h2>Painel de Criadores</h2>
        <p>Acesse sua conta ou faça seu registro profissional.</p>
        <button class="btn-opcao" onclick="mostrarTela('tela-login')">🔑 Já tenho cadastro (Login)</button>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-cadastro-criador')">📝 Quero me cadastrar (Novo)</button>
        <button class="btn-opcao" style="background:#333; margin-top:20px;" onclick="voltarParaEscolha()">⬅ Voltar</button>
    </div>

    <div id="tela-login" class="container tela">
        <h2>Login de Criador(a)</h2>
        <div class="form-group">
            <label>E-mail ou Usuário:</label>
            <input type="text" id="loginUser" class="form-control" placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label>Senha:</label>
            <input type="password" id="loginPass" class="form-control" placeholder="********">
        </div>
        <button class="btn-opcao btn-destaque" onclick="fazerLogin()">Entrar no Painel</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <div id="tela-cadastro-criador" class="container tela">
        <h2>Cadastro de Criador(a)</h2>
        <div class="aviso-legal">
            🔒 O cadastro exige validação de identidade e consentimento mútuo das partes.
        </div>
        <div class="form-group">
            <label>Nome Completo / Artístico:</label>
            <input type="text" id="novoNome" class="form-control" placeholder="Seu nome">
        </div>
        <div class="form-group">
            <label>E-mail:</label>
            <input type="email" id="novoEmail" class="form-control" placeholder="email@dominio.com">
        </div>
        <div class="form-group">
            <label>Telefone / WhatsApp:</label>
            <input type="text" id="novoTel" class="form-control" placeholder="(00) 00000-0000">
        </div>
        <div class="form-group">
            <label>Cidade / Estado onde atua:</label>
            <input type="text" id="novoCidade" class="form-control" placeholder="Ex: Birigui - SP">
        </div>
        <div class="form-group">
            <label>O que você vai comercializar?</label>
            <select id="novoTipoProduto" class="form-control">
                <option value="conteudo">Conteúdos Digitais (Packs / Vídeos)</option>
                <option value="acompanhante">Acompanhante / Perfil Profissional</option>
                <option value="ambos">Ambos</option>
            </select>
        </div>
        <div class="form-group">
            <label>📸 Verificação Facial / Documento:</label>
            <input type="file" id="novoFotoFacial" class="form-control" accept="image/*">
        </div>
        <div class="form-group">
            <label>Crie uma Senha:</label>
            <input type="password" id="novoSenha" class="form-control" placeholder="Mínimo 6 dígitos">
        </div>
        <button class="btn-opcao btn-destaque" onclick="finalizarCadastro()">Enviar para Análise</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <div id="tela-idade-consumidor" class="container tela">
        <h2>⚠️ Confirmação de Idade (+18)</h2>
        <p>Este ambiente contém conteúdos restritos para maiores de 18 anos. Você confirma ter idade legal?</p>
        <button class="btn-opcao btn-destaque" onclick="entrarComoConsumidor()">Sim, tenho 18 anos ou mais</button>
        <button class="btn-opcao" style="background:#d32f2f;" onclick="window.location.href='https://www.google.com'">Não, sair</button>
    </div>

    <div id="tela-catalogo" class="container tela" style="max-width: 500px;">
        <h2>🔥 Diretório & Catálogo VIP</h2>
        <p style="margin-bottom:10px;">Área exclusiva para clientes e consumidores.</p>
        <button class="btn-opcao" style="background:#333; padding: 10px; margin-bottom:15px;" onclick="voltarParaEscolha()">🚪 Trocar de Perfil / Sair</button>
        
        <div class="product">
            <h3>🌟 Acesso Geral ao Grupo VIP</h3>
            <p>Acesso completo a todo o acervo principal liberado na nuvem.</p>
            <div class="price">R$ 10,00</div>
            <button class="comprar" onclick="alert('Redirecionando para pagamento...')">Comprar Acesso (R$ 10)</button>
        </div>
    </div>

    <script>
        function mostrarTela(idTela) {
            document.querySelectorAll('.tela').forEach(el => el.classList.remove('ativa'));
            document.getElementById(idTela).classList.add('ativa');
        }
        function irParaCriador() { mostrarTela('tela-criador-menu'); }
        function irParaConsumidor() { mostrarTela('tela-idade-consumidor'); }
        function voltarParaEscolha() { mostrarTela('tela-escolha'); }
        function entrarComoConsumidor() { mostrarTela('tela-catalogo'); }
        function fazerLogin() {
            let user = document.getElementById('loginUser').value;
            if(!user) { alert('Preencha seu login!'); return; }
            alert('Login efetuado com sucesso!');
            mostrarTela('tela-catalogo');
        }
        function finalizarCadastro() {
            let nome = document.getElementById('novoNome').value;
            let email = document.getElementById('novoEmail').value;
            if(!nome || !email) { alert('Preencha pelo menos nome e e-mail!'); return; }
            alert('Cadastro enviado com sucesso!');
            mostrarTela('tela-catalogo');
        }
    </script>
</body>
</html>
"""

# Rota principal (Mostra o Site)
@app.route('/')
def home():
    return SITE_HTML

# Rota onde o Telegram vai enviar as mensagens do bot (Webhook)
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        texto_recebido = data['message'].get('text', '')

        # Resposta automática simples do bot
        resposta = f"Olá! Recebi sua mensagem: '{texto_recebido}'. Acesse nosso site principal pelo link do Render."
        
        # Envia de volta para o Telegram
        requests.post(TELEGRAM_URL, json={'chat_id': chat_id, 'text': resposta})

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
