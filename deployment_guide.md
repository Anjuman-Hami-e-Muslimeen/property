# Property Management System - cPanel Deployment Guide

## 🚀 Quick Setup Instructions

### Step 1: Prepare Your Files
Create the following folder structure on your local machine:

```
property_management/
├── app.py
├── passenger_wsgi.py
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── add_property.html
│   ├── edit_property.html
│   └── property_detail.html
└── uploads/ (create empty folder)
```

### Step 2: Upload to cPanel
1. **Compress all files** into a ZIP archive
2. **Upload to cPanel File Manager** in your application root directory (e.g., `/home/anjumanedu/`)
3. **Extract the files** in the File Manager
4. **Set folder permissions**:
   - `uploads/` folder: 755 or 777 (for file uploads)
   - All Python files: 644

### Step 3: Configure Python App in cPanel
1. Go to **Python App** section in cPanel
2. Click **Create Application**
3. Fill in the details:
   - **Python version**: Select latest available (3.8+ recommended)
   - **Application root**: `/home/anjumanedu/property_management` (or your path)
   - **Application URL**: Choose your desired URL
   - **Application startup file**: `passenger_wsgi.py`
   - **Application Entry point**: `application`

### Step 4: Install Dependencies
1. In the Python App interface, click **Open Terminal**
2. Run: `pip install -r requirements.txt`
3. Or manually install: `pip install Flask==2.3.3 Werkzeug==2.3.7 Flask-Login==0.6.3`

### Step 5: Environment Setup
1. In the Python App **Environment variables** section, add:
   - `FLASK_ENV`: `production`
   - `SECRET_KEY`: `your-secret-production-key-here`

### Step 6: Final Configuration
1. **Restart the application** in cPanel Python App interface
2. **Test the application** by visiting your application URL
3. **Check logs** if there are any issues (Passenger log file path: `/home/anjumanedu/logs/passenger.log`)

## 🔧 File Descriptions

### Core Files
- **app.py**: Main Flask application with all routes, database operations, and authentication
- **passenger_wsgi.py**: WSGI entry point for cPanel deployment
- **requirements.txt**: Python package dependencies

### Templates
- **base.html**: Base template with navigation and common styling
- **login.html**: User authentication login page
- **index.html**: Main property listings page
- **add_property.html**: Form to add new properties
- **edit_property.html**: Form to edit existing properties
- **property_detail.html**: Detailed view of individual properties

## 📁 Database
- **SQLite database**: `property_management.db` (auto-created on first run)
- **Tables**: `users`, `properties`, and `property_documents`
- **File uploads**: Stored in `uploads/` folder
- **Default admin user**: username: `admin`, password: `admin123` (change in production)

## 🛠 Features Included

### Property Management
- ✅ Add new properties with detailed information
- ✅ Edit existing property details
- ✅ Delete properties (with confirmation)
- ✅ View property listings with search-friendly layout
- ✅ Property status tracking (Available, Pending, Sold, Rented)

### Document Management
- ✅ Upload multiple documents per property
- ✅ Download documents
- ✅ Secure file handling with filename sanitization

### User Interface
- ✅ Responsive Bootstrap design
- ✅ Mobile-friendly interface
- ✅ Professional property cards layout
- ✅ Form validation and error handling
- ✅ User authentication system
- ✅ Secure login/logout functionality

## 🔒 Security Features
- User authentication with Flask-Login
- Password hashing with Werkzeug
- Input validation and sanitization
- Secure filename handling for uploads
- CSRF protection ready (secret key configured)
- File type restrictions for uploads
- Protected routes requiring login

## 📊 Database Schema

### Users Table
```sql
- id (PRIMARY KEY)
- username (TEXT, UNIQUE, NOT NULL)
- password_hash (TEXT, NOT NULL)
- created_date (TEXT)
```

### Properties Table
```sql
- id (PRIMARY KEY)
- title (TEXT, NOT NULL)
- description (TEXT)
- property_type (TEXT)
- price (REAL)
- location (TEXT)
- bedrooms (INTEGER)
- bathrooms (INTEGER)
- area (REAL)
- status (TEXT, DEFAULT 'Available')
- owner_name (TEXT)
- owner_contact (TEXT)
- created_date (TEXT)
- updated_date (TEXT)
```

### Property Documents Table
```sql
- id (PRIMARY KEY)
- property_id (INTEGER, FOREIGN KEY)
- filename (TEXT)
- original_filename (TEXT)
- upload_date (TEXT)
```

## 🚨 Troubleshooting

### Common Issues

1. **Application won't start**
   - Check Python version compatibility
   - Verify all files are uploaded correctly
   - Check passenger_wsgi.py path

2. **Database errors**
   - Ensure write permissions on application directory
   - Check if SQLite is available on the server

3. **File upload issues**
   - Set `uploads/` folder permissions to 755 or 777
   - Check max file size limits in cPanel

4. **Template not found errors**
   - Verify `templates/` folder structure
   - Check file case sensitivity (Linux servers)

### Log Files
- Check `/home/anjumanedu/logs/passenger.log` for application errors
- Use cPanel Error Logs for detailed debugging

## 🔄 Updates and Maintenance

### Adding New Features
1. Modify `app.py` for new routes
2. Create corresponding HTML templates
3. Update database schema if needed
4. Restart application in cPanel

### Backup Strategy
- Regularly backup `property_management.db`
- Backup `uploads/` folder contents
- Keep copies of configuration files

## 🎯 Next Steps for Enhancement

### Immediate Improvements
- Add image upload and display for properties
- Implement search and filter functionality
- Add user authentication system
- Create admin dashboard

### Advanced Features
- Email notifications for property inquiries
- Integration with map services
- Property comparison feature
- Export property data to PDF/Excel

## 📞 Support
For technical issues:
1. Check cPanel documentation for Python apps
2. Review Flask documentation for application issues
3. Contact your hosting provider for server-specific problems

---

**Note**: Replace `/home/anjumanedu/` with your actual cPanel home directory path throughout the setup process.