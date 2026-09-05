from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'south_pole_master_kulfi_key_2026'

# १. डायनॅमिक मेनू (फोटो, किंमत आणि कॅटेगरीसह - 100% कस्टमाइझ्ड)
MENU_ITEMS = [
    {"id": 1, "name": "मलाई कुल्फी (Malai Kulfi)", "price": 50, "category": "Classic", "image": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?auto=format&fit=crop&w=500&q=60"},
    {"id": 2, "name": "पिस्ता कुल्फी (Pista Kulfi)", "price": 60, "category": "Classic", "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?auto=format&fit=crop&w=500&q=60"},
    {"id": 3, "name": "आंबा कुल्फी (Mango Kulfi)", "price": 70, "category": "Special", "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=500&q=60"},
    {"id": 4, "name": "चॉकलेट कुल्फी (Chocolate Kulfi)", "price": 80, "category": "Special", "image": "https://images.unsplash.com/photo-1579954115545-a95591f28bfc?auto=format&fit=crop&w=500&q=60"}
]

# डॅशबोर्ड व डेटाबेस
ORDERS_DB = []
LOYALTY_DB = {}
OFFERS_DB = [
    {"title": "सुपर वीकेंड ऑफर 🎉", "desc": "प्रत्येक रविवारी सर्व कुल्फीवर १०% सूट!", "type": "Weekly"}
]

# सोशल मीडिया व रिव्ह्यू लिंक्स (WhatsApp, Instagram, Google Review)
SOCIAL_LINKS = {
    "whatsapp_business": "https://wa.me/919876543210?text=Hello%20South%20Pole%20Kulfi,%20I%20want%20to%20order!",
    "instagram": "https://instagram.com/southpolekulfi",
    "facebook": "https://facebook.com/southpolekulfi",
    "youtube": "https://youtube.com/@southpolekulfi",
    "google_review": "https://g.page/r/sample-google-review-link"
}

@app.route('/')
@app.route('/order', methods=['GET', 'POST'])
def customer_portal():
    return render_template('customer_menu.html', items=MENU_ITEMS, offers=OFFERS_DB)

@app.route('/place-order', methods=['POST'])
def place_order():
    name = request.form.get('name')
    phone = request.form.get('phone')
    dob = request.form.get('dob')
    item_id = int(request.form.get('item_id'))
    
    selected_item = next((item for item in MENU_ITEMS if item['id'] == item_id), None)
    
    if selected_item:
        current_points = LOYALTY_DB.get(phone, 0) + 10
        LOYALTY_DB[phone] = current_points
        
        order_id = len(ORDERS_DB) + 1
        order_details = {
            "id": order_id,
            "name": name,
            "phone": phone,
            "dob": dob,
            "item_name": selected_item['name'],
            "price": selected_item['price'],
            "points": current_points,
            "status": "Kitchen Preparing (तयार होत आहे)"
        }
        ORDERS_DB.append(order_details)
        
        return render_template('bill_success.html', order=order_details, social=SOCIAL_LINKS)
        
    return redirect(url_for('customer_portal'))

@app.route('/staff-panel')
def staff_panel():
    # पेटपूजा स्टाईल किचन डिस्प्ले (Staff Panel)
    return render_template('staff_panel.html', orders=ORDERS_DB)

@app.route('/update-order-status/<int:order_id>/<status>')
def update_order_status(order_id, status):
    for order in ORDERS_DB:
        if order['id'] == order_id:
            order['status'] = status
    return redirect(url_for('staff_panel'))

@app.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel():
    # पूर्ण कस्टमाइझ्ड ॲडमिन पॅनल (नवीन कुल्फी किंवा ऑफर जोडण्यासाठी)
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add_item':
            new_item = {
                "id": len(MENU_ITEMS) + 1,
                "name": request.form.get('name'),
                "price": float(request.form.get('price')),
                "category": request.form.get('category'),
                "image": request.form.get('image')
            }
            MENU_ITEMS.append(new_item)
        elif action == 'add_offer':
            new_offer = {
                "title": request.form.get('title'),
                "desc": request.form.get('desc'),
                "type": request.form.get('type')
            }
            OFFERS_DB.append(new_offer)
        return redirect(url_for('admin_panel'))
        
    return render_template('admin_panel.html', items=MENU_ITEMS, orders=ORDERS_DB, offers=OFFERS_DB)

@app.route('/check-loyalty', methods=['GET', 'POST'])
def check_loyalty():
    points = None
    phone = None
    if request.method == 'POST':
        phone = request.form.get('phone')
        points = LOYALTY_DB.get(phone, 0)
    return render_template('check_loyalty.html', points=points, phone=phone)

if __name__ == '__main__':
    app.run(debug=True)
