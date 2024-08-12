from app import app, db, Produto

def inicializar_db():
    with app.app_context():
        db.create_all()

        # Adicionar produtos iniciais se a tabela estiver vazia
        if Produto.query.count() == 0:
            produtos = [
                Produto(nome='Camisa', preco=50.00, imagem='camisa.png'),
                Produto(nome='Calça', preco=100.00, imagem='calca.png'),
                Produto(nome='Tênis', preco=150.00, imagem='tenis.png')
            ]
            db.session.bulk_save_objects(produtos)
            db.session.commit()

if __name__ == '__main__':
    inicializar_db()
