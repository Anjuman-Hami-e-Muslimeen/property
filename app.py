from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this in production

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['password_hash'])
    return None

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect('property_management.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  created_date TEXT)''')
    
    # Create properties table
    c.execute('''CREATE TABLE IF NOT EXISTS properties
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT,
                  property_type TEXT,
                  price REAL,
                  location TEXT,
                  bedrooms INTEGER,
                  bathrooms INTEGER,
                  area REAL,
                  status TEXT DEFAULT 'Available',
                  owner_name TEXT,
                  owner_contact TEXT,
                  created_date TEXT,
                  updated_date TEXT)''')
    
    # Create documents table
    c.execute('''CREATE TABLE IF NOT EXISTS property_documents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  property_id INTEGER,
                  filename TEXT,
                  original_filename TEXT,
                  document_type TEXT DEFAULT 'General',
                  upload_date TEXT,
                  FOREIGN KEY (property_id) REFERENCES properties (id))''')
    
    # Create Google Maps links table
    c.execute('''CREATE TABLE IF NOT EXISTS property_maps_links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  property_id INTEGER,
                  link_title TEXT NOT NULL,
                  google_maps_link TEXT NOT NULL,
                  latitude REAL,
                  longitude REAL,
                  created_date TEXT,
                  FOREIGN KEY (property_id) REFERENCES properties (id))''')
    
    # Create default admin user if not exists
    admin_username = 'admin'
    admin_password = 'admin123'  # Change this in production
    
    existing_user = c.execute('SELECT * FROM users WHERE username = ?', (admin_username,)).fetchone()
    if not existing_user:
        password_hash = generate_password_hash(admin_password)
        current_time = datetime.now().isoformat()
        c.execute('INSERT INTO users (username, password_hash, created_date) VALUES (?, ?, ?)',
                 (admin_username, password_hash, current_time))
    
    conn.commit()
    conn.close()
    
    # Run database migrations
    migrate_db()

def migrate_db():
    """Migrate existing database to new schema"""
    conn = sqlite3.connect('property_management.db')
    c = conn.cursor()
    
    try:
        # Check if document_type column exists in property_documents table
        c.execute("PRAGMA table_info(property_documents)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'document_type' not in columns:
            # Add document_type column to existing property_documents table
            c.execute('ALTER TABLE property_documents ADD COLUMN document_type TEXT DEFAULT "General"')
            print("Added document_type column to property_documents table")
        
        # Check if property_maps_links table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='property_maps_links'")
        if not c.fetchone():
            # Create property_maps_links table
            c.execute('''CREATE TABLE property_maps_links
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         property_id INTEGER,
                         link_title TEXT NOT NULL,
                         google_maps_link TEXT NOT NULL,
                         latitude REAL,
                         longitude REAL,
                         created_date TEXT,
                         FOREIGN KEY (property_id) REFERENCES properties (id))''')
            print("Created property_maps_links table")
        
        conn.commit()
        print("Database migration completed successfully")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect('property_management.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['username'], user_data['password_hash'])
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties ORDER BY created_date DESC').fetchall()
    
    # Get photos for each property
    properties_with_photos = []
    for property in properties:
        photos = conn.execute('''SELECT * FROM property_documents 
                               WHERE property_id = ? AND document_type = 'Photos' 
                               ORDER BY upload_date DESC LIMIT 1''', (property['id'],)).fetchall()
        property_dict = dict(property)
        property_dict['photos'] = photos
        properties_with_photos.append(property_dict)
    
    conn.close()
    return render_template('index.html', properties=properties_with_photos)

@app.route('/property/<int:property_id>')
@login_required
def property_detail(property_id):
    conn = get_db_connection()
    property_data = conn.execute('SELECT * FROM properties WHERE id = ?', (property_id,)).fetchone()
    documents = conn.execute('SELECT * FROM property_documents WHERE property_id = ? ORDER BY upload_date DESC', (property_id,)).fetchall()
    maps_links = conn.execute('SELECT * FROM property_maps_links WHERE property_id = ? ORDER BY created_date DESC', (property_id,)).fetchall()
    conn.close()
    
    if property_data is None:
        flash('Property not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('property_detail.html', property=property_data, documents=documents, maps_links=maps_links)

@app.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        property_type = request.form['property_type']
        price = float(request.form['price']) if request.form['price'] else 0.0
        location = request.form['location']
        bedrooms = int(request.form['bedrooms']) if request.form['bedrooms'] else 0
        bathrooms = int(request.form['bathrooms']) if request.form['bathrooms'] else 0
        area = float(request.form['area']) if request.form['area'] else 0.0
        status = request.form['status']
        owner_name = request.form['owner_name']
        owner_contact = request.form['owner_contact']
        
        current_time = datetime.now().isoformat()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO properties 
                         (title, description, property_type, price, location, bedrooms, bathrooms, area, status, owner_name, owner_contact, created_date, updated_date)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (title, description, property_type, price, location, bedrooms, bathrooms, area, status, owner_name, owner_contact, current_time, current_time))
        
        property_id = cursor.lastrowid
        
        # Handle Google Maps data
        google_maps_link = request.form.get('google_maps_link')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        if google_maps_link or (latitude and longitude):
            # Validate coordinates if provided
            if latitude and longitude:
                try:
                    latitude = float(latitude)
                    longitude = float(longitude)
                except ValueError:
                    latitude = None
                    longitude = None
            
            cursor.execute('''INSERT INTO property_maps_links 
                           (property_id, link_title, google_maps_link, latitude, longitude, created_date)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                        (property_id, 'Property Location', google_maps_link or '', latitude, longitude, current_time))
        
        # Handle file uploads
        if 'documents' in request.files:
            files = request.files.getlist('documents')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Save to database
                    cursor.execute('''INSERT INTO property_documents (property_id, filename, original_filename, document_type, upload_date)
                                     VALUES (?, ?, ?, ?, ?)''',
                                  (property_id, filename, file.filename, 'General', current_time))
        
        conn.commit()
        conn.close()
        
        flash('Property added successfully!', 'success')
        return redirect(url_for('property_detail', property_id=property_id))
    
    return render_template('add_property.html')

@app.route('/edit_property/<int:property_id>', methods=['GET', 'POST'])
@login_required
def edit_property(property_id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        property_type = request.form['property_type']
        price = float(request.form['price']) if request.form['price'] else 0.0
        location = request.form['location']
        bedrooms = int(request.form['bedrooms']) if request.form['bedrooms'] else 0
        bathrooms = int(request.form['bathrooms']) if request.form['bathrooms'] else 0
        area = float(request.form['area']) if request.form['area'] else 0.0
        status = request.form['status']
        owner_name = request.form['owner_name']
        owner_contact = request.form['owner_contact']
        
        updated_time = datetime.now().isoformat()
        
        conn.execute('''UPDATE properties 
                       SET title = ?, description = ?, property_type = ?, price = ?, location = ?, 
                           bedrooms = ?, bathrooms = ?, area = ?, status = ?, owner_name = ?, 
                           owner_contact = ?, updated_date = ?
                       WHERE id = ?''',
                    (title, description, property_type, price, location, bedrooms, bathrooms, area, 
                     status, owner_name, owner_contact, updated_time, property_id))
        
        conn.commit()
        conn.close()
        
        flash('Property updated successfully!', 'success')
        return redirect(url_for('property_detail', property_id=property_id))
    
    property_data = conn.execute('SELECT * FROM properties WHERE id = ?', (property_id,)).fetchone()
    conn.close()
    
    if property_data is None:
        flash('Property not found!', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_property.html', property=property_data)

@app.route('/delete_property/<int:property_id>', methods=['POST'])
@login_required
def delete_property(property_id):
    conn = get_db_connection()
    
    # Delete associated documents from filesystem
    documents = conn.execute('SELECT filename FROM property_documents WHERE property_id = ?', (property_id,)).fetchall()
    for doc in documents:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], doc['filename'])
        if os.path.exists(file_path):
            os.remove(file_path)
    
    # Delete from database
    conn.execute('DELETE FROM property_documents WHERE property_id = ?', (property_id,))
    conn.execute('DELETE FROM property_maps_links WHERE property_id = ?', (property_id,))
    conn.execute('DELETE FROM properties WHERE id = ?', (property_id,))
    
    conn.commit()
    conn.close()
    
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/add_maps_link/<int:property_id>', methods=['POST'])
@login_required
def add_maps_link(property_id):
    link_title = request.form['link_title']
    google_maps_link = request.form['google_maps_link']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    # Validate coordinates if provided
    if latitude and longitude:
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            flash('Invalid coordinates provided.', 'error')
            return redirect(url_for('property_detail', property_id=property_id))
    
    current_time = datetime.now().isoformat()
    
    conn = get_db_connection()
    conn.execute('''INSERT INTO property_maps_links 
                   (property_id, link_title, google_maps_link, latitude, longitude, created_date)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (property_id, link_title, google_maps_link, latitude, longitude, current_time))
    conn.commit()
    conn.close()
    
    flash('Google Maps link added successfully!', 'success')
    return redirect(url_for('property_detail', property_id=property_id))

@app.route('/delete_maps_link/<int:link_id>', methods=['POST'])
@login_required
def delete_maps_link(link_id):
    conn = get_db_connection()
    link_data = conn.execute('SELECT property_id FROM property_maps_links WHERE id = ?', (link_id,)).fetchone()
    
    if link_data:
        property_id = link_data['property_id']
        conn.execute('DELETE FROM property_maps_links WHERE id = ?', (link_id,))
        conn.commit()
        conn.close()
        flash('Google Maps link deleted successfully!', 'success')
        return redirect(url_for('property_detail', property_id=property_id))
    
    conn.close()
    flash('Link not found!', 'error')
    return redirect(url_for('index'))

@app.route('/add_document/<int:property_id>', methods=['POST'])
@login_required
def add_document(property_id):
    if 'document' not in request.files:
        flash('No file selected.', 'error')
        return redirect(url_for('property_detail', property_id=property_id))
    
    file = request.files['document']
    document_type = request.form.get('document_type', 'General')
    
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('property_detail', property_id=property_id))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        current_time = datetime.now().isoformat()
        
        conn = get_db_connection()
        conn.execute('''INSERT INTO property_documents (property_id, filename, original_filename, document_type, upload_date)
                       VALUES (?, ?, ?, ?, ?)''',
                    (property_id, filename, file.filename, document_type, current_time))
        conn.commit()
        conn.close()
        
        flash('Document uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Allowed types: txt, pdf, png, jpg, jpeg, gif, doc, docx', 'error')
    
    return redirect(url_for('property_detail', property_id=property_id))

@app.route('/delete_document/<int:document_id>', methods=['POST'])
@login_required
def delete_document(document_id):
    conn = get_db_connection()
    doc_data = conn.execute('SELECT property_id, filename FROM property_documents WHERE id = ?', (document_id,)).fetchone()
    
    if doc_data:
        property_id = doc_data['property_id']
        filename = doc_data['filename']
        
        # Delete file from filesystem
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        conn.execute('DELETE FROM property_documents WHERE id = ?', (document_id,))
        conn.commit()
        conn.close()
        
        flash('Document deleted successfully!', 'success')
        return redirect(url_for('property_detail', property_id=property_id))
    
    conn.close()
    flash('Document not found!', 'error')
    return redirect(url_for('index'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)