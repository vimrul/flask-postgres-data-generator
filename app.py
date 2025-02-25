from flask import Flask, render_template, request, jsonify
import psycopg2
import threading
import time
from faker import Faker

app = Flask(__name__)
fake = Faker()

# Global variables for database configuration and data generation flag
db_config = {}
generating = False

def create_tables():
    """Creates necessary tables if they do not exist."""
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(id),
            amount DECIMAL(10, 2),
            transaction_date TIMESTAMP DEFAULT NOW()
        );
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_id INT REFERENCES customers(id),
            product_name VARCHAR(255),
            quantity INT,
            order_date TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def generate_data():
    """Generates fake customer, transaction, and order data at intervals."""
    global generating
    while generating:
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            
            # Insert a fake customer record
            cur.execute("INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s) RETURNING id;", 
                        (fake.name(), fake.email(), fake.phone_number()))
            customer_id = cur.fetchone()[0]

            # Insert a fake transaction linked to the customer
            cur.execute("INSERT INTO transactions (customer_id, amount) VALUES (%s, %s);", 
                        (customer_id, round(fake.random_number(digits=3), 2)))
            
            # Insert a fake order linked to the customer
            cur.execute("INSERT INTO orders (customer_id, product_name, quantity) VALUES (%s, %s, %s);", 
                        (customer_id, fake.word(), fake.random_int(min=1, max=10)))
            
            conn.commit()
            cur.close()
            conn.close()
            
            # Wait for 2 seconds before generating the next set of data
            time.sleep(2)
        except Exception as e:
            print("Error generating data:", e)

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/connect_db', methods=['POST'])
def connect_db():
    """Handle database connection setup from user input."""
    global db_config
    data = request.json
    db_config = {
        "host": data["host"],
        "port": data["port"],
        "dbname": data["dbname"],
        "user": data["user"],
        "password": data["password"]
    }
    try:
        conn = psycopg2.connect(**db_config)
        conn.close()
        create_tables()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/start_generation', methods=['POST'])
def start_generation():
    """Start data generation in a background thread."""
    global generating
    if not generating:
        generating = True
        threading.Thread(target=generate_data, daemon=True).start()
    return jsonify({"status": "started"})

@app.route('/stop_generation', methods=['POST'])
def stop_generation():
    """Stop the data generation process."""
    global generating
    generating = False
    return jsonify({"status": "stopped"})

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    """Fetch and return the latest data from all tables."""
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Retrieve the latest 10 customer records
        cur.execute("SELECT * FROM customers ORDER BY created_at DESC LIMIT 10;")
        customers = cur.fetchall()
        
        # Retrieve the latest 10 transaction records
        cur.execute("SELECT * FROM transactions ORDER BY transaction_date DESC LIMIT 10;")
        transactions = cur.fetchall()
        
        # Retrieve the latest 10 order records
        cur.execute("SELECT * FROM orders ORDER BY order_date DESC LIMIT 10;")
        orders = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({"customers": customers, "transactions": transactions, "orders": orders})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
