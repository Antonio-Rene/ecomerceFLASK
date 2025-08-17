from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/usuarios')
def usuarios():
    return "Página de usuários"

@app.route('/anuncios')
def anuncios():
    return "Página de anúncios"

@app.route('/compras')
def compras():
    return "Página de compras"

@app.route('/vendas')
def vendas():
    return "Página de vendas"

if __name__ == '__main__':
    app.run(debug=True)