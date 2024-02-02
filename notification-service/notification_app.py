from flask import Flask
from models.models import db
from notification import noti_routes

app = Flask(__name__)
app.register_blueprint(noti_routes)

#change dev-mysql ti localhost for local use
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:my-secret-pw@dev-mysql:3306/mydatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:my-secret-pw@mysql:3306/mydatabase'


db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
    #app.run(host='127.0.0.1', port=8001, debug=True)
    #change 0.0.0.0 to 127.0.0.1 for local use

