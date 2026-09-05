from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# डमी मेनू डेटा
MENU_ITEMS = [
    {"id": "1", "name": "सीताफळ कुल्फी", "price": 40, "category": "Classic", "image": "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=100"},
    {"id": "2", "name": "मँगो कुल्फी", "price": 45, "category": "Seasonal", "image": "https://images.unsplash.com/photo-1553177598-fbb7a8b49704?w=100"}
]

ORDERS = []

@app.route('/')
def customer_portal():
    return render_template('customer_menu.html', items=MENU_ITEMS)

@app.route('/place_order', methods=['POST'])
def place_order():
    name = request.form.get('customer_name')
    phone = request.form.get('phone')
    dob = request.form.get('dob')
    cash_given = float(request.form.get('cash_given', 0) or 0)
    
    sitafal_qty = int(request.form.get('sitafal_qty', 0) or 0)
    mango_qty = int(request.form.get('mango_qty', 0) or 0)
    
    ordered_items = []
    total_amount = 0
    
    if sitafal_qty > 0:
        cost = sitafal_qty * 40
        ordered_items.append({"name": "सीताफळ कुल्फी", "qty": sitafal_qty, "total": cost})
        total_amount += cost
        
    if mango_qty > 0:
        cost = mango_qty * 45
        ordered_items.append({"name": "मँगो कुल्फी", "qty": mango_qty, "total": cost})
        total_amount += cost

    return_change = cash_given - total_amount if cash_given >= total_amount else 0

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
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "नवीन ऑर्डर"
    }
    ORDERS.append(order_data)
    
    return render_template('bill_success.html', order=order_data)

@app.route('/staff')
def staff_panel():
    return render_template('staff_panel.html', orders=ORDERS)

@app.route('/admin')
def admin_panel():
    # रिपोर्ट्स कॅल्क्युलेशन
    total_sales = sum(o['total'] for o in ORDERS)
    total_orders = len(ORDERS)
    return render_template('admin_panel.html', orders=ORDERS, total_sales=total_sales, total_orders=total_orders)

@app.route('/loyalty')
def check_loyalty():
    return render_template('check_loyalty.html')

if __name__ == '__main__':
    app.run(debug=True)
