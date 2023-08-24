from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer-portal', methods=['GET', 'POST'])
def customer_portal():
    if request.method == 'POST':
        # Handle the form submission for accessing the customer portal
        pass
    return render_template('customer_portal.html')

@app.route('/show-subscription-choices', methods=['GET', 'POST'])
def show_subscription_choices():
    if request.method == 'POST':
        # Handle the form submission for selecting a subscription plan
        pass
    return render_template('show_subscription_choices.html')

@app.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    if request.method == 'POST':
        # Handle the form submission for confirming the subscription
        pass
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
