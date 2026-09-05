from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# तुमच्या कुल्फीच्या वस्तू (डेटाबेस किंवा लिस्ट)
ITEMS = [
    {"id": 1, "name": "मलाई कुल्फी (Malai Kulfi)", "price": 50},
    {"id": 2, "name": "पिस्ता कुल्फी (Pista Kulfi)", "price": 60},
    {"id": 3, "name": "आंबा कुल्फी (Mango Kulfi)", "price": 70},
    {"id": 4, "name": "चॉकलेट कुल्फी (Chocolate Kulfi)", "price": 80}
]

@app.route('/order', methods=['GET', 'POST'])
def customer_menu():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        item_id = request.form.get('item_id')
        # पुढे ऑर्डर प्रोसेस करण्याची लॉजिक इथे येईल
        return redirect(url_for('customer_menu'))
    
    return render_template('customer_menu.html', items=ITEMS)

@app.route('/check-loyalty')
def check_loyalty():
    return "लोयल्टी पॉईंट्स पेज लवकच येत आहे!"

if __name__ == '__main__':
    app.run(debug=True)
