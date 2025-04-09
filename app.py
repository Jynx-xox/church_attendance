from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # We'll handle saving, QR generation, and email later
        print(f"Received signup: {name}, {email}")
        return redirect(url_for('success', name=name))
    return render_template('signup.html')

@app.route('/success')
def success():
    name = request.args.get('name')
    return f"Thanks for signing up, {name}! Check your email for your QR code soon."
