import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações fixadas (Telegram e Mercado Pago)
TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"

# Código HTML/JS do site completo com Painel de Criadora e Cadastro de Pacotes Avulsos
SITE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agência Bot - Plataforma Oficial</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; text-align: center; }
        .container { max-width: 480px; margin: 30px auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.8); border: 1px solid #333; text-align: left; }
        h2 { color: #ff4081; margin-top: 0; text-align: center; font-size: 22px; }
        p { color: #b0bec5; font-size: 14px; line-height: 1.5; text-align: center; margin-bottom: 20px; }
        .btn-opcao { background: #2a2a2a; color: #fff; border: 1px solid #444; padding: 14px; width: 100%; border-radius: 8px; font-size: 15px; font-weight: bold; cursor: pointer; margin-bottom: 12px; display: block; text-align: center; box-sizing: border-box; text-decoration: none; }
        .btn-opcao:hover { background: #333; border-color: #ff4081; }
        .btn-destaque { background: #ff4081; color: #fff; border: none; }
        .btn-destaque:hover { background: #e91e63; }
        .form-group { margin-bottom: 12px; }
        label { color: #b0bec5; font-size: 13px; display: block; margin-bottom: 5px; }
        .form-control { width: 100%; padding: 10px; background: #121212; border: 1px solid #444; color: #fff; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        .aviso-legal { background: rgba(255, 64, 129, 0.1); border-left: 3px solid #ff4081; padding: 10px; font-size: 12px; color: #b0bec5; margin-bottom: 15px; border-radius: 0 6px 6px 0; line-height: 1.4; }
        .info-box { background: rgba(0, 230, 118, 0.1); border-left: 3px solid #00e676; padding: 10px; font-size: 12px; color: #b0bec5; margin-bottom: 15px; border-radius: 0 6px 6px 0; line-height: 1.4; }
        .tela { display: none; }
        .tela.ativa { display: block; }
        .product { background: #2a2a2a; border: 1px solid #333; padding: 12px; margin: 10px 0; border-radius: 8px; }
        .product h3 { margin: 0 0 5px 0; color: #fff; font-size: 16px; }
        .product p { color: #b0bec5; font-size: 13px; margin: 0 0 8px 0; text-align: left; }
        .price { color: #00e676; font-weight: bold; font-size: 15px; margin-bottom: 8px; }
        a.comprar { background: #ff4081; color: white; border: none; padding: 10px 12px; width: 100%; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: block; text-align: center; text-decoration: none; box-sizing: border-box; }
        a.comprar:hover { background: #e91e63; }
        .avatar-preview { width: 80px; height: 80px; border-radius: 50%; background: #333; margin: 0 auto 15px auto; display: block; object-fit: cover; border: 2px solid #ff4081; }
    </style>
</head>
<body>

    <!-- TELA 1: Escolha de Perfil -->
    <div id="tela-escolha" class="container ativa">
        <h2>🔥 Agência Bot</h2>
        <p>Selecione o seu perfil de acesso para continuar:</p>
        <button class="btn-opcao btn-destaque" onclick="irParaCriadorMenu()">👩‍🦰 Sou Criador(a) / Profissional</button>
        <button class="btn-opcao" onclick="mostrarTela('tela-idade-consumidor')">🛍️ Sou Consumidor(a) / Cliente</button>
    </div>

    <!-- TELA 2: Menu de Criadores (Login ou Cadastro) -->
    <div id="tela-criador-menu" class="container tela">
        <h2>Painel de Criadores</h2>
        <p>Acesse sua conta ou faça seu registro profissional para gerenciar seus pacotes.</p>
        <button class="btn-opcao" onclick="mostrarTela('tela-login')">🔑 Já tenho cadastro (Login)</button>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-cadastro-criador')">📝 Quero me cadastrar (Novo)</button>
        <button class="btn-opcao" style="background:#333; margin-top:20px;" onclick="voltarParaEscolha()">⬅ Voltar</button>
    </div>

    <!-- TELA 3: Login -->
    <div id="tela-login" class="container tela">
        <h2>Login de Criador(a)</h2>
        <div class="form-group">
            <label>E-mail cadastrado:</label>
            <input type="email" id="loginEmail" class="form-control" placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label>Senha:</label>
            <input type="password" id="loginPass" class="form-control" placeholder="********">
        </div>
        <button class="btn-opcao btn-destaque" onclick="fazerLogin()">Entrar no Painel</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <!-- TELA 4: Cadastro de Criador (Novo) -->
    <div id="tela-cadastro-criador" class="container tela">
        <h2>Cadastro de Criador(a)</h2>
        <div class="aviso-legal">
            🔒 O cadastro exige validação de identidade. Após cadastrar, você poderá entrar direto no painel para criar seus pacotes.
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
            <label>Crie uma Senha:</label>
            <input type="password" id="novoSenha" class="form-control" placeholder="Mínimo 6 dígitos">
        </div>
        <button class="btn-opcao btn-destaque" onclick="finalizarCadastro()">Concluir e Acessar Painel</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <!-- TELA 5: Painel Exclusivo da Criadora (Gerenciamento e Criação de Pacotes) -->
    <div id="tela-painel-criador" class="container tela" style="max-width: 520px;">
        <h2>✨ Meu Painel Profissional</h2>
        <div style="text-align: center; margin-bottom: 15px;">
            <img id="avatarPreview" src="https://via.placeholder.com/80" class="avatar-preview" alt="Foto de Perfil">
            <h3 id="painelNomeCriadora" style="margin:5px 0; color:#fff;">Nome da Criadora</h3>
            <p style="margin:0; font-size:12px; color:#00e676;">Status: Verificado e Ativo</p>
        </div>

        <div class="info-box">
            💡 <b>Regra de Repasse:</b> A plataforma cobra apenas <b>1% de comissão</b> por cada pacote avulso vendido diretamente pelo site. O restante vai direto para sua caixinha!
        </div>

        <!-- Etapa 1: Alterar Foto e Dados -->
        <div style="background: #2a2a2a; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="font-size: 14px; margin-top:0; color:#ff4081;">1️⃣ Alterar Foto de Perfil</h3>
            <div class="form-group" style="margin-bottom:5px;">
                <input type="file" id="inputFotoPerfil" class="form-control" accept="image/*" onchange="atualizarFoto(event)">
            </div>
        </div>

        <!-- Etapa 2: Criar Pacote Avulso -->
        <div style="background: #2a2a2a; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="font-size: 14px; margin-top:0; color:#ff4081;">2️⃣ Criar Novo Pacote Avulso</h3>
            <div class="form-group">
                <label>Título do Pacote:</label>
                <input type="text" id="pacoteTitulo" class="form-control" placeholder="Ex: Pack Exclusivo Verão">
            </div>
            <div class="form-group">
                <label>Descrição do Conteúdo:</label>
                <input type="text" id="pacoteDesc" class="form-control" placeholder="Ex: 15 fotos + 2 vídeos em alta definição">
            </div>
            <div class="form-group">
                <label>Valor (R$):</label>
                <input type="number" id="pacotePreco" class="form-control" placeholder="25.00">
            </div>
            <button class="btn-opcao btn-destaque" style="padding:10px; margin-bottom:0;" onclick="adicionarPacote()">Publicar Pacote no Site</button>
        </div>

        <button class="btn-opcao" style="background:#333;" onclick="voltarParaEscolha()">🚪 Sair / Voltar ao Início</button>
    </div>

    <!-- TELA 6: Confirmação de Idade Consumidor -->
    <div id="tela-idade-consumidor" class="container tela">
        <h2>⚠️ Confirmação de Idade (+18)</h2>
        <p>Este ambiente contém conteúdos restritos para maiores de 18 anos. Você confirma ter idade legal?</p>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-catalogo')">Sim, tenho 18 anos ou mais</button>
        <button class="btn-opcao" style="background:#d32f2f;" onclick="voltarParaEscolha()">Não, sair</button>
    </div>

    <!-- TELA 7: Catálogo de Consumidores (Lista os pacotes criados e o grupo VIP) -->
    <div id="tela-catalogo" class="container tela" style="max-width: 500px;">
        <h2>🔥 Diretório & Catálogo VIP</h2>
        <p style="margin-bottom:10px;">Área exclusiva para clientes e consumidores.</p>
        <button class="btn-opcao" style="background:#333; padding: 8px; margin-bottom:15px;" onclick="voltarParaEscolha()">🚪 Trocar de Perfil / Sair</button>
        
        <div class="product">
            <h3>🌟 Acesso Geral ao Grupo VIP</h3>
            <p>Acesso completo a todo o acervo principal liberado na nuvem.</p>
            <div class="price">R$ 10,00</div>
            <a href="https://link.mercadopago.com.br/SEU_LINK_AQUI" target="_blank" class="comprar">Comprar Acesso (R$ 10)</a>
        </div>

        <!-- Onde os pacotes criados pelas criadoras vão aparecer automaticamente -->
        <div id="lista-pacotes-dinamica"></div>
    </div>

    <script>
        function mostrarTela(idTela) {
            document.querySelectorAll('.tela').forEach(el => el.classList.remove('ativa'));
            document.getElementById(idTela).classList.add('ativa');
        }
        function irParaCriadorMenu() { mostrarTela('tela-criador-menu'); }
        function voltarParaEscolha() { mostrarTela('tela-escolha'); }
        
        function fazerLogin() {
            let email = document.getElementById('loginEmail').value;
            if(!email) { alert('Preencha seu e-mail!'); return; }
            document.getElementById('painelNomeCriadora').innerText = email.split('@')[0].toUpperCase();
            mostrarTela('tela-painel-criador');
        }

        function finalizarCadastro() {
            let nome = document.getElementById('novoNome').value;
            let email = document.getElementById('novoEmail').value;
            if(!nome || !email) { alert('Preencha pelo menos nome e e-mail!'); return; }
            document.getElementById('painelNomeCriadora').innerText = nome;
            alert('Cadastro realizado com sucesso! Bem-vinda ao seu painel.');
            mostrarTela('tela-painel-criador');
        }

        function atualizarFoto(event) {
            let reader = new FileReader();
            reader.onload = function(){
                document.getElementById('avatarPreview').src = reader.result;
            }
            reader.readAsDataURL(event.target.files[0]);
        }

        function adicionarPacote() {
            let titulo = document.getElementById('pacoteTitulo').value;
            let desc = document.getElementById('pacoteDesc').value;
            let preco = document.getElementById('pacotePreco').value;

            if(!titulo || !preco) {
                alert('Preencha pelo menos o título e o valor do pacote!');
                return;
            }

            let containerCatalogo = document.getElementById('lista-pacotes-dinamica');
            let novoCard = document.createElement('div');
            novoCard.className = 'product';
            novoCard.innerHTML = `
                <h3>📦 ${titulo}</h3>
                <p>${desc || 'Conteúdo exclusivo disponível.'}</p>
                <div class="price">R$ ${parseFloat(preco).toFixed(2)}</div>
                <a href="https://link.mercadopago.com.br/SEU_LINK_AQUI" target="_blank" class="comprar">Comprar Pacote (R$ ${preco})</a>
            `;
            containerCatalogo.appendChild(novoCard);

            alert('Pacote publicado com sucesso no catálogo do site!');
            document.getElementById('pacoteTitulo').value = '';
            document.getElementById('pacoteDesc').value = '';
            document.getElementById('pacotePreco').value = '';
        }
    </script>
</body>
</html>
"""

# Rota principal do site
@app.route('/')
def home():
    return SITE_HTML

# Rota do Webhook do Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        chat_id = data['message']['chat']['id']
        texto_recebido = data['message'].get('text', '')

        resposta = f"Olá! Recebi sua mensagem: '{texto_recebido}'. Acesse nosso site principal pelo link do Render."
        requests.post(TELEGRAM_URL, json={'chat_id': chat_id, 'text': resposta})

    return jsonify({"status": "ok"})

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
