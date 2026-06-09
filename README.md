👗 Fashion Hub Clothing Website

📌 Project Overview

Fashion Hub is a modern and responsive online clothing shopping website developed using Flask, HTML, CSS, Bootstrap, and MySQL.
The project allows users to browse fashion products, add items to cart and wishlist, place orders, and manage products through an admin panel.

The website is designed with a professional UI and includes authentication, product management, search functionality, order management, and image uploads.

---

🚀 Features

👤 User Features

- User Registration & Login
- Secure Password Authentication
- Product Search
- Category Filtering
- Add to Cart
- Wishlist Management
- Product Details Page
- Order Checkout
- Order History
- Responsive Design

---

🛠️ Admin Features

- Admin Dashboard
- Add Products
- Edit Products
- Delete Products
- View Orders
- Manage Website Products

---

💻 Technologies Used

Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

Backend

- Python
- Flask Framework

Database

- MySQL

Tools & Libraries

- Flask-MySQLdb
- Werkzeug
- Bcrypt
- PyMySQL

---

📂 Project Structure

FASHION_HUB/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── uploads/
│       └── product images
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── cart.html
│   ├── wishlist.html
│   ├── orders.html
│   ├── add_product.html
│   ├── edit_product.html
│   ├── product_details.html
│   └── admin.html
│
├── app.py
├── requirements.txt
└── README.md

---

⚙️ Installation Steps

Step 1: Clone Repository

git clone https://github.com/your-username/FASHION_HUB.git

---

Step 2: Open Project Folder

cd FASHION_HUB

---

Step 3: Install Required Libraries

pip install -r requirements.txt

---

Step 4: Setup MySQL Database

Create a database named:

fashionhub

Import required tables into MySQL.

---

Step 5: Run Flask Application

python app.py

---

Step 6: Open Browser

http://127.0.0.1:5000

---

🗄️ Database Tables

Users Table

- id
- name
- email
- password

Products Table

- id
- name
- price
- category
- image
- description

Cart Table

- id
- product_id
- product_name
- price
- image

Orders Table

- id
- customer_name
- email
- address
- phone
- total_price

Wishlist Table

- id
- username
- product_id
- product_name
- price
- image

---

🔐 Security Features

- Password Hashing using Bcrypt
- Secure File Uploads
- Session Management
- Login Authentication
- Protected Routes

---

🎨 UI Features

- Responsive Layout
- Gradient Backgrounds
- Animated Buttons
- Professional Product Cards
- Sidebar Navigation
- Mobile Friendly Design

---

📸 Screenshots

Home Page

- Product listing
- Search bar
- Navigation bar

Product Details Page

- Product information
- Wishlist button
- Add to cart button

Admin Dashboard

- Product count
- User count
- Order count

---

🌟 Future Improvements

- Payment Gateway Integration
- AI Fashion Recommendation System
- Order Tracking
- Email Notifications
- Dark Mode
- Product Reviews & Ratings
- Chatbot Integration

---

📈 Learning Outcomes

This project helped in understanding:

- Flask Backend Development
- MySQL Database Integration
- Authentication Systems
- CRUD Operations
- Responsive UI Design
- File Upload Handling
- Session Management

---

👩‍💻 Author

Name: Villuri Anjali

Project: Fashion Hub Clothing Website

Technology: Flask + MySQL + HTML + CSS

---

📄 License

This project is developed for educational and learning purposes.
