from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SECRET_KEY'] = 'chave-secreta'
db = SQLAlchemy(app)


# CONFIGURA LOGIN

login_manager = LoginManager(app)
login_manager.login_view = "login"


# MODELOS

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    usuario = db.relationship("Usuario", backref="anuncios")

with app.app_context():
    db.create_all()


# LOGIN 

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# ROTES USUÁRIO

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado!")
            return redirect(url_for("cadastro"))

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        flash("Usuário cadastrado com sucesso! Faça login.")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            flash("Login realizado com sucesso!")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha inválidos.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado!")
    return redirect(url_for("index"))


# ROTAS PRINCIPAIS

@app.route("/")
def index():
    return render_template("index.html")


# CRUD ANÚNCIOS

@app.route("/anuncios")
@login_required
def lista_anuncios():
    anuncios = Anuncio.query.all()
    return render_template("anuncios.html", anuncios=anuncios)

@app.route("/anuncios/novo", methods=["GET", "POST"])
@login_required
def novo_anuncio():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        preco = request.form["preco"]
        anuncio = Anuncio(titulo=titulo, descricao=descricao, preco=preco, usuario=current_user)
        db.session.add(anuncio)
        db.session.commit()
        flash("Anúncio criado com sucesso!")
        return redirect(url_for("lista_anuncios"))
    return render_template("anuncio_form.html", anuncio=None)

@app.route("/anuncios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != current_user.id:
        flash("Você não tem permissão para editar este anúncio!")
        return redirect(url_for("lista_anuncios"))

    if request.method == "POST":
        anuncio.titulo = request.form["titulo"]
        anuncio.descricao = request.form["descricao"]
        anuncio.preco = request.form["preco"]
        db.session.commit()
        flash("Anúncio atualizado com sucesso!")
        return redirect(url_for("lista_anuncios"))
    return render_template("anuncio_form.html", anuncio=anuncio)

@app.route("/anuncios/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != current_user.id:
        flash("Você não tem permissão para excluir este anúncio!")
        return redirect(url_for("lista_anuncios"))

    db.session.delete(anuncio)
    db.session.commit()
    flash("Anúncio excluído com sucesso!")
    return redirect(url_for("lista_anuncios"))

if __name__ == "__main__":
    app.run(debug=True)
