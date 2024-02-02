from flask import Flask
from models.models import db
from customer import internal_routes

app = Flask(__name__)
app.register_blueprint(internal_routes)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:my-secret-pw@mysql:3306/mydatabase'



db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    