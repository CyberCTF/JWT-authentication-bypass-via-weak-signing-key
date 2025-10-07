#!/usr/bin/env python3
"""
Main test runner for JWT Authentication Bypass via Weak Signing Key lab
"""
import sys
import os
import subprocess
import json
from pathlib import Path

# Add the parent directory to Python path to import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_syntax_check():
    """Check Python syntax of main app file"""
    print("🔍 Running syntax check...")
    try:
        import app
        print("✅ Syntax check passed")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_import_tests():
    """Test that all required modules can be imported"""
    print("📦 Testing imports...")
    required_modules = ['flask', 'jwt', 'datetime', 'uuid', 'hashlib']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    
    return True

def run_jwt_tests():
    """Test JWT functionality"""
    print("🔐 Testing JWT functionality...")
    try:
        from app import create_jwt_token, verify_jwt_token, JWT_SECRET
        
        # Test token creation
        token = create_jwt_token("testuser", "admin")
        assert token is not None, "Token creation failed"
        print("✅ JWT token creation works")
        
        # Test token verification
        payload = verify_jwt_token(token)
        assert payload is not None, "Token verification failed"
        assert payload['sub'] == "testuser", "Token payload incorrect"
        assert payload['role'] == "admin", "Token role incorrect"
        print("✅ JWT token verification works")
        
        # Test weak secret (vulnerability check)
        assert JWT_SECRET == "admin123", "JWT secret should be weak for the lab"
        print("✅ Weak JWT secret confirmed (vulnerability present)")
        
        return True
    except Exception as e:
        print(f"❌ JWT test failed: {e}")
        return False

def run_user_authentication_tests():
    """Test user authentication logic"""
    print("👤 Testing user authentication...")
    try:
        from app import users
        
        # Test that users exist
        assert "admin" in users, "Admin user not found"
        assert "manager" in users, "Manager user not found"
        print(f"✅ Found {len(users)} users in system")
        
        # Test admin user has correct credentials
        admin = users["admin"]
        assert admin["password"] == "warehouse_secure", "Admin password incorrect"
        assert admin["role"] == "admin", "Admin role incorrect"
        print("✅ Admin user configured correctly")
        
        return True
    except Exception as e:
        print(f"❌ User authentication test failed: {e}")
        return False

def run_app_routes_test():
    """Test that Flask app routes are defined"""
    print("🛣️ Testing Flask routes...")
    try:
        from app import app
        
        expected_routes = ['/', '/login', '/dashboard', '/my-account', '/admin', '/admin/delete', '/logout']
        
        # Get all routes from Flask app
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(rule.rule)
        
        for expected_route in expected_routes:
            assert expected_route in routes, f"Route {expected_route} not found"
            print(f"✅ Route {expected_route} defined")
        
        return True
    except Exception as e:
        print(f"❌ Routes test failed: {e}")
        return False

def run_vulnerability_checks():
    """Check that the intended vulnerabilities are present"""
    print("🚨 Checking intended vulnerabilities...")
    try:
        from app import JWT_SECRET, JWT_ALGORITHM
        
        # Check 1: Weak JWT secret
        weak_secrets = ["admin123", "secret", "password", "123456"]
        assert JWT_SECRET in weak_secrets, f"JWT secret '{JWT_SECRET}' should be weak"
        print("✅ Weak JWT secret vulnerability present")
        
        # Check 2: HS256 algorithm (vulnerable to key confusion)
        assert JWT_ALGORITHM == "HS256", "Should use HS256 algorithm for vulnerability"
        print("✅ HS256 algorithm vulnerability present")
        
        return True
    except Exception as e:
        print(f"❌ Vulnerability check failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🧪 Starting JWT Authentication Bypass Lab Tests")
    print("=" * 60)
    
    tests = [
        ("Syntax Check", run_syntax_check),
        ("Import Tests", run_import_tests),
        ("JWT Tests", run_jwt_tests),
        ("User Authentication Tests", run_user_authentication_tests),
        ("Flask Routes Test", run_app_routes_test),
        ("Vulnerability Checks", run_vulnerability_checks)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Lab is ready for deployment.")
        return 0
    else:
        print("💥 Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())