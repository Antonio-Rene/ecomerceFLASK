\
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SECRET_KEY'] = 'mude-esta-chave-secreta'
db = SQLAlchemy(app)

# ------------------------------
# Login config
# ------------------------------
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

# ------------------------------
# Models
# ------------------------------
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    def set_senha(self, senha): self.senha_hash = generate_password_hash(senha)
    def check_senha(self, senha): return check_password_hash(self.senha_hash, senha)

class Anuncio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    usuario = db.relationship("Usuario", backref="anuncios")

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ------------------------------
# Public pages
# ------------------------------
@app.route("/")
def index():
    anuncios = Anuncio.query.order_by(Anuncio.id.desc()).all()
    return render_template("index.html", anuncios=anuncios)

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]
        if Usuario.query.filter_by(email=email).first():
            flash("Email já cadastrado!", "danger")
            return redirect(url_for("cadastro"))
        u = Usuario(nome=nome, email=email)
        u.set_senha(senha)
        db.session.add(u)
        db.session.commit()
        flash("Usuário cadastrado! Faça login.", "success")
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        senha = request.form["senha"]
        u = Usuario.query.filter_by(email=email).first()
        if u and u.check_senha(senha):
            login_user(u, remember=True)
            flash("Login realizado!", "success")
            return redirect(url_for("lista_anuncios"))
        flash("Email ou senha inválidos.", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado!", "info")
    return redirect(url_for("index"))

# ------------------------------
# Protected: CRUD Anúncios
# ------------------------------
@app.route("/anuncios")
@login_required
def lista_anuncios():
    anuncios = Anuncio.query.order_by(Anuncio.id.desc()).all()
    return render_template("anuncios.html", anuncios=anuncios)

@app.route("/anuncios/novo", methods=["GET", "POST"])
@login_required
def novo_anuncio():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        descricao = request.form["descricao"].strip()
        preco = float(request.form["preco"])
        a = Anuncio(titulo=titulo, descricao=descricao, preco=preco, usuario=current_user)
        db.session.add(a)
        db.session.commit()
        flash("Anúncio criado!", "success")
        return redirect(url_for("lista_anuncios"))
    return render_template("anuncio_form.html", anuncio=None)

@app.route("/anuncios/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_anuncio(id):
    a = Anuncio.query.get_or_404(id)
    if a.usuario_id != current_user.id:
        flash("Sem permissão para editar este anúncio.", "danger")
        return redirect(url_for("lista_anuncios"))
    if request.method == "POST":
        a.titulo = request.form["titulo"].strip()
        a.descricao = request.form["descricao"].strip()
        a.preco = float(request.form["preco"])
        db.session.commit()
        flash("Anúncio atualizado!", "success")
        return redirect(url_for("lista_anuncios"))
    return render_template("anuncio_form.html", anuncio=a)

@app.route("/anuncios/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_anuncio(id):
    a = Anuncio.query.get_or_404(id)
    if a.usuario_id != current_user.id:
        flash("Sem permissão para excluir este anúncio.", "danger")
        return redirect(url_for("lista_anuncios"))
    db.session.delete(a)
    db.session.commit()
    flash("Anúncio excluído!", "info")
    return redirect(url_for("lista_anuncios"))

# Helper for footer docs
@app.context_processor
def inject_access():
    return dict(PUBLIC_PAGES=["/", "/login", "/cadastro"],
                PROTECTED_PAGES=["/anuncios", "/anuncios/novo", "/anuncios/editar/<id>", "/anuncios/excluir/<id>", "/logout"])

if __name__ == "__main__":
    app.run(debug=True)
