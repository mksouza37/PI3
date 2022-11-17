from flaskblog import app 

def test_paginaInicial():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert 'Portal' in response.data.decode('utf-8')  

def test_criacaoNovaConta():
    response = app.test_client().get('/register')
    assert response.status_code == 200
    assert 'Crie sua conta agora!' in response.data.decode('utf-8')

def test_modificarInfosConta():
    response = app.test_client().get('/account')
    assert response.status_code == 302
    #assert 'Informações da Conta' in response.data.decode('utf-8') <== não consegue pq não há usuário autenticado
    #precisaria descobrir uma maneira de simular um usuário autenticado para fazer o teste.

def test_entrarNaConta():
    response = app.test_client().get('/login')
    assert response.status_code == 200
    assert 'Acessar a Conta' in response.data.decode('utf-8')

def test_sairdaConta():
    response = app.test_client().get('/logout')
    assert response.status_code == 302
    assert 'forum' in response.data.decode('utf-8')

def test_consultaCertificado():
    response = app.test_client().get('/consulta')
    assert response.status_code == 200
    assert 'Status do Certificado Ambiental no IBAMA' in response.data.decode('utf-8')

def test_consultaBlog():
    response = app.test_client().get('/blog')
    assert response.status_code == 200
    assert 'Bem vindo ao Blog do Pesque Bem!' in response.data.decode('utf-8')

def test_consultaForum():
    response = app.test_client().get('/forum')
    assert response.status_code == 200
    assert 'Bem vindo ao Fórum do Pesque Bem!' in response.data.decode('utf-8')

def test_novaPostagem():
    response = app.test_client().get('/post/new')
    assert response.status_code == 302
    #assert 'Nova Postagem' in response.data.decode('utf-8') <== não consegue pq não há usuário autenticado e ele tem login.required
    #precisaria descobrir uma maneira de simular um usuário autenticado para fazer o teste.
    #O mesmo acontece para os testes 10 a 15. Vão retornar 302 por conta do login.required.

def test_consultaLegislacao():
    response = app.test_client().get('/leis')
    assert response.status_code == 200
    assert 'Essa página relaciona todas as proposições' in response.data.decode('utf-8')

    #como testar o script que busca a legislação no congresso?

def test_noticias():
    response = app.test_client().get('/noticias')
    assert response.status_code == 200
    assert 'Mantenha-se bem informado' in response.data.decode('utf-8')

def test_estatisticas():
    response = app.test_client().get('/estatisticas')
    assert response.status_code == 200
    assert 'Como está a distribuição' in response.data.decode('utf-8')

def test_acessibilidade():
    response = app.test_client().get('/acessibilidade')
    assert response.status_code == 200
    assert 'Sugestões de Ferramentas de Acesso' in response.data.decode('utf-8')

    #como testar se a ferramenta libras está funcionando?

def test_segestoes():
    response = app.test_client().get('/sugest')
    assert response.status_code == 200
    assert 'Envie aqui Sugestões e Comentários para o Portal' in response.data.decode('utf-8')

def test_consultaMuralAnuncios():
    response = app.test_client().get('/mural')
    assert response.status_code == 200
    assert 'Aproveite as oportunidades de negócios' in response.data.decode('utf-8')

def test_incluiAnuncio():
    response = app.test_client().get('/postaAnuncio')
    assert response.status_code == 302
    #mesma questão do inclusão de novo post. ele redireciona porque não há usuário logado.

def test_excluiAnuncio():
    response = app.test_client().get('/desabilitaanuncio')
    assert response.status_code == 302
    #mesma questão do inclusão de novo post. ele redireciona porque não há usuário logado.

def test_APIinfos():
    response = app.test_client().get('/apiInfos')
    assert response.status_code == 200
    assert 'Bem vindo a API do Portal Pesque Bem.' in response.data.decode('utf-8')

    #como testar o mapa coropletico?





    




    









