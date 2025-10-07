from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response
import jwt
from datetime import datetime, timedelta
import uuid
import hashlib

app = Flask(__name__)

JWT_SECRET = "admin123"
JWT_ALGORITHM = "HS256"

users = {
    "manager": {"password": "supply2024", "role": "manager", "full_name": "John Mitchell", "department": "Supply Chain", "email": "j.mitchell@inventorypro.com"},
    "supervisor": {"password": "inventory!", "role": "supervisor", "full_name": "Sarah Connor", "department": "Warehouse Operations", "email": "s.connor@inventorypro.com"},
    "analyst": {"password": "data2024", "role": "analyst", "full_name": "Mike Rodriguez", "department": "Data Analysis", "email": "m.rodriguez@inventorypro.com"},
    "coordinator": {"password": "coord123", "role": "coordinator", "full_name": "Emma Wilson", "department": "Logistics", "email": "e.wilson@inventorypro.com"},
    "admin": {"password": "warehouse_secure", "role": "admin", "full_name": "Robert Admin", "department": "IT Administration", "email": "admin@inventorypro.com"}
}

inventory_items = [
    {"id": 1, "name": "Dell Laptop XPS 13", "category": "Electronics", "quantity": 25, "location": "Warehouse A", "status": "available"},
    {"id": 2, "name": "Office Chair Pro", "category": "Furniture", "quantity": 12, "location": "Warehouse B", "status": "available"},
    {"id": 3, "name": "Network Switch 24-Port", "category": "Networking", "quantity": 8, "location": "IT Storage", "status": "reserved"},
    {"id": 4, "name": "Wireless Mouse", "category": "Accessories", "quantity": 45, "location": "Warehouse A", "status": "available"},
    {"id": 5, "name": "Monitor 27inch 4K", "category": "Electronics", "quantity": 15, "location": "Warehouse C", "status": "available"}
]

critical_assets = [
    {"id": 101, "name": "Server Rack Enterprise", "value": "$25,000", "location": "Secure Data Center", "classification": "Critical Infrastructure"},
    {"id": 102, "name": "Backup Storage Array", "value": "$18,500", "location": "Secure Data Center", "classification": "Critical Infrastructure"},
    {"id": 103, "name": "Network Core Switch", "value": "$12,000", "location": "Network Operations Center", "classification": "Essential Systems"},
    {"id": 104, "name": "Security Camera System", "value": "$8,500", "location": "Multiple Locations", "classification": "Security Equipment"}
]

def create_jwt_token(username, role):
    payload = {
        "iss": "inventorymanager",
        "exp": datetime.utcnow() + timedelta(hours=24),
        "sub": username,
        "role": role,
        "kid": str(uuid.uuid4())
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            token = create_jwt_token(username, users[username]['role'])
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('session', token, httponly=True)
            return response
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('session')
    if not token:
        return redirect(url_for('login'))
    
    payload = verify_jwt_token(token)
    if not payload:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', 
                         username=payload['sub'], 
                         role=payload['role'], 
                         items=inventory_items)

@app.route('/my-account')
def my_account():
    token = request.cookies.get('session')
    if not token:
        return redirect(url_for('login'))
    
    payload = verify_jwt_token(token)
    if not payload:
        return redirect(url_for('login'))
    
    user_info = {
        "username": payload['sub'],
        "role": payload['role'],
        "exp": payload['exp']
    }
    
    return render_template('account.html', user=user_info)

@app.route('/admin')
def admin_panel():
    token = request.cookies.get('session')
    if not token:
        return jsonify({"error": "Authentication required"}), 401
    
    payload = verify_jwt_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    
    if payload['sub'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    # Get list of users (excluding admin)
    user_list = []
    for username, user_data in users.items():
        if username != 'admin':  # Don't show admin in deletable users
            user_list.append({
                "username": username,
                "full_name": user_data["full_name"],
                "role": user_data["role"],
                "department": user_data["department"],
                "email": user_data["email"]
            })
    
    return render_template('admin.html', 
                         username=payload['sub'], 
                         items=critical_assets,
                         users=user_list)

@app.route('/admin/delete')
def delete_user():
    token = request.cookies.get('session')
    username = request.args.get('username')
    
    if not token:
        return jsonify({"error": "Authentication required"}), 401
    
    payload = verify_jwt_token(token)
    if not payload or payload['sub'] != 'admin':
        return jsonify({"error": "Admin access required"}), 403
    
    if not username:
        return jsonify({"error": "Username parameter required"}), 400
        
    if username == 'admin':
        return jsonify({"error": "Cannot delete admin user"}), 403
    
    if username in users:
        user_info = users[username]
        del users[username]
        return jsonify({
            "success": f"User '{username}' ({user_info['full_name']}) has been successfully deleted from the system",
            "deleted_user": {
                "username": username,
                "full_name": user_info["full_name"],
                "department": user_info["department"]
            }
        })
    
    return jsonify({"error": f"User '{username}' not found"}), 404

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3206, debug=False)