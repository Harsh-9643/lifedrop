from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///lifedrop.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ──────────────── MODELS ────────────────

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    age = db.Column(db.Integer)
    last_donated = db.Column(db.String(50))
    is_available = db.Column(db.Boolean, default=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

class Camp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50))
    organizer = db.Column(db.String(100))
    contact = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Emergency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    units_needed = db.Column(db.Integer, nullable=False)
    hospital = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    urgency = db.Column(db.String(20), default='urgent')
    is_fulfilled = db.Column(db.Boolean, default=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)

# ──────────────── ADMIN CREDENTIALS ────────────────
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'lifedrop2024')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ──────────────── PUBLIC ROUTES ────────────────

@app.route('/')
def index():
    donors_count = Donor.query.filter_by(is_available=True).count()
    camps_count = Camp.query.count()
    emergencies_count = Emergency.query.filter_by(is_fulfilled=False).count()
    recent_camps = Camp.query.order_by(Camp.created_at.desc()).limit(3).all()
    active_emergencies = Emergency.query.filter_by(is_fulfilled=False).order_by(Emergency.requested_at.desc()).limit(3).all()
    return render_template('index.html', donors_count=donors_count, camps_count=camps_count,
                           emergencies_count=emergencies_count, recent_camps=recent_camps,
                           active_emergencies=active_emergencies)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        age_raw = request.form.get('age', '')
        donor = Donor(
            name=request.form['name'],
            blood_group=request.form['blood_group'],
            city=request.form['city'],
            phone=request.form['phone'],
            email=request.form.get('email', ''),
            age=int(age_raw) if age_raw.isdigit() else None,
            last_donated=request.form.get('last_donated', '')
        )
        db.session.add(donor)
        db.session.commit()
        flash('Thank you for registering as a donor!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/find_donor', methods=['GET', 'POST'])
def find_donor():
    donors = []
    camps = Camp.query.order_by(Camp.date.asc()).all()
    if request.method == 'POST':
        blood_group = request.form.get('blood_group', '')
        city = request.form.get('city', '')
        query = Donor.query.filter_by(is_available=True)
        if blood_group:
            query = query.filter_by(blood_group=blood_group)
        if city:
            query = query.filter(Donor.city.ilike(f'%{city}%'))
        donors = query.all()
    return render_template('find_donor.html', donors=donors, camps=camps)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        msg = Contact(
            name=request.form['name'],
            email=request.form['email'],
            subject=request.form.get('subject', ''),
            message=request.form['message']
        )
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/emergency', methods=['GET', 'POST'])
def emergency():
    if request.method == 'POST':
        units_raw = request.form.get('units_needed', '')
        req = Emergency(
            patient_name=request.form['patient_name'],
            blood_group=request.form['blood_group'],
            units_needed=int(units_raw) if units_raw.isdigit() else 1,
            hospital=request.form['hospital'],
            city=request.form['city'],
            contact_name=request.form['contact_name'],
            contact_phone=request.form['contact_phone'],
            urgency=request.form.get('urgency', 'urgent')
        )
        db.session.add(req)
        db.session.commit()
        flash('Emergency request submitted! We will contact you shortly.', 'success')
        return redirect(url_for('emergency'))
    return render_template('emergency.html')

# ──────────────── ADMIN ROUTES ────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    stats = {
        'total_donors': Donor.query.count(),
        'available_donors': Donor.query.filter_by(is_available=True).count(),
        'total_camps': Camp.query.count(),
        'unread_messages': Contact.query.filter_by(is_read=False).count(),
        'active_emergencies': Emergency.query.filter_by(is_fulfilled=False).count(),
        'fulfilled_emergencies': Emergency.query.filter_by(is_fulfilled=True).count(),
    }
    recent_donors = Donor.query.order_by(Donor.registered_at.desc()).limit(5).all()
    recent_messages = Contact.query.order_by(Contact.sent_at.desc()).limit(5).all()
    active_emergencies = Emergency.query.filter_by(is_fulfilled=False).order_by(Emergency.requested_at.desc()).all()
    return render_template('admin_dashboard.html', stats=stats, recent_donors=recent_donors,
                           recent_messages=recent_messages, active_emergencies=active_emergencies)

@app.route('/admin/donors')
@admin_required
def admin_donors():
    donors = Donor.query.order_by(Donor.registered_at.desc()).all()
    return render_template('admin_donors.html', donors=donors)

@app.route('/admin/donors/toggle/<int:id>')
@admin_required
def toggle_donor(id):
    donor = Donor.query.get_or_404(id)
    donor.is_available = not donor.is_available
    db.session.commit()
    return redirect(url_for('admin_donors'))

@app.route('/admin/donors/delete/<int:id>')
@admin_required
def delete_donor(id):
    donor = Donor.query.get_or_404(id)
    db.session.delete(donor)
    db.session.commit()
    return redirect(url_for('admin_donors'))

@app.route('/admin/messages')
@admin_required
def admin_messages():
    messages = Contact.query.order_by(Contact.sent_at.desc()).all()
    return render_template('admin_messages.html', messages=messages)

@app.route('/admin/messages/read/<int:id>')
@admin_required
def mark_read(id):
    msg = Contact.query.get_or_404(id)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/delete/<int:id>')
@admin_required
def delete_message(id):
    msg = Contact.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for('admin_messages'))

@app.route('/admin/camps', methods=['GET', 'POST'])
@admin_required
def admin_camps():
    if request.method == 'POST':
        camp = Camp(
            name=request.form['name'],
            location=request.form['location'],
            city=request.form['city'],
            date=request.form['date'],
            time=request.form.get('time', ''),
            organizer=request.form.get('organizer', ''),
            contact=request.form.get('contact', '')
        )
        db.session.add(camp)
        db.session.commit()
        flash('Camp added successfully!', 'success')
        return redirect(url_for('admin_camps'))
    camps = Camp.query.order_by(Camp.date.asc()).all()
    return render_template('admin_camps.html', camps=camps)

@app.route('/admin/camps/delete/<int:id>')
@admin_required
def delete_camp(id):
    camp = Camp.query.get_or_404(id)
    db.session.delete(camp)
    db.session.commit()
    return redirect(url_for('admin_camps'))

@app.route('/admin/emergencies')
@admin_required
def admin_emergencies():
    emergencies = Emergency.query.order_by(Emergency.requested_at.desc()).all()
    return render_template('admin_emergencies.html', emergencies=emergencies)

@app.route('/admin/emergencies/fulfill/<int:id>')
@admin_required
def fulfill_emergency(id):
    req = Emergency.query.get_or_404(id)
    req.is_fulfilled = True
    db.session.commit()
    return redirect(url_for('admin_emergencies'))

@app.route('/admin/emergencies/delete/<int:id>')
@admin_required
def delete_emergency(id):
    req = Emergency.query.get_or_404(id)
    db.session.delete(req)
    db.session.commit()
    return redirect(url_for('admin_emergencies'))

# ──────────────── INIT ────────────────

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)