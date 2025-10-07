# JWT Authentication Bypass Lab

## Objective

This cybersecurity lab demonstrates a JWT authentication bypass vulnerability caused by a weak signing key. Participants will learn to identify, exploit, and remediate JWT weaknesses in web applications.

## Lab Environment

**Target Application**: InventoryPro Enterprise Asset Management
**Technology Stack**: Flask, JWT, Docker
**Difficulty**: Intermediate
**Estimated Time**: 30-45 minutes

## Learning Objectives

After completing this lab, participants will be able to:
- Identify JWT tokens in web applications
- Recognize weak JWT signing keys
- Use tools like hashcat to crack JWT secrets
- Forge JWT tokens with elevated privileges
- Access unauthorized administrative functions
- Understand JWT security best practices

## Prerequisites

### Required Tools
- Burp Suite (with JWT Editor extension)
- Hashcat (for secret cracking)
- Web browser with developer tools
- Docker (for lab deployment)

### Required Knowledge
- Basic understanding of web authentication
- Familiarity with HTTP requests/responses
- Basic knowledge of JSON Web Tokens
- Command line usage

## Lab Setup

1. **Deploy the Application**
   ```bash
   cd deploy
   docker-compose up -d
   ```

2. **Verify Deployment**
   ```bash
   curl -f http://localhost:3206/
   ```

3. **Access the Application**
   - URL: http://localhost:3206
   - Test Credentials: `manager` / `supply2024`

## Vulnerability Overview

The application uses JWT tokens for session management but implements a critically weak signing key. This vulnerability allows attackers to:
- Crack the signing secret using common wordlists
- Forge tokens with administrative privileges
- Bypass authorization controls
- Access sensitive administrative functions

## Attack Methodology

### Phase 1: Reconnaissance
1. Examine application authentication mechanism
2. Identify JWT token usage
3. Extract JWT from browser cookies/storage

### Phase 2: Token Analysis
1. Decode JWT structure without verification
2. Analyze header and payload components
3. Identify signing algorithm (HS256)

### Phase 3: Secret Cracking
1. Use hashcat with common wordlists
2. Attempt brute-force attack on signing secret
3. Verify cracked secret against original token

### Phase 4: Token Forgery
1. Create new JWT payload with admin privileges
2. Sign token using cracked secret
3. Replace session token in browser

### Phase 5: Privilege Escalation
1. Access administrative endpoints
2. Extract sensitive information
3. Demonstrate unauthorized access

## Expected Findings

Successful exploitation will reveal:
- Administrative panel access at `/admin`
- Critical asset information
- Security flags demonstrating compromise
- User management capabilities

## Remediation

### Immediate Actions
1. Generate cryptographically strong signing keys
2. Implement key rotation procedures
3. Review all JWT implementations

### Long-term Security
1. Use RSA or ECDSA algorithms where appropriate
2. Implement proper secret management
3. Regular security assessments
4. Monitor for suspicious JWT activities

## Assessment Criteria

Participants will be evaluated on:
- Successful identification of JWT weakness
- Proper use of cracking tools
- Accurate token forgery
- Administrative access achievement
- Understanding of remediation steps

## Additional Resources

- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [OWASP JWT Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [JWT.io Debugger](https://jwt.io/)
- [Hashcat Documentation](https://hashcat.net/hashcat/)

## Lab Completion

Document your findings including:
- Methods used to identify the vulnerability
- Tools and techniques employed
- Specific weaknesses discovered
- Proof of concept screenshots
- Recommended remediation steps
