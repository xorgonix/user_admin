from flask import Flask, render_template, request, jsonify, redirect, url_for
import stripe
import json

app = Flask(__name__)

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = 'sk_test_51Ni2C6AFil1bezBoN1khrPHM8AsoZwEGgelPtRCUC6wRf1mkEx7idQt7dPJC51UEZoRKOB29JNosoivzzUaBt4Vj004sRD7lJ0'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    # The price ID passed from the front end.
    price_id = request.form.get('priceId')

    session = stripe.checkout.Session.create(
        success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://example.com/canceled.html',
        mode='subscription',
        line_items=[{
            'price': price_id,
            # For metered billing, do not pass quantity
            'quantity': 1
        }],
    )

    # Redirect to the URL returned on the session
    return redirect(session.url, code=303)

@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = 'STRIPE_WEBHOOK_SECRET'
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
    # Payment is successful and the subscription is created.
    # You should provision the subscription and save the customer ID to your database.
      print(data)
    elif event_type == 'invoice.paid':
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
      print(data)
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
      print(data)
    else:
      print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})

@app.route('/customer-portal', methods=['POST'])
def customer_portal():
    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = 'DOMAIN_URL'
    return_url = url_for('index', _external=True)   
    customer_id = 'CUSTOMER_ID'

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url=return_url,
    )

    # redirect to the URL for the session
    return redirect(session.url, code=303)

if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
    @app.route('/plans', methods=['GET'])
def display_plans():
    # Fetch the plans from Stripe
    plans = stripe.Plan.list()
    # Render the plans in a template (you need to create this template)
    return render_template('plans.html', plans=plans)

@app.route('/select-plan', methods=['POST'])
def select_plan():
    # Get the selected plan ID from the frontend
    plan_id = request.form.get('planId')
    # Create a checkout session with the selected plan
    session = stripe.checkout.Session.create(
        success_url='https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://example.com/canceled.html',
        mode='subscription',
        line_items=[{
            'price': plan_id,
            'quantity': 1
        }],
    )
    # Redirect to the checkout page
    return redirect(session.url, code=303)
