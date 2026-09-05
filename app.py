from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import urllib.parse

app = Flask(__name__)
app.secret_key = 'south_pole_fully_customizable_secret'

# ब्रँड आणि लोगो सेटिंग (ॲडमिनवरून बदलता येईल)
STORE_CONFIG = {
    "name": "South Pole Natural Kulfi",
    "tagline": "POS Counter & QR Menu with Photos",
    "logo": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150" # इथे तुमचा लोगो टाका
}

MENU_ITEMS = [
    {"id": 1, "name": "Jamun Kulfi", "price": 35, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150"},
    {"id": 2, "name": "Chocolate Kulfi", "price": 35, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=150"},
    {"id": 3, "name": "Paan Kulfi", "price": 30, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"},
    {"id": 4, "name": "Mango Kulfi", "price": 30, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=150"}
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
    return render_template('customer_menu.html', items=MENU_ITEMS, config=STORE_CONFIG, social=SOCIAL_LINKS)

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
            LOYALTY_DB[phone] = {"name": name, "phone": phone, "dob": dob if dob else "N/A", "points": 1}

    order_id = len(ORDERS) + 1
    items_text = "\n".join([f"- {i['name']} x {i['qty']} = ₹{i['total']}" for i in ordered_items])
    
    whatsapp_msg = f"""🍦 *{STORE_CONFIG['name']}* 🍦
नमस्ते *{name}*, आपली ऑर्डर कन्फर्म झाली आहे! 🙏

🧾 *ऑर्डर बिल (Order ID: #{order_id})*
{items_text}

💰 *एकूण रक्कम:* ₹{total_amount}
💵 *दिलेले पैसे:* ₹{cash_given}
🔄 *परत दिलेले पैसे:* ₹{return_change}

पुन्हा भेट दिल्याबद्दल धन्यवाद! 🙏"""

    encoded_msg = urllib.parse.quote(whatsapp_msg)
    whatsapp_link = f"https://wa.me/91{phone}?text={encoded_msg}"

    order_data = {
        "id": order_id, "name": name, "phone": phone, "dob": dob,
        "items": ordered_items, "total": total_amount, "cash_given": cash_given,
        "return_change": return_change, "status": "Pending",
        "whatsapp_link": whatsapp_link, "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ORDERS.append(order_data)
    return render_template('bill_success.html', order=order_data, config=STORE_CONFIG, social=SOCIAL_LINKS)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == ADMIN_PASSWORD:
            session['admin_logged'] = True
            return redirect(url_for('admin_panel'))
        error = "चुकीचा ॲडमिन पासवर्ड!"
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    
    total_sales = sum(o['total'] for o in ORDERS)
    return render_template('admin_panel.html', 
                           orders=ORDERS, total_sales=total_sales, 
                           menu=MENU_ITEMS, config=STORE_CONFIG, 
                           loyalty_users=LOYALTY_DB)

@app.route('/admin/add_item', methods=['POST'])
def admin_add_item():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    new_id = max([i['id'] for i in MENU_ITEMS], default=0) + 1
    name = request.form.get('name')
    price = float(request.form.get('price', 0))
    category = request.form.get('category')
    image = request.form.get('image') or "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150"
    
    MENU_ITEMS.append({"id": new_id, "name": name, "price": price, "category": category, "image": image})
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_item/<int:item_id>')
def admin_delete_item(item_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    global MENU_ITEMS
    MENU_ITEMS = [i for i in MENU_ITEMS if i['id'] != item_id]
    return redirect(url_for('admin_panel'))

@app.route('/admin/update_config', methods=['POST'])
def admin_update_config():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    STORE_CONFIG['name'] = request.form.get('store_name')
    STORE_CONFIG['tagline'] = request.form.get('tagline')
    STORE_CONFIG['logo'] = request.form.get('logo_url')
    return redirect(url_for('admin_panel'))

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
        if phone in LOYALTY_DB: user_data = LOYALTY_DB[phone]
        else: message = "हा नंबर लॉयल्टी प्रोग्राममध्ये सापडला नाही."
    return render_template('check_loyalty.html', user_data=user_data, message=message, config=STORE_CONFIG)

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    error = None
    if request.method == 'POST':
        for s in STAFF_LIST:
            if s['username'] == request.form.get('username') and s['password'] == request.form.get('password'):
                session['staff_logged'] = True
                return redirect(url_for('staff_panel'))
        error = "चुकीचा युजरनेम किंवा पासवर्ड!"
    return render_template('staff_login.html', error=error)

@app.route('/staff')
def staff_panel():
    if not session.get('staff_logged') and not session.get('admin_logged'): return redirect(url_for('staff_login'))
    return render_template('staff_panel.html', orders=ORDERS, config=STORE_CONFIG)

@app.route('/staff/confirm/<int:order_id>')
def staff_confirm_order(order_id):
    for o in ORDERS:
        if o['id'] == order_id: o['status'] = 'Confirmed'
    return redirect(url_for('staff_panel'))

@app.route('/staff/logout')
def staff_logout():
    session.pop('staff_logged', None)
    return redirect(url_for('staff_login'))

if __name__ == '__main__':
    app.run(debug=True)
