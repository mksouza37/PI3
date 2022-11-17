import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, SugestForm, PostaAnuncioForm, DesabilitaAnuncioForm
from flaskblog.models import User, Post, empresas, Postblog, Legislacao, Noticias, Anuncio
from flask_login import login_user, current_user, logout_user, login_required
import json
import pandas as pd
from urllib.request import urlopen
import folium
import geopandas as gpd
import webbrowser
import base64

@app.route("/")
def index():
    return render_template('index.html', title='Pesque Bem')

@app.route('/consulta')
def consulta():
    emps = empresas.query.all()
    return render_template('consulta.html',  posts=emps, title='Certificação')

@app.route("/blog")
def blog():
    postsbl = Postblog.query.all()
    print(postsbl)
    return render_template('blog.html', postsbl=postsbl, title='Blog')

@app.route("/forum")
def forum():
    posts = Post.query.all()
    return render_template('forum.html', posts=posts, title='Fórum')

@app.route("/leis")
def leis():
    legs = Legislacao.query.all()
    return render_template('leis.html',  posts=legs,  title='Legislação')

@app.route("/noticias")
def noticias():
    notic = Noticias.query.all()
    return render_template('noticias.html', posts=notic, title='Notícias')

@app.route("/estatisticas")
def estatisticas():
    return render_template('estatisticas.html', title='Estatísticas')

@app.route("/estTam")
def estTam():
    return render_template('estTam.html', title='Estudo')

@app.route("/mapa")
def mapa():

    estados = gpd.read_file(app.open_resource('static/CloroMap/countries.geojson'))
    
    response = urlopen("http://127.0.0.1:5000/api?SEL=todos")
    data_json = json.loads(response.read())
    df = pd.DataFrame (data_json, columns = ['conduta','ramo','estado'])

    est = df.groupby(['estado']).count()['ramo']
    cond_est = df.groupby(['conduta','estado']).count()
    bNE = cond_est.query("conduta == 'CNPJ não encontrado nos registros do IBAMA.'")['ramo'].droplevel(0)
    bPO = cond_est.query("conduta == 'Possui certificado ambiental.'")['ramo'].droplevel(0)
    bNP = cond_est.query("conduta == 'Não possui certificado ambiental.'")['ramo'].droplevel(0)

    cons = pd.concat([est,bNE, bPO, bNP], axis=1).reset_index(level=0).fillna(0)
    cons.columns=['ESTADO','Total de Empresas','CNPJ não encontrado na base do Ibama','Possui certificado','Não possui certificado']

    estados = gpd.GeoDataFrame(estados, geometry='geometry')
    estados.crs = 'epsg:4326'
    estados = estados.merge(cons, on='ESTADO')

    BR_LAT = -14.235
    BR_LON = -51.9253

    mapa = folium.Map(location=[BR_LAT,BR_LON], control_scale = True, zoom_start=5, tiles='cartodbpositron')

    coropletico = folium.Choropleth(
        geo_data=estados,
        data=estados,
        columns=['ESTADO','Total de Empresas','CNPJ não encontrado na base do Ibama','Possui certificado','Não possui certificado'],
        key_on='feature.properties.ESTADO',
        legend_name='Número de Empresas por Estado (grupo das 500 maiores)',
        fill_color = 'YlOrRd'
    ).add_to(mapa)

    coropletico.geojson.add_child(
        folium.features.GeoJsonTooltip(['ESTADO','Total de Empresas','CNPJ não encontrado na base do Ibama','Possui certificado','Não possui certificado'])
    )

    output_file = "Empresas por Estado.html"
    mapa.save(output_file)
    webbrowser.open(output_file, new=2)

    return render_template('estatisticas.html', title='Estatísticas')

@app.route("/apiInfos")
def apiInfos():
    return render_template('apiInfos.html', title='Informações da API')

@app.route('/api')
def api():
    SEL = request.args.get('SEL')
    CNPJ = request.args.get('CNPJ')
    EST = request.args.get('EST')

    teste = ((SEL != None)*1) + ((CNPJ !=None)*1) + ((EST!=None)*1)
    
    if (teste != 1):

        return "<h2><br><br> ***  ERRO: endereço utilizado inválido. Consulte as instruções da API e verifique as alternativas válidas para consulta. ***</h2>",404

    elif SEL != None:

        if SEL == 'todos':

            emps = empresas.query.all()
            emps2=[]
            for item in emps:
                emps2.append(item.to_dict())
            return json.dumps(emps2,ensure_ascii=False)

        else:
        
            return "<h2><br><br> ***  ERRO: Preenchimento do parâmetro SEL inválido. Consulte as instruções da API e verifique as alternativas válidas para esse parâmetro. ***</h2>",404

    elif EST != None:

        estados = ['TO','SE','SP','SC','RR','RO','RS','RN','RJ','PI','PE','PR','PB','PA','MG','MS','MT','MA','GO','ES','DF','CE','BA','AM','AP','AL','AC'] 

        if EST in estados:

            emps = empresas.query.filter_by(estado=EST)
            emps2=[]
            for item in emps:
                emps2.append(item.to_dict())
            return json.dumps(emps2,ensure_ascii=False)

        else:
        
            return "<h2><br><br> ***  ERRO: Preenchimento do parâmetro EST inválido. Consulte as instruções da API e verifique as alternativas válidas para esse parâmetro. ***</h2>",404

    elif CNPJ != None:

        #MELHORAR: incluir validador de CNPJ

        emps = empresas.query.filter_by(cnpj=CNPJ).first()

        if(emps != None):
            
            emps = emps.to_dict()
            return json.dumps(emps,ensure_ascii=False)

        else:
            return "<h2><br><br> ***  CNPJ não encontrado. ***</h2>"


@app.route("/mural")
def mural():
    
    empr = Anuncio.query.filter_by(statusvigencia = 'sim').all()
    print(empr is None)
    empr[0].foto2 = 'data:image/png;base64, '+str(empr[0].foto)[2:-1]
    for n in range(1,len(empr)):
            empr[n].foto2 = 'data:image/png;base64, '+str(empr[n].foto)[2:-1]
            
    return render_template('mural.html',  posts=empr, title='Mural de Vendas')


@app.route("/postaAnuncio", methods=['GET', 'POST'])
@login_required
def postaAnuncio():
    
        form = PostaAnuncioForm()
        if form.validate_on_submit():

            rosto = base64.b64encode(form.foto.data.read())
            post = Anuncio(foto=rosto, titulo=form.titulo.data, texto=form.texto.data,
                           dt_inclusao=form.dt_inclusao.data, nomeAnunciante=form.nomeAnunciante.data,
                           cidade=form.cidade.data, estado=form.estado.data, telcont=form.telcont.data,
                           usuarioCad=current_user.email, statusvigencia='sim')
            db.session.add(post)
            db.session.commit()
            flash('Seu anúncio foi postado!', 'success')
            return redirect(url_for('mural'))
        
            
        return render_template('PostaAnuncio.html', title='Inclusão de Novo Anúncio',
                               form=form, legend='Novo Anúncio')


@app.route("/desabilitaanuncio", methods=['GET', 'POST'])
@login_required
def desabilitaanuncio():

    form = DesabilitaAnuncioForm()
    
    if form.validate_on_submit():
        
        anun_desab = Anuncio.query.filter_by(id=form.numero.data).first()

        if(anun_desab != None):

            if (anun_desab.usuarioCad == current_user.email):
                anun_desab.statusvigencia='nao'
                db.session.commit()
                flash('Seu anúncio foi desabilitado!', 'success')
                return redirect(url_for('mural'))

            else:
                return "<h2><br><br> ***  Atenção  ***<br><br> O anúncio informado não pertence ao usuário.<br><br>Clicar no botão Voltare e informar um número de anúncio válido.</h2>"
                
        else:
            return "<h2><br><br> ***  Anúncio não encontrado.<br><br>Clicar no botão Voltar e informar um número de anúncio válido. ***</h2>"
                            
    return render_template('desabilitaAnuncio.html', title='Desabilitar Anúncio',
                                     form=form, legend='Desabilitar Anúncio')

@app.route("/sugest", methods=['GET', 'POST'])
def sugest():
    return render_template('sugest.html', title='Sugestões')

	
@app.route("/acessibilidade")
def acessibilidade():
    return render_template('acessibilidade.html', title='Acessibilidade')

@app.route('/sw')
def serviceworker():
    from flask import make_response, send_from_directory
    #response = make_response(send_from_directory('static',filename='service_worker.js'))
    response = make_response(app.send_static_file('sw.js'))    
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada! Você já pode acessa-la', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrar', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forum'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('forum'))
        else:
            flash('Acesso negado. Por favor, cheque e-mail e senha', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('forum'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Sua conta foi atualizada!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Conta',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    
        form = PostForm()
        if form.validate_on_submit():
            if (current_user.username != 'AdmBlog'):
                post = Post(title=form.title.data, content=form.content.data, author=current_user)
            else:
                post = Postblog(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Sua postagem foi criada!', 'success')
            if (current_user.username != 'AdmBlog'):            
                return redirect(url_for('forum'))
            else:
                return redirect(url_for('blog'))
            
        return render_template('create_post.html', title='Nova Postagem',
                               form=form, legend='Nova Postagem')

@app.route("/post/<int:post_id>")
def post(post_id):
    if (current_user.username != 'AdmBlog'):
        post = Post.query.get_or_404(post_id)
    else:
        post = Postblog.query.get_or_404(post_id)
    
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    if (current_user.username != 'AdmBlog'):    
        post = Post.query.get_or_404(post_id)
    else:
        post = Postblog.query.get_or_404(post_id)    
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Sua postagem foi atualizada!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Atualizar Postagem',
                           form=form, legend='Atualizar Postagem')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    if (current_user.username != 'AdmBlog'):
        post = Post.query.get_or_404(post_id)
    else:
        post = Postblog.query.get_or_404(post_id)    
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Seu post foi apagado!', 'success')
    if (current_user.username != 'AdmBlog'):            
        return redirect(url_for('forum'))
    else:
        return redirect(url_for('blog'))





