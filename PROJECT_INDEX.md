# Property Management System - Project Index

## 📋 Project Overview

This is a **Flask-based Property Management System** designed for real estate professionals to manage property listings, documents, and client information. The application provides a complete CRUD (Create, Read, Update, Delete) interface for property management with document upload capabilities.

## 🏗️ Architecture & Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Database**: SQLite (property_management.db)
- **File Handling**: Werkzeug 2.3.7
- **Authentication**: Flask-Login 0.6.3
- **WSGI Server**: Passenger (for cPanel deployment)

### Frontend
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Responsive Design**: Mobile-first approach

### Deployment
- **Platform**: cPanel with Python App support
- **WSGI Entry Point**: passenger_wsgi.py
- **Environment**: Production-ready configuration

## 📁 Project Structure

```
property_management/
├── app.py                          # Main Flask application
├── passenger_wsgi.py               # WSGI entry point for cPanel
├── requirements.txt                # Python dependencies
├── deployment_guide.md             # Detailed deployment instructions
├── property_management.db          # SQLite database (auto-generated)
├── PROJECT_INDEX.md               # This project index file
├── templates/                      # HTML templates
│   ├── base.html                   # Base template with navigation
│   ├── login.html                  # User authentication login page
│   ├── index.html                  # Property listings page
│   ├── add_property.html           # Add new property form
│   ├── edit_property.html          # Edit property form
│   └── property_detail.html        # Property detail view
└── uploads/                        # Document storage
    ├── 20250821_102855_Websites_Report.pdf
    └── 20250821_103303_Websites_Report.pdf
```

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-incrementing unique identifier |
| username | TEXT UNIQUE NOT NULL | User's login username |
| password_hash | TEXT NOT NULL | Hashed password for security |
| created_date | TEXT | ISO format timestamp |

### Properties Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-incrementing unique identifier |
| title | TEXT NOT NULL | Property title/name |
| description | TEXT | Detailed property description |
| property_type | TEXT | Type (Apartment, House, Villa, etc.) |
| price | REAL | Property price in ₹ |
| location | TEXT | Property location/address |
| bedrooms | INTEGER | Number of bedrooms |
| bathrooms | INTEGER | Number of bathrooms |
| area | REAL | Property area in sq ft |
| status | TEXT DEFAULT 'Available' | Status (Available, Pending, Sold, Rented) |
| owner_name | TEXT | Property owner's name |
| owner_contact | TEXT | Owner's contact information |
| created_date | TEXT | ISO format timestamp |
| updated_date | TEXT | ISO format timestamp |

### Property Documents Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-incrementing unique identifier |
| property_id | INTEGER | Foreign key to properties table |
| filename | TEXT | Stored filename with timestamp |
| original_filename | TEXT | Original uploaded filename |
| upload_date | TEXT | ISO format timestamp |

## 🚀 Core Features

### 1. Property Management
- ✅ **Add Properties**: Comprehensive form with all property details
- ✅ **Edit Properties**: Update existing property information
- ✅ **Delete Properties**: Remove properties with confirmation
- ✅ **View Properties**: List all properties with search-friendly cards
- ✅ **Property Details**: Detailed view with all information

### 2. Document Management
- ✅ **File Upload**: Support for multiple file types (PDF, Images, Documents)
- ✅ **Secure Storage**: Files stored with timestamped names
- ✅ **Download**: Direct file download functionality
- ✅ **File Type Validation**: Restricted to safe file types
- ✅ **Size Limits**: 16MB maximum file size

### 3. User Interface
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Bootstrap Styling**: Modern, professional appearance
- ✅ **Status Indicators**: Color-coded property status badges
- ✅ **Property Cards**: Attractive card-based layout
- ✅ **Navigation**: Easy-to-use navigation menu

### 4. Data Management
- ✅ **Form Validation**: Client and server-side validation
- ✅ **Error Handling**: User-friendly error messages
- ✅ **Flash Messages**: Success/error notifications
- ✅ **Data Sanitization**: Secure input handling

### 5. Authentication
- ✅ **User Login**: Secure authentication system
- ✅ **Password Hashing**: Secure password storage
- ✅ **Protected Routes**: All features require login
- ✅ **Session Management**: Automatic session handling
- ✅ **Logout Functionality**: Secure logout process

## 🔧 Technical Implementation

### Flask Routes
- `/login` - User authentication login page
- `/logout` - User logout (redirects to login)
- `/` - Home page with property listings (protected)
- `/property/<id>` - Individual property detail view (protected)
- `/add_property` - Add new property form (protected)
- `/edit_property/<id>` - Edit existing property (protected)
- `/delete_property/<id>` - Delete property (POST, protected)
- `/download/<filename>` - Download uploaded files (protected)

### Key Functions
- `init_db()` - Database initialization (creates default admin user)
- `allowed_file()` - File type validation
- `get_db_connection()` - Database connection helper
- `load_user()` - Flask-Login user loader
- `login_user()` - User authentication
- `logout_user()` - User logout

### Security Features
- User authentication with Flask-Login
- Password hashing with Werkzeug
- Input validation and sanitization
- Secure filename handling
- File type restrictions
- CSRF protection ready
- SQL injection prevention
- Protected routes requiring login

## 📱 User Interface Components

### Navigation
- **Brand**: Property Manager with home icon
- **Menu Items**: All Properties, Add Property
- **User Menu**: Username display with logout option
- **Responsive**: Collapsible mobile menu

### Property Cards (Index Page)
- Property image placeholder
- Status badge (Available/Pending/Sold/Rented)
- Title and location
- Key details (bedrooms, bathrooms, area)
- Price display
- View details button

### Property Detail Page
- Large property image placeholder
- Complete property information
- Contact information sidebar
- Document downloads
- Action buttons (Edit, Delete, Back)

### Forms
- **Login Form**: Username and password authentication
- **Add Property**: Comprehensive form with all fields
- **Edit Property**: Pre-populated form for updates
- **File Upload**: Multiple file selection
- **Validation**: Required field indicators

## 🎨 Design Features

### Color Scheme
- **Primary**: Bootstrap blue (#0d6efd)
- **Success**: Green (#28a745) for available properties
- **Warning**: Yellow (#ffc107) for pending properties
- **Danger**: Red (#dc3545) for sold/rented properties

### Typography
- **Icons**: Font Awesome for visual elements
- **Fonts**: Bootstrap default system fonts
- **Responsive**: Scalable text sizes

### Layout
- **Grid System**: Bootstrap responsive grid
- **Cards**: Material design-inspired cards
- **Shadows**: Subtle depth with shadow-sm
- **Hover Effects**: Interactive card animations

## 📊 Current Data

### Sample Files
The system currently contains:
- 2 PDF documents in the uploads folder
- Database file (property_management.db) - auto-generated
- Default admin user (username: admin, password: admin123)

### File Types Supported
- **Documents**: PDF, DOC, DOCX, TXT
- **Images**: PNG, JPG, JPEG, GIF
- **Size Limit**: 16MB per file

## 🚀 Deployment Information

### cPanel Deployment
- **WSGI File**: passenger_wsgi.py
- **Python Version**: 3.8+ recommended
- **Dependencies**: Flask, Werkzeug
- **File Permissions**: 755 for folders, 644 for files

### Environment Variables
- `FLASK_ENV`: production
- `SECRET_KEY`: Custom secret key (change in production)

## 🔄 Development Workflow

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Run application: `python app.py`
3. Access at: `http://localhost:5000`

### Production Deployment
1. Upload files to cPanel
2. Configure Python App in cPanel
3. Set environment variables
4. Restart application

## 🛠️ Maintenance & Updates

### Database Backup
- Regular backup of `property_management.db`
- Backup `uploads/` folder contents
- Keep configuration file copies

### Logs
- Application logs: `/home/anjumanedu/logs/passenger.log`
- cPanel error logs for debugging

## 🎯 Future Enhancements

### Immediate Improvements
- [ ] Image upload and display for properties
- [ ] Search and filter functionality
- [ ] Multiple user accounts and roles
- [ ] Admin dashboard
- [ ] Property image gallery

### Advanced Features
- [ ] Email notifications for inquiries
- [ ] Map integration (Google Maps)
- [ ] Property comparison feature
- [ ] Export to PDF/Excel
- [ ] Advanced reporting
- [ ] Multi-language support

## 📞 Support & Documentation

### Key Files
- **app.py**: Main application logic
- **deployment_guide.md**: Detailed deployment instructions
- **requirements.txt**: Python dependencies
- **passenger_wsgi.py**: Production WSGI configuration

### Troubleshooting
- Check Python version compatibility
- Verify file permissions
- Review application logs
- Test database connectivity

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: Production Ready 