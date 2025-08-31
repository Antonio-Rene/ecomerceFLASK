from app import db, Usuario, app

with app.app_context():
    db.create_all()
    if not Usuario.query.filter_by(email='admin@example.com').first():
        u = Usuario(nome='Admin', email='admin@example.com')
        u.set_senha('senha123')
        db.session.add(u)
        db.session.commit()
        print('admin criado')
