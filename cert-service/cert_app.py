from flask import Flask
from models.models import db
from certificate import cert_routes

app = Flask(__name__)
app.register_blueprint(cert_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:my-secret-pw@mysql:3306/mydatabase'


db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    #app.run(host='127.0.0.1', port=5001, debug=True)
#changed host to 0.0.0.0 from 127.0.0.1 change it later