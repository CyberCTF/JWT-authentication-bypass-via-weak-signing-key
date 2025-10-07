# JWT Authentication Bypass via Weak Signing Key

## Scenario
Vulnerability lab demonstrating a critical flaw in JWT authentication using weak signing keys. The application's inventory management system uses a predictable secret key that can be easily cracked, allowing attackers to forge admin tokens and gain unauthorized access.

## How to run
```bash
git clone https://github.com/CyberCTF/JWT-authentication-bypass-via-weak-signing-key.git
cd JWT-authentication-bypass-via-weak-signing-key
docker compose -f deploy/docker-compose.dev.yml up -d --build
```

**Access**: http://localhost:3206




