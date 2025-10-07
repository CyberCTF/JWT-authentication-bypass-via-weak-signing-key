# InventoryPro User Guide

## Overview

InventoryPro is an enterprise-grade inventory management system designed for tracking and managing organizational assets. The system provides role-based access control and secure authentication mechanisms.

## Features

### 🏢 Enterprise Dashboard
- Real-time inventory overview
- Asset categorization and tracking
- Location-based organization
- Status monitoring (Available/Reserved)

### 👥 User Management
- Role-based access control
- Secure JWT authentication
- Session management
- Profile management

### 🔐 Security Features
- JWT token-based authentication
- Role-based authorization
- Secure admin panel
- Session timeout protection

### 🎨 Modern Interface
- Dark theme optimized for long usage
- Responsive design for all devices
- Glassmorphism UI elements
- Accessibility-first approach

## User Roles

### Manager
- Access to standard inventory dashboard
- View all inventory items
- Manage personal account settings
- **Credentials**: `manager` / `supply2024`

### Supervisor
- Enhanced inventory access
- Additional reporting capabilities
- **Credentials**: `supervisor` / `inventory!`

### Administrator
- Full system access
- Critical asset management
- User administration
- **Credentials**: Admin access requires special authorization

## Getting Started

1. **Access the Application**
   ```
   http://localhost:3206
   ```

2. **Login**
   - Use provided credentials for your role
   - System will redirect to appropriate dashboard

3. **Navigate**
   - Use the top navigation menu
   - Access different sections based on your role

4. **Manage Account**
   - Click "Account" to view profile information
   - Monitor session expiration
   - Update security settings

## Security Guidelines

- Always logout when finished
- Do not share account credentials
- Report suspicious activity immediately
- Admin panel access is restricted and monitored

## Technical Requirements

- Modern web browser (Chrome, Firefox, Safari, Edge)
- JavaScript enabled
- Stable internet connection
- Screen resolution: 1024x768 minimum

## Support

For technical support or access issues, contact your system administrator.
