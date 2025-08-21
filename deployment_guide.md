# Property Management System - cPanel Deployment Guide

## Prerequisites

- cPanel hosting account with Python support
- Python 3.7+ installed on your hosting
- Access to cPanel File Manager or FTP

## Step 1: Prepare Your Local Project

1. **Create the .env file** (copy from env_template.txt):
   ```bash
   cp env_template.txt .env
   ```

2. **Update the .env file** with your production values:
   ```env
   FLASK_SECRET_KEY=your-super-secret-production-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD=your-secure-admin-password
   ```

## Step 2: Upload to cPanel

1. **Create a ZIP file** of your project (excluding unnecessary files):
   - Include: `app_production.py`, `config.py`, `passenger_wsgi.py`, `.htaccess`, `requirements.txt`, `templates/`, `static/` (if any)
   - Exclude: `app.py`, `*.pyc`, `__pycache__/`, `.env`, `property_management.db`

2. **Upload to cPanel**:
   - Log into cPanel
   - Go to File Manager
   - Navigate to your domain's public_html directory
   - Upload and extract the ZIP file

## Step 3: Set Up Python Environment

1. **Create Python App** (if using cPanel's Python Selector):
   - Go to "Setup Python App" in cPanel
   - Create a new application
   - Set Python version to 3.7 or higher
   - Set application root to your project directory
   - Set application URL to your domain

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Step 4: Configure Environment Variables

1. **Create .env file on server**:
   - In File Manager, create a new file named `.env`
   - Add your production environment variables:
   ```env
   FLASK_SECRET_KEY=your-super-secret-production-key-here
   FLASK_ENV=production
   FLASK_DEBUG=False
   DATABASE_URL=sqlite:///property_management.db
   ADMIN_USERNAME=your-admin-username
   ADMIN_PASSWORD=your-secure-admin-password
   MAX_CONTENT_LENGTH=16777216
   UPLOAD_FOLDER=uploads
   ALLOWED_EXTENSIONS=txt,pdf,png,jpg,jpeg,gif,doc,docx
   SESSION_COOKIE_SECURE=True
   SESSION_COOKIE_HTTPONLY=True
   SESSION_COOKIE_SAMESITE=Lax
   ```

## Step 5: Update passenger_wsgi.py

1. **Edit passenger_wsgi.py**:
   - Update the INTERP path to match your Python installation:
   ```python
   INTERP = os.path.expanduser("/home/YOUR_CPANEL_USERNAME/virtualenv/YOUR_APP_NAME/3.9/bin/python")
   ```

## Step 6: Set File Permissions

1. **Set correct permissions**:
   ```bash
   chmod 755 passenger_wsgi.py
   chmod 644 .htaccess
   chmod 600 .env
   chmod 755 uploads/
   ```

## Step 7: Test the Application

1. **Visit your domain** to test the application
2. **Login** with your admin credentials
3. **Test file uploads** and other features

## Security Considerations

### 1. Environment Variables
- Never commit `.env` file to version control
- Use strong, unique passwords
- Generate a secure FLASK_SECRET_KEY

### 2. File Permissions
- Keep `.env` file readable only by the web server
- Ensure uploads directory is writable but not executable
- Protect database files from direct access

### 3. Database Security
- Consider using MySQL/PostgreSQL for production
- Regularly backup your database
- Use strong admin passwords

### 4. SSL/HTTPS
- Enable SSL certificate in cPanel
- Update SESSION_COOKIE_SECURE=True in production

## Troubleshooting

### Common Issues:

1. **500 Internal Server Error**:
   - Check passenger_wsgi.py Python path
   - Verify all dependencies are installed
   - Check error logs in cPanel

2. **Import Errors**:
   - Ensure all required packages are in requirements.txt
   - Check Python version compatibility

3. **File Upload Issues**:
   - Verify uploads directory permissions
   - Check MAX_CONTENT_LENGTH setting
   - Ensure directory is writable

4. **Database Issues**:
   - Check database file permissions
   - Verify database path in configuration

### Error Logs:
- Check cPanel Error Logs
- Review Python application logs
- Monitor file permissions

## Maintenance

### Regular Tasks:
1. **Backup database** regularly
2. **Update dependencies** periodically
3. **Monitor disk space** (uploads folder)
4. **Review error logs**
5. **Update admin passwords** regularly

### Performance Optimization:
1. **Enable caching** for static files
2. **Optimize images** before upload
3. **Monitor database size**
4. **Consider CDN** for static assets

## Support

If you encounter issues:
1. Check cPanel error logs
2. Verify file permissions
3. Test with a simple Flask app first
4. Contact your hosting provider for Python-specific issues

## Files Structure for Deployment

```
public_html/
├── app_production.py      # Main application
├── config.py             # Configuration
├── passenger_wsgi.py     # WSGI entry point
├── .htaccess            # Apache configuration
├── .env                 # Environment variables (create on server)
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
├── uploads/            # File uploads directory
└── property_management.db  # Database (created automatically)
```

## Quick Deployment Checklist

- [ ] Upload all project files
- [ ] Create and configure .env file
- [ ] Update passenger_wsgi.py Python path
- [ ] Install Python dependencies
- [ ] Set correct file permissions
- [ ] Test application functionality
- [ ] Configure SSL certificate
- [ ] Set up regular backups
- [ ] Test file uploads
- [ ] Verify admin login works