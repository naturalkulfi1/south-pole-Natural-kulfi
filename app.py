from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'south_pole_secret_key'

# दक्षिण पोल नॅचरल कुल्फीचे सर्व ३६ आयटम्स
MENU_ITEMS = [
    {"id": 1, "name": "Jamun Kulfi", "price": 35, "category": "Kulfi"},
    {"id": 2, "name": "Chocolate Kulfi", "price": 35, "category": "Kulfi"},
    {"id": 3, "name": "Paan Kulfi", "price": 30, "category": "Kulfi"},
    {"id": 4, "name": "Mango Kulfi", "price": 30, "category": "Kulfi"},
    {"id": 5, "name": "Sitafal Kulfi", "price": 30, "category": "Kulfi"},
    {"id": 6, "name": "Special Mawa Kulfi", "price": 45, "category": "Special"},
    {"id": 7, "name": "Malai Kulfi", "price": 35, "category": "Kulfi"},
    {"id": 8, "name": "Kesar Pistachio Kulfi", "price": 40, "category": "Special"},
    {"id": 9, "name": "Badam Pista Kulfi", "price": 40, "category": "Special"},
    {"id": 10, "name": "Roasted Almond Kulfi", "price": 45, "category": "Special"},
    {"id": 11, "name": "Anjeer (Fig) Kulfi", "price": 45, "category": "Special"},
    {"id": 12, "name": "Black Currant Kulfi", "price": 40, "category": "Kulfi"},
    {"id": 13, "name": "Butterscotch Kulfi", "price": 40, "category": "Kulfi"},
    {"id": 14, "name": "American Nuts Kulfi", "price": 45, "category": "Special"},
    {"id": 15, "name": "Rajbhog Kulfi", "price": 45, "category": "Special"},
    {"id": 16, "name": "Kulfi Falooda", "price": 60, "category": "Falooda"},
    {"id": 17, "name": "Royal Kulfi Falooda", "price": 80, "category": "Falooda"},
    {"id": 18, "name": "Anjeer Ice Cream Scoop", "price": 85, "category": "Scoop"},
    {"id": 19, "name": "Mango Scoop", "price": 65, "category": "Scoop"},
    {"id": 20, "name": "Sitafal Scoop", "price": 65, "category": "Scoop"},
    {"id": 21, "name": "Vanilla Scoop", "price": 50, "category": "Scoop"},
    {"id": 22, "name": "Chocolate Scoop", "price": 55, "category": "Scoop"},
    {"id": 23, "name": "Strawberry Scoop", "price": 55, "category": "Scoop"},
    {"id": 24, "name": "Butterscotch Scoop", "price": 60, "category": "Scoop"},
    {"id": 25, "name": "Dry Fruits Shake", "price": 125, "category": "Shake"},
    {"id": 26, "name": "Anjeer Shake", "price": 105, "category": "Shake"},
    {"id": 27, "name": "Mango Shake", "price": 95, "category": "Shake"},
    {"id": 28, "name": "Chocolate Shake", "price": 90, "category": "Shake"},
    {"id": 29, "name": "Cold Coffee with Ice Cream", "price": 110, "category": "Shake"},
    {"id": 30, "name": "Sitafal Shake", "price": 105, "category": "Shake"},
    {"id": 31, "name": "Kesar Milkshake", "price": 100, "category": "Shake"},
    {"id": 32, "name": "Anjeer Mastani", "price": 145, "category": "Mastani"},
    {"id": 33, "name": "Mango Mastani", "price": 135, "category": "Mastani"},
    {"id": 34, "name": "Dry Fruit Mastani", "price": 160, "category": "Mastani"},
    {"id": 35, "name": "Chocolate Blast Mastani", "price": 150, "category": "Mastani"},
    {"id": 36, "name": "Special South Pole Sundae", "price": 180, "category": "Sundae"}
]

STAFF_LIST = [
    {"id": 1, "username": "staff1", "password": "123", "name": "रोहन (कौंटर)", "phone": "9876543210"}
]

ADMIN_PASSWORD = "admin123"
ORDERS = []
LOYALTY_DB = {}

SOCIAL_LINKS = {
    "instagram": "https://instagram.com/southpolenaturalkulfi",
    "facebook": "https://facebook.com/southpolenaturalkulfi",
    "youtube": "https://youtube.com/@southpolenaturalkulfi",
    "google_review": "https://g.page/r/your-google-review-link"
}

@app.route('/')
def customer_portal():
    return render_template('customer_menu.html', items=MENU_ITEMS, social=SOCIAL_LINKS)

@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form.get('customer_name')
    phone = request.form.get('phone')
    dob = request.form.get('dob') # जन्म तारीख
    cash_given = float(request.form.get('cash_given', 0) or 0)
    
    ordered_items = []
    total_amount = 0
    
    for item in MENU_ITEMS:
        qty = int(request.form.get(f'item_{item["id"]}', 0) or 0)
        if qty > 0:
            cost = qty * item['price']
            ordered_items.append({"name": item['name'], "qty": qty, "total": cost})
            total_amount += cost

    return_change = cash_given - total_amount if cash_given >= total_amount else 0

    if phone and total_amount > 0:
        if phone in LOYALTY_DB:
            LOYALTY_DB[phone]['points'] += 1
            if name: LOYALTY_DB[phone]['name'] = name
            if dob: LOYALTY_DB[phone]['dob'] = dob
        else:
            LOYALTY_DB[phone] = {"name": name, "phone": phone, "dob": dob if dob else "N/A", "points": 1}

    order_id = len(ORDERS) + 1
    order_data = {
        "id": order_id,
        "name": name,
        "phone": phone,
        "dob": dob,
        "items": ordered_items,
        "total": total_amount,
        "cash_given": cash_given,
        "return_change": return_change,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ORDERS.append(order_data)
    
    return render_template('bill_success.html', order=order_data, social=SOCIAL_LINKS)

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        for s in STAFF_LIST:
            if s['username'] == username and s['password'] == password:
                session['staff_logged'] = True
                return redirect(url_for('staff_panel'))
        error = "चुकीचा युजरनेम किंवा पासवर्ड!"
    return render_template('staff_login.html', error=error)

@app.route('/staff')
def staff_panel():
    if not session.get('staff_logged'):
        return redirect(url_for('staff_login'))
    return render_template('staff_panel.html', orders=ORDERS, staff=STAFF_LIST)

@app.route('/staff/logout')
def staff_logout():
    session.pop('staff_logged', None)
    return redirect(url_for('staff_login'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged'] = True
            return redirect(url_for('admin_panel'))
        error = "चुकीचा ॲडमिन पासवर्ड!"
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    total_sales = sum(o['total'] for o in ORDERS)
    total_orders = len(ORDERS)
    return render_template('admin_panel.html', orders=ORDERS, total_sales=total_sales, total_orders=total_orders, menu=MENU_ITEMS, staff=STAFF_LIST, loyalty_users=LOYALTY_DB, social=SOCIAL_LINKS)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

@app.route('/loyalty', methods=['GET', 'POST'])
def check_loyalty():
    user_data = None
    message = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone in LOYALTY_DB:
            user_data = LOYALTY_DB[phone]
        else:
            message = "हा नंबर लॉयल्टी प्रोग्राममध्ये सापडला नाही."
    return render_template('check_loyalty.html', user_data=user_data, message=message)

if __name__ == '__main__':
    app.run(debug=True)
