from flask import Flask, request, jsonify, render_template
import mysql.connector
import pandas as pd

app = Flask(__name__, template_folder='templates')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'debezium',
    'database': 'inventory'
}

@app.route('/send_data', methods=['POST'])
def send_data():
    data = request.get_json()

    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()

    insert_query = '''
    INSERT INTO customers (id, plate_number, car_make, car_year, owner_name, owner_address, owner_phone_number, subscription_status, subscription_start, subscription_end, balance, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    cursor.execute(insert_query, (
        data['id'],
        data['plate_number'],
        data['car_make'],
        data['car_year'],
        data['owner_name'],
        data['owner_address'],
        data['owner_phone_number'],
        data['subscription_status'],
        data['subscription_start'],
        data['subscription_end'],
        data['balance'],
        data['timestamp']
    ))

    conn.commit()

    cursor.close()

    conn.close()

    return jsonify({'message': 'Data received and stored successfully'}), 200

@app.route('/customers', methods=['GET'])
def customers():
    plate_number = request.args.get('plate_number', '')
    page = int(request.args.get('page', 1))
    items_per_page = 10

    conn = mysql.connector.connect(**db_config)

    