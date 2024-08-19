from hello import db,app,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin



class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False) 
    token = db.Column(db.String(1024), nullable=True)
    @staticmethod
    def generate_reset_token(user_id, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'user_id': user_id}).decode('utf-8')
    

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
            print(f"User Id: {user_id}")  # Debugging statement
        except:
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.id}','{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))