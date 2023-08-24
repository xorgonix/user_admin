from flask import Flask, render_template, request, redirect, url_for, session
import stripe

stripe.api_key = 'your-stripe-secret-key'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer-portal', methods=['GET', 'POST'])
def customer_portal():
    if 'customer_id' not in session:
        return redirect(url_for('home'))

    session = stripe.billing_portal.Session.create(
        customer=session['customer_id'],
        return_url=url_for('home', _external=True)
    )
    return redirect(session.url)

@app.route('/show-subscription-choices', methods=['GET', 'POST'])
def show_subscription_choices():
    plans = stripe.Plan.list()
    return render_template('show_subscription_choices.html', plans=plans)

@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if 'plan_id' not in session:
        return redirect(url_for('show_subscription_choices'))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': session['plan_id'],
            'quantity': 1,
        }],
        mode='subscription',
        success_url=url_for('home', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('show_subscription_choices', _external=True),
    )
    return redirect(checkout_session.url)

if __name__ == '__main__':
    app.run(debug=True)
