from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import urllib.parse

app = Flask(__name__)
app.secret_key = 'south_pole_ultimate_complete_secret_2026'

STORE_CONFIG = {
    "name": "South Pole Natural Kulfi",
    "tagline": "POS Counter & QR Menu with Photos",
    "logo": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150"
}

SOCIAL_LINKS = {
    "instagram": "https://instagram.com/southpolenaturalkulfi",
    "facebook": "https://facebook.com/southpolenaturalkulfi",
    "youtube": "https://youtube.com/@southpolenaturalkulfi",
    "whatsapp_channel": "https://whatsapp.com/channel/your-whatsapp-channel-link",
    "google_review": "https://g.page/r/your-google-review-link"
}

MENU_ITEMS = [
    {"id": 1, "name": "Jamun Kulfi", "price": 35, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150"},
    {"id": 2, "name": "Chocolate Kulfi", "price": 35, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=150"},
    {"id": 3, "name": "Paan Kulfi", "price": 30, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"},
    {"id": 4, "name": "Mango Kulfi", "price": 30, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?w=150"},
    {"id": 5, "name": "Sitafal Kulfi", "price": 30, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=150"},
    {"id": 6, "name": "Special Mawa Kulfi", "price": 45, "category": "Special", "image": "https://images.unsplash.com/photo-1587314168485-3236d6710814?w=150"},
    {"id": 7, "name": "Malai Kulfi", "price": 35, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=150"},
    {"id": 8, "name": "Kesar Pistachio Kulfi", "price": 40, "category": "Special", "image": "https://images.unsplash.com/photo-1560008511-11c63416e52d?w=150"},
    {"id": 9, "name": "Badam Pista Kulfi", "price": 40, "category": "Special", "image": "https://images.unsplash.com/photo-1576506295286-5cda18df43e7?w=150"},
    {"id": 10, "name": "Roasted Almond Kulfi", "price": 45, "category": "Special", "image": "https://images.unsplash.com/photo-1549395156-e0c1fe6fc7a5?w=150"},
    {"id": 11, "name": "Anjeer (Fig) Kulfi", "price": 45, "category": "Special", "image": "https://images.unsplash.com/photo-1505394033641-40c6ad1178d7?w=150"},
    {"id": 12, "name": "Black Currant Kulfi", "price": 40, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"},
    {"id": 13, "name": "Butterscotch Kulfi", "price": 40, "category": "Kulfi", "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=150"},
    {"id": 14, "name": "American Nuts Kulfi", "price": 45, "category": "Special", "image": "https://images.unsplash.com/photo-1582716401301-b2444cb73389?w=150"},
    {"id": 15, "name": "Rajbhog Kulfi", "price": 45, "category": "Special", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"},
    {"id": 16, "name": "Kulfi Falooda", "price": 60, "category": "Falooda", "image": "https://images.unsplash.com/photo-1553177598-f339f7271e98?w=150"},
    {"id": 17, "name": "Royal Kulfi Falooda", "price": 80, "category": "Falooda", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=150"},
    {"id": 18, "name": "Anjeer Ice Cream Scoop", "price": 85, "category": "Scoop", "image": "https://images.unsplash.com/photo-1497034825429-c343d7c6a68f?w=150"},
    {"id": 19, "name": "Mango Scoop", "price": 65, "category": "Scoop", "image": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=150"},
    {"id": 20, "name": "Sitafal Scoop", "price": 65, "category": "Scoop", "image": "https://images.unsplash.com/photo-1560008511-11c63416e52d?w=150"},
    {"id": 21, "name": "Vanilla Scoop", "price": 50, "category": "Scoop", "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=150"},
    {"id": 22, "name": "Chocolate Scoop", "price": 55, "category": "Scoop", "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=150"},
    {"id": 23, "name": "Strawberry Scoop", "price": 55, "category": "Scoop", "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=150"},
    {"id": 24, "name": "Butterscotch Scoop", "price": 60, "category": "Scoop", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"},
    {"id": 25, "name": "Dry Fruits Shake", "price": 125, "category": "Shake", "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=150"},
    {"id": 26, "name": "Anjeer Shake", "price": 105, "category": "Shake", "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=150"},
    {"id": 27, "name": "Mango Shake", "price": 95, "category": "Shake", "image": "https://images.unsplash.com/photo-1546173159-315724a31696?w=150"},
    {"id": 28, "name": "Chocolate Shake", "price": 90, "category": "Shake", "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=150"},
    {"id": 29, "name": "Cold Coffee with Ice Cream", "price": 110, "category": "Shake", "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=150"},
    {"id": 30, "name": "Sitafal Shake", "price": 105, "category": "Shake", "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=150"},
    {"id": 31, "name": "Kesar Milkshake", "price": 100, "category": "Shake", "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=150"},
    {"id": 32, "name": "Anjeer Mastani", "price": 145, "category": "Mastani", "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=150"},
    {"id": 33, "name": "Mango Mastani", "price": 135, "category": "Mastani", "image": "https://images.unsplash.com/photo-1553177598-f339f7271e98?w=150"},
    {"id": 34, "name": "Dry Fruit Mastani", "price": 160, "category": "Mastani", "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=150"},
    {"id": 35, "name": "Chocolate Blast Mastani", "price": 150, "category": "Mastani", "image": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=150"},
    {"id": 36, "name": "Special South Pole Sundae", "price": 180, "category": "Sundae", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=150"}
]

STAFF_LIST = [
    {"id": 1, "username": "staff1", "password": "123", "name": "रोहन (कौंटर)", "phone": "9876543210"}
]

ADMIN_PASSWORD = "admin123"
ORDERS = []
LOYALTY_DB = {}

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
🔄 *परत दिले:* ₹{return_change}

---
🌟 आमचे सोशल मीडिया आणि चॅनेल्स फॉलो करा:
📸 Instagram: {SOCIAL_LINKS['instagram']}
📘 Facebook: {SOCIAL_LINKS['facebook']}
▶️ YouTube: {SOCIAL_LINKS['youtube']}
📢 WhatsApp Channel: {SOCIAL_LINKS['whatsapp_channel']}
⭐ Google Review: {SOCIAL_LINKS['google_review']}

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
    total_orders = len(ORDERS)
    
    now = datetime.now()
    daily_sales = sum(o['total'] for o in ORDERS if datetime.strptime(o['date'], "%Y-%m-%d %H:%M").date() == now.date())
    weekly_sales = sum(o['total'] for o in ORDERS if datetime.strptime(o['date'], "%Y-%m-%d %H:%M") >= now - timedelta(days=7))
    monthly_sales = sum(o['total'] for o in ORDERS if datetime.strptime(o['date'], "%Y-%m-%d %H:%M").month == now.month)
    
    return render_template('admin_panel.html', 
                           orders=ORDERS, total_sales=total_sales, total_orders=total_orders,
                           daily_sales=daily_sales, weekly_sales=weekly_sales, monthly_sales=monthly_sales,
                           menu=MENU_ITEMS, staff_list=STAFF_LIST, config=STORE_CONFIG, 
                           social=SOCIAL_LINKS, loyalty_users=LOYALTY_DB)

@app.route('/admin/update_config', methods=['POST'])
def admin_update_config():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    STORE_CONFIG['name'] = request.form.get('store_name')
    STORE_CONFIG['tagline'] = request.form.get('tagline')
    STORE_CONFIG['logo'] = request.form.get('logo_url')
    
    SOCIAL_LINKS['instagram'] = request.form.get('instagram')
    SOCIAL_LINKS['facebook'] = request.form.get('facebook')
    SOCIAL_LINKS['youtube'] = request.form.get('youtube')
    SOCIAL_LINKS['whatsapp_channel'] = request.form.get('whatsapp_channel')
    SOCIAL_LINKS['google_review'] = request.form.get('google_review')
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_item', methods=['POST'])
def admin_add_item():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    new_id = max([i['id'] for i in MENU_ITEMS], default=0) + 1
    MENU_ITEMS.append({
        "id": new_id,
        "name": request.form.get('name'),
        "price": float(request.form.get('price', 0)),
        "category": request.form.get('category'),
        "image": request.form.get('image') or "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?w=150"
    })
    return redirect(url_for('admin_panel'))

@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
def admin_edit_item(item_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    item = next((i for i in MENU_ITEMS if i['id'] == item_id), None)
    if not item: return redirect(url_for('admin_panel'))
    
    if request.method == 'POST':
        item['name'] = request.form.get('name')
        item['price'] = float(request.form.get('price', 0))
        item['category'] = request.form.get('category')
        item['image'] = request.form.get('image') or item['image']
        return redirect(url_for('admin_panel'))
        
    return render_template('admin_edit_item.html', item=item, config=STORE_CONFIG, social=SOCIAL_LINKS)

@app.route('/admin/delete_item/<int:item_id>')
def admin_delete_item(item_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    global MENU_ITEMS
    MENU_ITEMS = [i for i in MENU_ITEMS if i['id'] != item_id]
    return redirect(url_for('admin_panel'))

@app.route('/admin/add_staff', methods=['POST'])
def admin_add_staff():
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    new_id = max([s['id'] for s in STAFF_LIST], default=0) + 1
    STAFF_LIST.append({
        "id": new_id,
        "username": request.form.get('username'),
        "password": request.form.get('password'),
        "name": request.form.get('name'),
        "phone": request.form.get('phone')
    })
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete_staff/<int:staff_id>')
def admin_delete_staff(staff_id):
    if not session.get('admin_logged'): return redirect(url_for('admin_login'))
    global STAFF_LIST
    STAFF_LIST = [s for s in STAFF_LIST if s['id'] != staff_id]
    return redirect(url_for('admin_panel'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

@app.route('/loyalty', methods=['GET', 'POST'])
def check_loyalty():
    user_data, message = None, None
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone in LOYALTY_DB: user_data = LOYALTY_DB[phone]
        else: message = "हा नंबर लॉयल्टी प्रोग्राममध्ये सापडला नाही."
    return render_template('check_loyalty.html', user_data=user_data, message=message, config=STORE_CONFIG, social=SOCIAL_LINKS)

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
