# 💧 LifeDrop — Blood Donation Website

A full-stack blood donation platform built with **Python Flask + SQLite**.

---

## 📁 Project Structure

```
lifedrop/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── static/
│   ├── style.css           # Public website styles
│   ├── admin.css           # Admin panel styles
│   └── main.js             # JavaScript (counters, reveal, hamburger)
└── templates/
    ├── base.html           # Shared navbar + footer
    ├── index.html          # Homepage
    ├── about.html          # About page
    ├── register.html       # Donor registration
    ├── find_donor.html     # Search donors + blood camps
    ├── contact.html        # Contact form
    ├── emergency.html      # Emergency blood request
    ├── admin_login.html    # Admin login screen
    ├── admin_base.html     # Admin sidebar layout
    ├── admin_dashboard.html
    ├── admin_donors.html
    ├── admin_messages.html
    ├── admin_camps.html
    └── admin_emergencies.html
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
- Website: http://localhost:5000
- Admin Panel: http://localhost:5000/admin

---

Admin credentials are set via environment variables (ADMIN_USERNAME, ADMIN_PASSWORD) — not hardcoded.

---

## 🛠 Features

### Public Pages
- **Home** — Hero, stats counter, blood group search, upcoming camps, active emergencies
- **About** — Mission, values, eligibility, team
- **Register** — Donor registration form with eligibility sidebar
- **Find Donor** — Search by blood group + city, blood camp table, compatibility chart
- **Contact** — Contact form, office info
- **Emergency** — Emergency blood request form, 24/7 helpline, compatibility reference

### Admin Panel (Password Protected)
- **Dashboard** — Stats cards, active emergencies, recent donors & messages
- **Donors** — View all, enable/disable, delete
- **Messages** — View all, mark read, delete
- **Blood Camps** — Add new camps, delete existing
- **Emergencies** — Mark fulfilled, delete requests

---

## 🎨 Design

- **Colors:** Pinkish-white (#fff5f5) + Bold red (#e53935)
- **Fonts:** Playfair Display (headings) + DM Sans (body)
- **Admin Theme:** Dark sidebar (#0f0f1a) + light content area
- **Responsive:** Mobile-friendly with hamburger menu

---

## 📦 Tech Stack

| Layer    | Tech                  |
|----------|-----------------------|
| Backend  | Python Flask          |
| Database | SQLite (via SQLAlchemy)|
| Frontend | HTML + CSS + JS       |
| Fonts    | Google Fonts          |
| Auth     | Flask session         |
