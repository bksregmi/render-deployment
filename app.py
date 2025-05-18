from flask import Flask, render_template, redirect, url_for,jsonify,request
from pymongo import MongoClient
import mysql.connector

app=Flask(__name__)

client=MongoClient("mongodb+srv://workingyatri:QF0jmjKOfREtICoS@cluster1.fqv7v2j.mongodb.net/")
db=client['Status_Table']
collection=db['Status']
STATUS_DOC_ID = 1

def get_status():
    # Connect to the database
    doc=collection.find_one({"_id":STATUS_DOC_ID})
    if doc:
        return doc.get("status",0),doc.get("Emstat",0)
    else:
        return -1,-1

@app.route('/')
def index():
    status,emstat=get_status()
    return render_template('index.html', status=status, Emstat=emstat)


@app.route('/toggle')
def toggle():
    button_type = request.args.get('type')
    update_field=None
    
    if button_type == 'normal':
        update_field = 'status'
    elif button_type == 'emergency':
        update_field = 'Emstat'
    else:
        return redirect(url_for('index'))
    doc=collection.find_one({"_id":STATUS_DOC_ID})
    if not doc:
        doc={"_id":STATUS_DOC_ID,"status":-1,"Emstat":-1}
        collection.insert_one(doc)
        
    current_value=doc.get(update_field,0)
    new_value=0 if current_value==1 else 1
    collection.update_one(
        {"_id": STATUS_DOC_ID},
        {"$set": {update_field: new_value}}
    )    
    return redirect(url_for('index'))

@app.route("/status", methods=["GET"])
def get_status_endpoint():
    status,emstat=get_status()
    return jsonify({"status": status,"Emstat":emstat})  # Send it as a JSON response

            
if __name__ == '__main__':
    app.run()