from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'south-pole-kulfi-super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kulfi_shop.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    loyalty_points = db.Column(db.Integer, default=0)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), default='default.jpg')

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    items_summary = db.Column(db.String(300), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Pending')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        admin_user = User(username='admin', password=hashed_pw, role='admin')
        db.session.add(admin_user)
        db.session.commit()
        
    # जर डेटाबेसमध्ये मेनू रिकामा असेल, तर आपोआप सॅम्पल कुलफी जोडल्या जातील
    if not MenuItem.query.first():
        sample_items = [
            MenuItem(name='Malai Kulfi', price=50),
            MenuItem(name='Pista Kulfi', price=60),
            MenuItem(name='Mango Kulfi', price=70)
        ]
        db.session.add_all(sample_items)
        db.session.commit()

@app.route('/')
def home():
    return redirect(url_for('customer_menu'))

@app.route('/order', methods=['GET', 'POST'])
def customer_menu():
    items = MenuItem.query.all()
    if request.method == 'POST':
        c_name = request.form.get('name')
        c_phone = request.form.get('phone')
        c_dob = request.form.get('dob')
        selected_item_id = request.form.get('item_id')
        
        # सुरक्षितपणे item_id तपासा जेणेकरून क्रश होणार नाही
        item = None
        if selected_item_id and selected_item_id.isdigit():
            item = MenuItem.query.get(int(selected_item_id))
            
        if item:
            customer = Customer.query.filter_by(phone=c_phone).first()
            if not customer:
                customer = Customer(name=c_name, phone=c_phone, dob=c_dob, loyalty_points=10)
                db.session.add(customer)
            else:
                customer.loyalty_points += 10
            
            new_bill = Bill(
                customer_name=c_name, 
                customer_phone=c_phone, 
                items_summary=item.name, 
                total_amount=item.price,
                status='Pending'
            )
            db.session.add(new_bill)
            db.session.commit()
            
            wa_message = f"New Kulfi Order! Customer: {c_name}, Phone: {c_phone}, Item: {item.name}, Amount: Rs.{item.price}"
            whatsapp_url = f"https://wa.me/91YOUR_NUMBER?text={urllib.parse.quote(wa_message)}"
            
            flash('तुमची ऑर्डर यशस्वीरित्या नोंदवली गेली आहे!')
            return render_template('bill_success.html', bill=new_bill, whatsapp_url=whatsapp_url)
        else:
            flash('कृपया मेनूमधून योग्य कुलफी निवडा!')

    return render_template('customer_menu.html', items=items)

@app.route('/check-loyalty', methods=['GET', 'POST'])
def check_loyalty():
    customer = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        customer = Customer.query.filter_by(phone=phone).first()
    return render_template('check_loyalty.html', customer=customer)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('चुकीचे युजरनेम किंवा पासवर्ड!')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    bills = Bill.query.all()
    menu_items = MenuItem.query.all()
    customers = Customer.query.all()
    return render_template('dashboard.html', bills=bills, menu_items=menu_items, customers=customers)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
