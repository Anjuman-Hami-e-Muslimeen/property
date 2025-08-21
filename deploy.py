#!/usr/bin/env python3
"""
Deployment helper script for Property Management System
This script helps validate the deployment setup and create necessary files.
"""

import os
import sys
import secrets
import string

def generate_secret_key(length=32):
    """Generate a secure secret key"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'app_production.py',
        'config.py',
        'passenger_wsgi.py',
        '.htaccess',
        'requirements.txt',
        'templates/',
        'uploads/'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def create_env_file():
    """Create .env file with secure defaults"""
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    secret_key = generate_secret_key()
    
    env_content = f"""# Flask Configuration
FLASK_SECRET_KEY={secret_key}
FLASK_ENV=production
FLASK_DEBUG=False

# Database Configuration
DATABASE_URL=sqlite:///property_management.db

# Admin User Configuration
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# File Upload Configuration
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=txt,pdf,png,jpg,jpeg,gif,doc,docx

# Security Configuration
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with secure defaults")
    print("⚠️  IMPORTANT: Change ADMIN_PASSWORD and FLASK_SECRET_KEY in production!")

def validate_structure():
    """Validate the project structure"""
    print("\n🔍 Validating project structure...")
    
    # Check templates
    template_files = [
        'templates/base.html',
        'templates/index.html',
        'templates/login.html',
        'templates/add_property.html',
        'templates/edit_property.html',
        'templates/property_detail.html'
    ]
    
    missing_templates = []
    for template in template_files:
        if not os.path.exists(template):
            missing_templates.append(template)
    
    if missing_templates:
        print("❌ Missing template files:")
        for template in missing_templates:
            print(f"   - {template}")
        return False
    
    print("✅ All template files found")
    return True

def check_permissions():
    """Check and suggest file permissions"""
    print("\n🔐 Checking file permissions...")
    
    files_to_check = [
        ('passenger_wsgi.py', 0o755),
        ('.htaccess', 0o644),
        ('uploads/', 0o755)
    ]
    
    for file_path, expected_permission in files_to_check:
        if os.path.exists(file_path):
            current_permission = oct(os.stat(file_path).st_mode)[-3:]
            expected_permission_str = oct(expected_permission)[-3:]
            
            if current_permission == expected_permission_str:
                print(f"✅ {file_path}: {current_permission}")
            else:
                print(f"⚠️  {file_path}: {current_permission} (should be {expected_permission_str})")
        else:
            print(f"❌ {file_path}: File not found")

def main():
    """Main deployment validation function"""
    print("🚀 Property Management System - Deployment Validator")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Deployment validation failed!")
        sys.exit(1)
    
    # Validate structure
    if not validate_structure():
        print("\n❌ Structure validation failed!")
        sys.exit(1)
    
    # Create .env file if needed
    create_env_file()
    
    # Check permissions
    check_permissions()
    
    print("\n" + "=" * 50)
    print("✅ Deployment validation completed!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your production values")
    print("2. Upload files to your cPanel hosting")
    print("3. Install Python dependencies: pip install -r requirements.txt")
    print("4. Set correct file permissions")
    print("5. Test the application")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

if __name__ == '__main__':
    main() 