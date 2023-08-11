from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = '1234abcd'  

# Simulating user data storage (Replace with a proper database)
users = {
    'user1': {
        'password': hashlib.sha256('password123'.encode()).hexdigest()
    }
}

# Login route
@app.route('/http://127.0.0.1:5000\login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username in users and users[username]['password'] == hashed_password:
            session['username'] = username
            return redirect(url_for('dashboard'))

    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Welcome, {session["username"]}! This is your dashboard.'
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
