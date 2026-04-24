from flask import Flask, render_template, request, redirect, session, flash
from db_config import conn, cursor

app = Flask(__name__)
app.secret_key = "secret123"


# 👑 ADMIN LOGIN
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s AND role='admin'",
            (user, pwd)
        )
        data = cursor.fetchone()

        if data:
            session['user'] = user
            session['role'] = 'admin'
            return redirect('/admin')
        else:
            return render_template('admin_login.html', error="Invalid Admin Login")

    return render_template('admin_login.html')


# 👤 USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s AND role='user'",
            (user, pwd)
        )
        data = cursor.fetchone()

        if data:
            session['user'] = user
            session['role'] = 'user'
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid User Login")

    return render_template('login.html')


# 📝 REGISTER (FIXED + FLASH MESSAGE)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s", (user,))
        if cursor.fetchone():
            return render_template('register.html', error="User already exists")

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,'user')",
            (user, pwd)
        )
        conn.commit()

        # ✅ SUCCESS MESSAGE FIX
        flash("Registration successful! Please login now")
        return redirect('/login')

    return render_template('register.html')


# 🚪 LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# 👤 USER DASHBOARD
@app.route('/')
def index():
    if session.get('role') != 'user':
        return redirect('/login')

    cursor.execute("SELECT * FROM donations")
    data = cursor.fetchall()

    total = len(data)
    available = sum(1 for row in data if row[5].strip() == 'Available')
    collected = sum(1 for row in data if row[5].strip() == 'Collected')

    return render_template('view_food.html',
                           data=data,
                           total=total,
                           available=available,
                           collected=collected)


# 👑 ADMIN DASHBOARD
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/admin_login')

    cursor.execute("SELECT * FROM donations")
    data = cursor.fetchall()

    total = len(data)
    available = sum(1 for row in data if row[5].strip() == 'Available')
    collected = sum(1 for row in data if row[5].strip() == 'Collected')

    return render_template('view_food.html',
                           data=data,
                           total=total,
                           available=available,
                           collected=collected)


# ➕ ADD FOOD
@app.route('/add', methods=['GET', 'POST'])
def add():
    if session.get('role') != 'admin':
        return "Access Denied"

    if request.method == 'POST':
        foods = request.form.getlist('food[]')
        qtys = request.form.getlist('qty[]')
        locs = request.form.getlist('loc[]')
        contacts = request.form.getlist('contact[]')
        expiries = request.form.getlist('expiry[]')

        for i in range(len(foods)):
            cursor.execute("""
                INSERT INTO donations 
                (food_name, quantity, location, contact, status, expiry_date)
                VALUES (%s,%s,%s,%s,'Available',%s)
            """, (foods[i], qtys[i], locs[i], contacts[i], expiries[i]))

        conn.commit()
        return redirect('/admin')

    return render_template('add_food.html')


# ✏️ UPDATE
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if session.get('role') != 'admin':
        return "Access Denied"

    if request.method == 'POST':
        qty = request.form['qty']
        status = request.form['status']

        cursor.execute(
            "UPDATE donations SET quantity=%s, status=%s WHERE id=%s",
            (qty, status, id)
        )
        conn.commit()
        return redirect('/admin')

    cursor.execute("SELECT * FROM donations WHERE id=%s", (id,))
    data = cursor.fetchone()
    return render_template('update_food.html', data=data)


# ❌ DELETE
@app.route('/delete/<int:id>')
def delete(id):
    if session.get('role') != 'admin':
        return "Access Denied"

    cursor.execute("DELETE FROM donations WHERE id=%s", (id,))
    conn.commit()
    return redirect('/admin')


# 🤝 REQUEST FOOD
@app.route('/request/<int:id>', methods=['GET', 'POST'])
def request_food(id):
    if session.get('role') != 'user':
        return "Only users allowed"

    if request.method == 'POST':
        name = session.get('user')

        cursor.execute("""
            INSERT INTO requests 
            (donation_id, requester_name, status, arrival_status)
            VALUES (%s,%s,'Pending','Not Coming')
        """, (id, name))

        conn.commit()
        return redirect('/view_requests')

    return render_template('request.html')


# ✅ APPROVE
@app.route('/approve/<int:id>')
def approve(id):
    if session.get('role') != 'admin':
        return "Access Denied"

    cursor.execute(
        "UPDATE requests SET status='Approved' WHERE id=%s",
        (id,)
    )
    conn.commit()

    return redirect('/view_requests')


# 🚗 I AM COMING
@app.route('/coming/<int:id>')
def coming(id):
    if session.get('role') != 'user':
        return "Only user allowed"

    cursor.execute(
        "UPDATE requests SET arrival_status='Coming' WHERE id=%s",
        (id,)
    )
    conn.commit()

    return redirect('/view_requests')


# 📦 COLLECTED
@app.route('/collect/<int:id>')
def collect_food(id):
    if session.get('role') != 'user':
        return "Only user allowed"

    cursor.execute(
        "UPDATE requests SET arrival_status='Collected' WHERE id=%s",
        (id,)
    )

    cursor.execute("SELECT donation_id FROM requests WHERE id=%s", (id,))
    donation = cursor.fetchone()

    if donation:
        cursor.execute(
            "UPDATE donations SET status='Collected' WHERE id=%s",
            (donation[0],)
        )

    conn.commit()
    return redirect('/view_requests')


# 📋 VIEW REQUESTS
@app.route('/view_requests')
def view_requests():

    if session.get('role') == 'admin':
        cursor.execute("SELECT * FROM requests")

    elif session.get('role') == 'user':
        cursor.execute(
            "SELECT * FROM requests WHERE requester_name=%s",
            (session.get('user'),)
        )
    else:
        return "Access Denied"

    data = cursor.fetchall()
    return render_template('view_requests.html', data=data)


# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)