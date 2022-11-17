from flaskblog.models import Anuncio, User, Noticias, Post, Postblog, empresas, Legislacao

def test_novo_anuncio():

    post = Anuncio(titulo='a', texto='a', dt_inclusao='a', nomeAnunciante='a', cidade='a', estado='a', telcont='a', usuarioCad='a', statusvigencia='sim')

    assert post.titulo == 'a'
    assert post.texto == 'a'
    assert post.dt_inclusao == 'a'
    assert post.nomeAnunciante == 'a'
    assert post.cidade == 'a'
    assert post.estado == 'a'
    assert post.telcont == 'a'
    assert post.usuarioCad == 'a'
    assert post.statusvigencia == 'sim'

def test_novo_Usuario():

    usuario = User(username = 'a', email = 'a', image_file = 'a.jpg', password = 'a')
    
    assert usuario.username == 'a'
    assert usuario.email == 'a'
    assert usuario.image_file == 'a.jpg'
    assert usuario.password == 'a'

#como testar o relacionamento da tabela user com as tabelas Post e Postblog?

def test_NovaPostagem():

    post = Post(title = 'a', date_posted = '01/01/22', content = 'a', user_id = 1)
    
    assert post.title == 'a'
    assert post.date_posted == '01/01/22'
    assert post.content == 'a'
    assert post.user_id == 1

#aparentemente ele não verifica o tipo de dado (ex.: aceita int onde deveria ser string). pq?

def test_NovaPostagem_Blog():

    postB = Postblog(title = 'a', date_posted = '01/01/22', content = 'a', user_id = 1)
    
    assert postB.title == 'a'
    assert postB.date_posted == '01/01/22'
    assert postB.content == 'a'
    assert postB.user_id == 1

def test_NovaEmpresa():

    emp = empresas(nome = 'a', cnpj = '02308994000133', cidade = 'a', estado = 'a', ramo = 'a', conduta = 'a')
    
    assert emp.nome == 'a'
    assert emp.cnpj == '02308994000133'
    assert emp.cidade == 'a'
    assert emp.estado == 'a'
    assert emp.ramo == 'a'
    assert emp.conduta == 'a'

def test_Noticia():
    
    noticia = Noticias(dataPub='a', titulo='a', link='a.www')

    assert noticia.dataPub == 'a'
    assert noticia.titulo == 'a'
    assert noticia.link == 'a.www'

def test_Legislação():

    lei = Legislacao(ident = 1, siglaTipo = 'a', ano = 2022, ementa = 'a', uri = 'a')
    
    assert lei.ident == 1
    assert lei.siglaTipo == 'a'
    assert lei.ano == 2022
    assert lei.ementa == 'a'
    assert lei.uri == 'a'
