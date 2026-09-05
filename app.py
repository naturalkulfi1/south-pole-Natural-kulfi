from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'south_pole_secret_key'

# कुल्फीचे आयटम्स
ITEMS = [
    {"id": 1, "name": "मलाई कुल्फी (Malai Kulfi)", "price": 50},
    {"id": 2, "name": "पिस्ता कुल्फी (Pista Kulfi)", "price": 60},
    {"id": 3, "name": "आंबा कुल्फी (Mango Kulfi)", "price": 70},
    {"id": 4, "name": "चॉकलेट कुल्फी (Chocolate Kulfi)", "price": 80}
]

# डमी डेटाबेस
orders_db = []
loyalty_db = {}

@app.route('/')
@app.route('/order', methods=['GET', 'POST'])
def customer_menu():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        item_id = int(request.form.get('item_id'))
        
        selected_item = next((item for item in ITEMS if item['id'] == item_id), None)
        
        if selected_item:
            # लॉयल्टी पॉईंट्स जोडणे (प्रत्येक ऑर्डरमागे 10 पॉईंट्स)
            current_points = loyalty_db.get(phone, 0) + 10
            loyalty_db[phone] = current_points
            
            order_details = {
                "name": name,
                "phone": phone,
                "item_name": selected_item['name'],
                "price": selected_item['price'],
                "points": current_points
            }
            orders_db.append(order_details)
            
            return render_template('bill_success.html', order=order_details)
            
    return render_template('customer_menu.html', items=ITEMS)

@app.route('/check-loyalty', methods=['GET', 'POST'])
def check_loyalty():
    points = None
    phone = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        points = loyalty_db.get(phone, 0)
    return render_template('check_loyalty.html', points=points, phone=phone)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['admin'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template('dashboard.html', orders=orders_db)

if __name__ == '__main__':
    app.run(debug=True)
