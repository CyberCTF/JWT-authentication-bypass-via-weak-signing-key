import requests

def test_login():
    session = requests.Session()
    print("🔍 Testing InventoryPro login functionality...")
    
    # Test login
    response = session.post('http://localhost:3206/login', data={
        'username': 'manager',
        'password': 'supply2024'
    })
    
    print(f"Login status: {response.status_code}")
    print(f"Redirected to: {response.url}")
    
    # Check if we got a JWT token
    token = session.cookies.get('session')
    if token:
        print(f"✅ JWT token obtained: {token[:50]}...")
        
        # Test dashboard access
        dashboard_response = session.get('http://localhost:3206/dashboard')
        if dashboard_response.status_code == 200:
            print("✅ Dashboard accessible")
        else:
            print(f"❌ Dashboard access failed: {dashboard_response.status_code}")
            
        # Test admin access (should be forbidden)
        admin_response = session.get('http://localhost:3206/admin')
        if admin_response.status_code == 403:
            print("✅ Admin panel properly protected")
        else:
            print(f"⚠️  Admin panel status: {admin_response.status_code}")
    else:
        print("❌ No JWT token received")
    
    print("\n🎯 Login test completed!")

if __name__ == "__main__":
    test_login()
