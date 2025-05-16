from flask import Flask, render_template, redirect, url_for,jsonify,request
import mysql.connector

app=Flask(__name__)

db_config = {'host':'sql12.freesqldatabase.com','user':'sql12779194','password':'Q2z6DmdZZD','database':'sql12779194'}

def get_status(varname):
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname=%s",(varname,))
    status = cursor.fetchone()[0]  # Fetch the result
    conn.close()
    return status

@app.route('/')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname='status'")
    status = cursor.fetchone()[0]
    
    cursor.execute("SELECT Value FROM Status WHERE Varname='Emstat'")
    emergency_status = cursor.fetchone()[0]
    conn.close()
    return render_template('index.html', status=status, Emstat=emergency_status)


@app.route('/toggle')
def toggle():
    button_type = request.args.get('type')
    
    
    if button_type == 'normal':
        varname = 'status'
    elif button_type == 'emergency':
        varname = 'Emstat'
    else:
        return redirect(url_for('index'))
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Status WHERE Varname=%s",(varname,))
    current_status = cursor.fetchone()[0]
    new_status = 0 if current_status == 1 else 1
    cursor.execute("UPDATE Status SET Value=%s WHERE Varname=%s", (new_status,varname))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/status", methods=["GET"])
def get_status_endpoint():
    status = get_status('status')  # Fetch the current status from DB
    emstat = get_status('Emstat')
    return jsonify({"status": status,"Emstat":emstat})  # Send it as a JSON response

            
if __name__ == '__main__':
    app.run()