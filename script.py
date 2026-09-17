import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "7139961367:AAH604l5jQ830YeeMFCcflqBgugln3Zadsc"
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
MP_ACCESS_TOKEN = "APP_USR-6787238743343148-091523-7de483b0fa92f00855ab3523599f0995-175404649"

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
        .profile-card { background: #2a2a2a; border: 1px solid #333; padding: 12px; margin: 10px 0; border-radius: 8px; display: flex; align-items: center; cursor: pointer; text-align: left; }
        .profile-card:hover { border-color: #ff4081; }
        .profile-thumb { width: 60px; height: 60px; border-radius: 50%; object-fit: cover; margin-right: 15px; border: 2px solid #ff4081; }
        .product { background: #2a2a2a; border: 1px solid #333; padding: 12px; margin: 10px 0; border-radius: 8px; text-align: left; }
        .price { color: #00e676; font-weight: bold; font-size: 15px; margin-bottom: 8px; }
        a.comprar { background: #ff4081; color: white; border: none; padding: 10px 12px; width: 100%; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; display: block; text-align: center; text-decoration: none; box-sizing: border-box; }
        a.comprar:hover { background: #e91e63; }
        .avatar-preview { width: 80px; height: 80px; border-radius: 50%; background: #333; margin: 0 auto 15px auto; display: block; object-fit: cover; border: 2px solid #ff4081; }
    </style>
</head>
<body>

    <!-- TELA 1: Escolha Principal -->
    <div id="tela-escolha" class="container ativa">
        <h2>🔥 Agência Bot</h2>
        <p>Selecione o seu perfil de acesso:</p>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-criador-menu')">👩‍🦰 Sou Criador(a) / Profissional</button>
        <button class="btn-opcao" onclick="mostrarTela('tela-idade-consumidor')">🛍️ Sou Consumidor(a) / Cliente</button>
    </div>

    <!-- TELA 2: Menu Criadoras -->
    <div id="tela-criador-menu" class="container tela">
        <h2>Painel de Criadoras</h2>
        <p>Gerencie seu perfil, monte pacotes ou cadastre seus locais de atendimento (Jobs).</p>
        <button class="btn-opcao" onclick="mostrarTela('tela-login')">🔑 Já tenho cadastro (Login)</button>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-cadastro-criador')">📝 Quero me cadastrar</button>
        <button class="btn-opcao" style="background:#333; margin-top:20px;" onclick="voltarParaEscolha()">⬅ Voltar</button>
    </div>

    <!-- TELA 3: Login Criadora -->
    <div id="tela-login" class="container tela">
        <h2>Login de Criadora</h2>
        <div class="form-group">
            <label>E-mail:</label>
            <input type="email" id="loginEmail" class="form-control" placeholder="seu@email.com">
        </div>
        <div class="form-group">
            <label>Senha:</label>
            <input type="password" id="loginPass" class="form-control" placeholder="********">
        </div>
        <button class="btn-opcao btn-destaque" onclick="fazerLogin()">Entrar no Painel</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <!-- TELA 4: Cadastro Completo Criadora / Job -->
    <div id="tela-cadastro-criador" class="container tela">
        <h2>Cadastro Profissional</h2>
        <div class="aviso-legal">
            🔒 Informe seus dados de atuação para aparecer no diretório do site.
        </div>
        <div class="form-group">
            <label>Nome Artístico:</label>
            <input type="text" id="novoNome" class="form-control" placeholder="Seu nome ou apelido">
        </div>
        <div class="form-group">
            <label>E-mail:</label>
            <input type="email" id="novoEmail" class="form-control" placeholder="email@dominio.com">
        </div>
        <div class="form-group">
            <label>Categoria de Atuação:</label>
            <select id="novoCategoria" class="form-control">
                <option value="conteudo">Apenas Conteúdo Digital</option>
                <option value="job">Apenas Job / Acompanhante Presencial</option>
                <option value="ambos">Conteúdo + Job (Ambos)</option>
            </select>
        </div>
        <div class="form-group">
            <label>Local / Região de Atendimento (para Jobs):</label>
            <input type="text" id="novoLocal" class="form-control" placeholder="Ex: Birigui - SP e região">
        </div>
        <div class="form-group">
            <label>Descrição / Sobre mim:</label>
            <input type="text" id="novoDesc" class="form-control" placeholder="Conte o que oferece...">
        </div>
        <div class="form-group">
            <label>Foto de Perfil (Avatar):</label>
            <input type="file" id="novoFoto" class="form-control" accept="image/*">
        </div>
        <div class="form-group">
            <label>Senha:</label>
            <input type="password" id="novoSenha" class="form-control" placeholder="Mínimo 6 dígitos">
        </div>
        <button class="btn-opcao btn-destaque" onclick="salvarCadastroCriadora()">Concluir e Abrir Painel</button>
        <button class="btn-opcao" style="background:#333;" onclick="mostrarTela('tela-criador-menu')">Voltar</button>
    </div>

    <!-- TELA 5: Painel da Criadora (Criar Pacotes e Vitrine) -->
    <div id="tela-painel-criador" class="container tela" style="max-width: 520px;">
        <h2>✨ Meu Painel Profissional</h2>
        <div style="text-align: center; margin-bottom: 15px;">
            <img id="painelAvatar" src="https://via.placeholder.com/80" class="avatar-preview" alt="Avatar">
            <h3 id="painelNome" style="margin:5px 0; color:#fff;">Criadora</h3>
            <p style="margin:0; font-size:12px; color:#00e676;">Ativo no Diretório Oficial</p>
        </div>

        <div class="info-box">
            💡 <b>Taxa da Plataforma:</b> Incide apenas <b>1% de comissão</b> sobre os pacotes vendidos avulsos no site.
        </div>

        <div style="background: #2a2a2a; padding: 12px; border-radius: 8px; margin-bottom: 15px;">
            <h3 style="font-size: 14px; margin-top:0; color:#ff4081;">📦 Criar Pacote de Conteúdo</h3>
            <div class="form-group"><label>Título:</label><input type="text" id="pTitulo" class="form-control" placeholder="Ex: Pack VIP Fotos"></div>
            <div class="form-group"><label>Valor (R$):</label><input type="number" id="pPreco" class="form-control" placeholder="20.00"></div>
            <button class="btn-opcao btn-destaque" style="padding:10px; margin-bottom:0;" onclick="adicionarPacoteCriadora()">Publicar no Catálogo</button>
        </div>

        <button class="btn-opcao" style="background:#333;" onclick="voltarParaEscolha()">🚪 Sair</button>
    </div>

    <!-- TELA 6: Verificação +18 Consumidor -->
    <div id="tela-idade-consumidor" class="container tela">
        <h2>⚠️ Confirmação de Idade (+18)</h2>
        <p>Conteúdo exclusivo para maiores de idade. Confirma?</p>
        <button class="btn-opcao btn-destaque" onclick="mostrarTela('tela-cliente-menu')">Sim, tenho 18 anos</button>
        <button class="btn-opcao" style="background:#d32f2f;" onclick="voltarParaEscolha()">Não</button>
    </div>

    <!-- TELA 7: Menu do Cliente (Escolhe Grupo VIP ou Criadoras A-Z) -->
    <div id="tela-cliente-menu" class="container tela">
        <h2>🛍️ Área do Consumidor</h2>
        <p>O que você deseja acessar hoje?</p>
        
        <div class="product" style="border-color:#ff4081; text-align:center;">
            <h3>🌟 Acesso Geral ao Grupo VIP</h3>
            <p>Todo o acervo principal liberado na nuvem.</p>
            <div class="price">R$ 10,00</div>
            <!-- Substitua pelo link real da sua caixinha do Mercado Pago quando quiser -->
            <a href="https://link.mercadopago.com.br/SEU_LINK_AQUI" target="_blank" class="comprar">Comprar Grupo VIP</a>
        </div>

        <button class="btn-opcao btn-destaque" style="margin-top:15px;" onclick="abrirCatalogoCriadoras('conteudo')">📁 Catálogo de Conteúdos (A-Z)</button>
        <button class="btn-opcao btn-destaque" onclick="abrirCatalogoCriadoras('job')">💎 Catálogo de Jobs / Presencial (A-Z)</button>
        <button class="btn-opcao" style="background:#333; margin-top:10px;" onclick="voltarParaEscolha()">⬅ Voltar</button>
    </div>

    <!-- TELA 8: Listagem de Criadoras de A a Z -->
    <div id="tela-catalogo-criadoras" class="container tela">
        <h2 id="tituloCatalogoCriadoras">Diretório de Criadoras</h2>
        <p>Clique em uma criadora para ver detalhes, fotos e locais de atendimento:</p>
        <div id="listaCriadorasAZ"></div>
        <button class="btn-opcao" style="background:#333; margin-top:15px;" onclick="mostrarTela('tela-cliente-menu')">⬅ Voltar</button>
    </div>

    <!-- TELA 9: Perfil Detalhado da Criadora para o Cliente -->
    <div id="tela-perfil-detalhe" class="container tela">
        <div style="text-align:center;">
            <img id="detalheFoto" src="https://via.placeholder.com/90" class="avatar-preview" alt="Foto">
            <h2 id="detalheNome" style="margin:5px 0; color:#ff4081;">Nome</h2>
            <p id="detalheCategoria" style="color:#00e676; font-size:13px; font-weight:bold;"></p>
        </div>
        <div style="background:#2a2a2a; padding:12px; border-radius:8px; margin:10px 0;">
            <p style="text-align:left; margin:0 0 8px 0; font-size:13px;"><b>📍 Local / Atendimento:</b> <span id="detalheLocal">-</span></p>
            <p style="text-align:left; margin:0; font-size:13px;"><b>💬 Sobre:</b> <span id="detalheDesc">-</span></p>
        </div>
        <div id="detalhePacotesContainer"></div>
        <button class="btn-opcao" style="background:#333; margin-top:15px;" onclick="mostrarTela('tela-catalogo-criadoras')">⬅ Voltar ao Diretório</button>
    </div>

    <script>
        // Banco de dados em memória do site
        let criadorasBD = [
            { nome: "Amanda S.", categoria: "ambos", local: "Birigui e Araçatuba - SP", desc: "Conteúdos diários e disponibilidade para atendimento VIP.", foto: "https://via.placeholder.com/80", pacotes: [{ titulo: "Pack Exclusivo 20 Fotos", preco: "25.00" }] },
            { nome: "Bruna Lima", categoria: "conteudo", local: "Online / Todo o Brasil", desc: "Especialista em packs personalizados e vídeos sob encomenda.", foto: "https://via.placeholder.com/80", pacotes: [{ titulo: "Vídeo Privado 10min", preco: "40.00" }] },
            { nome: "Carla Duarte", categoria: "job", local: "Birigui - SP", desc: "Acompanhante para eventos e encontros selecionados.", foto: "https://via.placeholder.com/80", pacotes: [] }
        ];

        let criadoraLogadaIndex = null;

        function mostrarTela(idTela) {
            document.querySelectorAll('.tela').forEach(el => el.classList.remove('ativa'));
            document.getElementById(idTela).classList.add('ativa');
        }
        function voltarParaEscolha() { mostrarTela('tela-escolha'); }

        function fazerLogin() {
            let email = document.getElementById('loginEmail').value;
            if(!email) { alert('Digite seu e-mail!'); return; }
            criadoraLogadaIndex = 0; // Exemplo padrão
            document.getElementById('painelNome').innerText = email.split('@')[0].toUpperCase();
            mostrarTela('tela-painel-criador');
        }

        function salvarCadastroCriadora() {
            let nome = document.getElementById('novoNome').value;
            let email = document.getElementById('novoEmail').value;
            let cat = document.getElementById('novoCategoria').value;
            let local = document.getElementById('novoLocal').value;
            let desc = document.getElementById('novoDesc').value;

            if(!nome || !email) { alert('Preencha os campos obrigatórios!'); return; }

            let nova = { nome: nome, categoria: cat, local: local || 'Não informado', desc: desc || 'Sem descrição', foto: "https://via.placeholder.com/80", pacotes: [] };
            criadorasBD.push(nova);
            criadoraLogadaIndex = criadorasBD.length - 1;

            document.getElementById('painelNome').innerText = nome;
            alert('Cadastro concluído com sucesso!');
            mostrarTela('tela-painel-criador');
        }

        function adicionarPacoteCriadora() {
            let titulo = document.getElementById('pTitulo').value;
            let preco = document.getElementById('pPreco').value;
            if(!titulo || !preco) { alert('Preencha o título e o valor!'); return; }

            if(criadoraLogadaIndex !== null) {
                criadorasBD[criadoraLogadaIndex].pacotes.push({ titulo: titulo, preco: preco });
                alert('Pacote publicado com sucesso no seu perfil!');
                document.getElementById('pTitulo').value = '';
                document.getElementById('pPreco').value = '';
            }
        }

        function abrirCatalogoCriadoras(tipoFiltro) {
            let tituloEl = document.getElementById('tituloCatalogoCriadoras');
            tituloEl.innerText = tipoFiltro === 'conteudo' ? '📁 Catálogo de Conteúdos (A-Z)' : '💎 Catálogo de Jobs / Presencial (A-Z)';
            
            let listaEl = document.getElementById('listaCriadorasAZ');
            listaEl.innerHTML = '';

            // Ordena de A a Z pelo nome
            let filtradas = criadorasBD.filter(c => tipoFiltro === 'ambos' || c.categoria === tipoFiltro || c.categoria === 'ambos');
            filtradas.sort((a, b) => a.nome.localeCompare(b.nome));

            if(filtradas.length === 0) {
                listaEl.innerHTML = '<p style="color:#b0bec5; text-align:center;">Nenhuma criadora encontrada nesta categoria.</p>';
            } else {
                filtradas.forEach(c => {
                    let card = document.createElement('div');
                    card.className = 'profile-card';
                    card.innerHTML = `
                        <img src="${c.foto}" class="profile-thumb">
                        <div>
                            <h3 style="margin:0 0 5px 0; color:#fff; font-size:16px;">${c.nome}</h3>
                            <p style="margin:0; font-size:12px; color:#b0bec5;">📍 ${c.local}</p>
                        </div>
                    `;
                    card.onclick = () => verPerfilDetalhe(c);
                    listaEl.appendChild(card);
                });
            }
            mostrarTela('tela-catalogo-criadoras');
        }

        function verPerfilDetalhe(c) {
            document.getElementById('detalheNome').innerText = c.nome;
            document.getElementById('detalheCategoria').innerText = c.categoria.toUpperCase();
            document.getElementById('detalheLocal').innerText = c.local;
            document.getElementById('detalheDesc').innerText = c.desc;
            document.getElementById('detalheFoto').src = c.foto;

            let pacContainer = document.getElementById('detalhePacotesContainer');
            pacContainer.innerHTML = '<h3 style="font-size:14px; color:#ff4081; text-align:left; margin-top:15px;">Pacotes e Serviços Disponíveis:</h3>';

            if(c.pacotes.length === 0) {
                pacContainer.innerHTML += '<p style="font-size:13px; color:#b0bec5; text-align:left;">Nenhum pacote avulso cadastrado no momento.</p>';
            } else {
                c.pacotes.forEach(p => {
                    pacContainer.innerHTML += `
                        <div class="product">
                            <h3>📦 ${p.titulo}</h3>
                            <div class="price">R$ ${parseFloat(p.preco).toFixed(2)}</div>
                            <a href="https://link.mercadopago.com.br/SEU_LINK_AQUI" target="_blank" class="comprar">Comprar por R$ ${p.preco}</a>
                        </div>
                    `;
                });
            }
            mostrarTela('tela-perfil-detalhe');
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
        resposta = f"Olá! Recebi sua mensagem: '{texto_recebido}'. Acesse nosso site principal pelo link do Render."
        requests.post(TELEGRAM_URL, json={'chat_id': chat_id, 'text': resposta})
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    porta = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=porta)
