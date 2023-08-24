from flask import Flask, render_template, request
import stripe

app = Flask(__name__)

# Stripe API keys
stripe_keys = {
  'secret_key': 'your_secret_key',
  'publishable_key': 'your_publishable_key'
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
