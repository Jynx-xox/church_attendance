from flask import Flask, render_template, request, redirect, url_for
from models import db, User
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

# 🔧 Optional: Only use this once if you didn't use setup_db.py
# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # 🔍 Check if this email is already signed up
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return f"That email is already signed up: {email}"

        # ✅ Save new user
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        # Send to Zapier
        zapier_webhook_url = "https://hooks.zapier.com/hooks/catch/22423332/20hrygz/"
        try:
            requests.post(zapier_webhook_url, json={
                "name": name,
                "email": email
            })
        except Exception as e:
            print("Error sending to Zapier:", e)

        return redirect(url_for('success', name=name))

    return render_template('signup.html')

@app.route('/delete_user/<email>')
def delete_user(email):
    user = User.query.filter_by(email=email).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"✅ Deleted user with email: {email}"
    else:
        return "❌ No user found with that email."


@app.route('/success')
def success():
    name = request.args.get('name')
    return f"Thanks for signing up, {name}! Check your email for your QR code soon."

if __name__ == '__main__':
    app.run(debug=True)
