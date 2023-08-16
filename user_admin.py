from flask import Flask, request, render_template_string, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Set up Flask app and database
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sophtbot.db'
db = SQLAlchemy(app)

# Define User model
from datetime import datetime

from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=True, default=False)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Route to initialize the database and create tables
@app.route('/init_db')
def init_db():
    db.create_all()
    return '<h1>Database initialized and tables created!</h1>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes and logic
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(user_name=request.form['username'], 
                        first_name=request.form['first_name'], 
                        last_name=request.form['last_name'], 
                        phone=request.form['phone'], 
                        email=request.form['email'], 
                        password=hashed_password,
                        admin=False,
                        registered_on=datetime.utcnow(),
                        last_login=datetime.utcnow()
                        )
        db.session.add(new_user)
        db.session.commit()
        return render_template('registration_ok.html')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(user_name=request.form['username']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user, remember=request.form.get('remember'))
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'POST':
        current_user.user_name = request.form['username']
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.phone = request.form['phone']
        current_user.email = request.form['email']
        db.session.commit()
        return '<h1>Your profile has been updated!</h1>'
    return render_template('update.html')

@app.route('/list_users')
@login_required
def list_users():
    users = User.query.all()
    print(users)  # Add this print statement
    return render_template('list_users.html', users=users)



if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
