from flask import Flask, redirect, render_template, request,redirect
import mysql.connector

app = Flask(__name__)
import random
import os
from urllib.parse import urlparse
 
 
# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:ofUhcyFcnxgPCWRkXDYMXoyjcZgEcPoO@interchange.proxy.rlwy.net:29258/railway")
 
# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:ofUhcyFcnxgPCWRkXDYMXoyjcZgEcPoO@interchange.proxy.rlwy.net:29258/railway"
 
url = urlparse(db_url)
 
# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)
 
cursor = db.cursor()

cursor = db.cursor()

# Home Page
@app.route('/')
def index():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    print("DATA FROM DB:", data) 
    return render_template('index.html', customer=data)

# Insert Ride
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    cursor.execute("INSERT INTO customer(name,mobile,amount,location) VALUES(%s,%s,%s,%s)",
                   (name, mobile, amount, location))
    db.commit()
    return redirect('/')
# Delete Ride
@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    mobile = request.form['mobile']

    cursor.execute("""
        DELETE FROM customer 
        WHERE name=%s AND mobile=%s
    """, (name, mobile))

    db.commit()
    return redirect('/')
# Update Ride

@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    cursor.execute("""
        UPDATE customer 
        SET name=%s,amount=%s, location=%s
        WHERE  mobile=%s
    """, (name,amount, location, mobile))

    db.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)