from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Substitua por uma chave secreta real

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///loja.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definindo os modelos
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(100), nullable=False)

class Carrinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    produto = db.relationship('Produto', backref='carrinhos')

@app.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar_ao_carrinho/<int:produto_id>')
def adicionar_ao_carrinho(produto_id):
    produto = Produto.query.get_or_404(produto_id)

    if 'carrinho' not in session:
        session['carrinho'] = {}

    if produto_id in session['carrinho']:
        session['carrinho'][produto_id] += 1
    else:
        session['carrinho'][produto_id] = 1

    session.modified = True
    return redirect(url_for('index'))

@app.route('/carrinho')
def carrinho():
    itens_carrinho = []
    if 'carrinho' in session:
        for produto_id, quantidade in session['carrinho'].items():
            produto = Produto.query.get(produto_id)
            if produto:
                itens_carrinho.append({
                    'produto': produto,
                    'quantidade': quantidade
                })
    return render_template('carrinho.html', itens_carrinho=itens_carrinho)

@app.route('/remover_do_carrinho/<int:produto_id>')
def remover_do_carrinho(produto_id):
    if 'carrinho' in session:
        session['carrinho'].pop(str(produto_id), None)
        session.modified = True
    return redirect(url_for('carrinho'))

if __name__ == '__main__':
    app.run(debug=True)
