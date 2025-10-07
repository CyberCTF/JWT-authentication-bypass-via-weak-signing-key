#!/usr/bin/env python3

import requests
import sys
import time

def test_deployment():
    """Test if the deployment is working correctly"""
    url = "http://localhost:3206"
    
    print("🔍 Testing InventoryPro deployment...")
    
    try:
        # Test main page
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and "InventoryPro" in response.text:
            print("✅ Application is accessible")
        else:
            print("❌ Application not accessible")
            return False
            
        # Test login functionality
        session = requests.Session()
        login_data = {
            "username": "manager",
            "password": "supply2024"
        }
        
        response = session.post(f"{url}/login", data=login_data)
        if response.status_code == 200:
            print("✅ Login functionality working")
        else:
            print("❌ Login functionality failed")
            return False
            
        # Test dashboard access
        response = session.get(f"{url}/dashboard")
        if response.status_code == 200 and "Dashboard" in response.text:
            print("✅ Dashboard accessible")
        else:
            print("❌ Dashboard not accessible")
            return False
            
        # Test admin panel (should be forbidden)
        response = session.get(f"{url}/admin")
        if response.status_code == 403:
            print("✅ Admin panel properly protected")
        else:
            print("❌ Admin panel security issue")
            return False
            
        print("\n🎯 All tests passed! Application is ready for penetration testing.")
        print(f"Access the app at: {url}")
        print("Credentials: manager / supply2024")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    if not test_deployment():
        sys.exit(1)
