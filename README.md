# 🐾 PetPal – Web Platform for Pet Care & Adoption  

Welcome to **PetPal**, a feature-rich web application designed for pet lovers.  
This project provides a complete digital solution for pet adoption, veterinary booking, online shopping, and community interaction.  
Built using **Django and MySQL**, with a responsive UI powered by **HTML, CSS, and Bootstrap**, PetPal is an ideal platform for modern pet care and adoption needs.  

---

## 🔍 Project Overview  

PetPal enables users to:  

- Browse and search pets for adoption  
- Submit and track adoption requests  
- Book veterinary appointments online  
- Shop pet supplies through the integrated pet store  
- Register and manage user accounts securely  
- Post and interact with the community (stories, tips, events)  
- Receive updates and notifications  
- Access from any device with a mobile-friendly UI  

---

## 🚀 Key Features  

### 🔐 User Authentication  
- Sign up, log in, and log out  
- Secure session handling  
- Role-based access for users and admins  

### 🐶 Pet Management & Adoption  
- Add, edit, and view pet profiles  
- Submit adoption requests  
- Admin approval/rejection of adoption  

### 🩺 Veterinary Appointment System  
- Book vet appointments  
- Manage and track bookings  
- Admin scheduling for doctors  

### 🛒 Pet Store Module  
- Browse products (Food, Toys, Accessories)  
- Add/remove products to cart  
- Place secure orders (Cash on Delivery / UPI)  
- Track past orders  

### 🔔 Notifications & Messaging  
- Get alerts for adoption, bookings, and orders  
- Integrated free APIs for messaging/email  

### 📊 Admin Dashboard  
- Manage users, pets, adoption requests, and orders  
- Monitor community posts and events  
- Generate reports and analytics  

---

## 🛠️ Tech Stack  

| Layer        | Technology           |  
|--------------|----------------------|  
| Backend      | Django (Python)      |  
| Database     | MySQL                |  
| Frontend     | HTML5, CSS3, Bootstrap |  
| Templating   | Django Templates (Jinja2) |  
| Version Control | Git, GitHub       |  

---

## ⚙️ How to Run Locally  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/petpal.git
cd petpal

---

2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up MySQL database

Create a new MySQL database (e.g., petpal_db)

Update database settings in settings.py

5️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Create superuser (Admin)
python manage.py createsuperuser

7️⃣ Start development server
python manage.py runserver


Open in browser 👉 http://localhost:8000

📁 Folder Structure
PetPal/
│
├── petpal/                 # Project settings & configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── pets/                   # Pet Management Module
├── adoption/               # Adoption Module
├── appointments/           # Vet Booking Module
├── store/                  # Pet Store Module
├── community/              # Community & Posts Module
├── accounts/               # User & Admin Management
│
├── templates/              # Global HTML templates
├── static/                 # Global static files (CSS, JS, images)
│
├── manage.py
├── db.sqlite3 (or MySQL DB connection)
├── README.md
└── requirements.txt


👨‍💻 Author

Raghul K – MSc Information Technology Student, Annamalai University
