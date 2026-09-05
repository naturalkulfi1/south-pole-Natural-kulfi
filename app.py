from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'south_pole_secret_key'  # सेशन मॅनेजमेंटसाठी आवश्यक

# डायनॅमिक मेनू डेटा
MENU_ITEMS = [
    {"id": 1, "name": "सीताफळ कुल्फी", "price": 40, "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=100"},
    {"id": 2, "name": "मँगो कुल्फी", "price": 45, "image": "https://images.unsplash.com/photo-1553177598-fbb7a8b49704?w=100"}
]

# स्टाफ डेटाबेस (युजरनेम आणि पासवर्डसह)
STAFF_LIST = [
    {"id": 1, "username": "staff1", "password": "123", "name": "रोहन (कौंटर)", "phone": "9876543210"}
]

# ॲडमिन पासवर्ड
ADMIN_PASSWORD = "admin123"

ORDERS = []
LOYALTY_DB = {}  # 1 Visit = 1 Point

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
    dob = request.form.get('dob')
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
            LOYALTY_DB[phone] = {
                "name": name, 
                "phone": phone, 
                "dob": dob if dob else "उपलब्ध नाही", 
                "points": 1 
            }

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

# --- स्टाफ लॉगिन आणि पॅनल ---
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

# --- ॲडमिन लॉगिन आणि पॅनल ---
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

# ॲडमिन: मेनू ॲड/डिलिट
@app.route('/admin/add_menu', methods=['POST'])
def add_menu():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    name = request.form.get('name')
    price = float(request.form.get('price', 0))
    image = request.form.get('image')
    new_id = len(MENU_ITEMS) + 1
    MENU_ITEMS.append({"id": new_id, "name": name, "price": price, "image": image})
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_menu/<int:item_id>')
def delete_menu(item_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    global MENU_ITEMS
    MENU_ITEMS = [item for item in MENU_ITEMS if item['id'] != item_id]
    return redirect(url_for('admin_panel'))

# ॲडमिन: स्टाफ ॲड/डिलिट
@app.route('/admin/add_staff', methods=['POST'])
def add_staff():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    name = request.form.get('staff_name')
    username = request.form.get('staff_username')
    password = request.form.get('staff_password')
    phone = request.form.get('staff_phone')
    new_id = len(STAFF_LIST) + 1
    STAFF_LIST.append({"id": new_id, "username": username, "password": password, "name": name, "phone": phone})
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_staff/<int:staff_id>')
def delete_staff(staff_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    global STAFF_LIST
    STAFF_LIST = [s for s in STAFF_LIST if s['id'] != staff_id]
    return redirect(url_for('admin_panel'))

@app.route('/loyalty', methods=['GET', 'POST'])
def check_loyalty():
    user_data = None
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        phone = request.form.get('phone')
        if action == 'check':
            if phone in LOYALTY_DB:
                user_data = LOYALTY_DB[phone]
            else:
                message = "हा नंबर लॉयल्टी प्रोग्राममध्ये सापडला नाही."
    return render_template('check_loyalty.html', user_data=user_data, message=message)

if __name__ == '__main__':
    app.run(debug=True)
