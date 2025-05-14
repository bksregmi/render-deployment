from flask import Flask, render_template, redirect, url_for,jsonify
import mysql.connector

app=Flask(__name__)

db_config = {'host':'sql12.freesqldatabase.com','user':'sql12777796','password':'SktVxwR9Hp','database':'sql12777796'}

def get_status():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname='status'")
    status = cursor.fetchone()[0]  # Fetch the result
    conn.close()
    return status

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname='status'")
    status = cursor.fetchone()[0]
    conn.close()
    return render_template('index.html', status=status)


@app.route('/toggle')
def toggle():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname='status'")
    current_status = cursor.fetchone()[0]
    new_status = 0 if current_status == 1 else 1
    cursor.execute("UPDATE Status SET Value=%s WHERE Varname='status'", (new_status,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/status", methods=["GET"])
def get_status_endpoint():
    status = get_status()  # Fetch the current status from DB
    return jsonify({"status": status})  # Send it as a JSON response

            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)