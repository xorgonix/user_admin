from flask import Flask, render_template, request
import stripe

app = Flask(__name__)

#set the template folder to the templates folder in the current directory

app.template_folder = './stripe/templates'

# Stripe API keys
stripe_keys = {
  'secret_key': 'sk_test_51Ni2C6AFil1bezBoN1khrPHM8AsoZwEGgelPtRCUC6wRf1mkEx7idQt7dPJC51UEZoRKOB29JNosoivzzUaBt4Vj004sRD7lJ0',
  'publishable_key': 'pk_test_51Ni2C6AFil1bezBoqXwLAd2UsrcFhZ3yqZY0ZKcxeZNGcOTLJrXxaoymJHf7ozTHldJemG8Gch6RPsDZRwuqa8jM00vWHXfD5L'
}

stripe.api_key = stripe_keys['secret_key']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    plan = request.form.get('plan')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': stripe_keys[plan],
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return jsonify({'session_id': session.id})

@app.route('/products')
def products():
    products = stripe.Product.list()
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
