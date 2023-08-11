from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = '1234abcd'

# Simulating user data storage (Replace with a proper database)
users = {
    'tatendakbeni@gmail.com': {
        'password': hashlib.sha256('password123'.encode()).hexdigest()
    }
}

# Login route
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if email in users and users[email]['password'] == hashed_password:
            session['email'] = email
            return redirect(url_for('dashboard'))

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        return f'Welcome, {session["email"]}! This is your dashboard.'
    return render_template('remittance_calculator.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
