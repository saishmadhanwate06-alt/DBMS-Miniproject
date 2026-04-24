🍱 Food Waste Management System
A web-based application built using Flask (Python) and MySQL to reduce food waste by connecting food donors (like hotels) with NGOs/users who can collect and utilize excess food.

🚀 Features
Admin
Admin login
Add multiple food donations
Update / Delete food items
Approve user requests
View all requests

👤 User (NGO)
User registration & login
View available food
Request food
Mark "I am Coming"
Mark food as Collected
View own requests

🛠️ Tech Stack
Frontend: HTML, CSS, Bootstrap
Backend: Flask (Python)
Database: MySQL

📁 Project Structure
Food-Waste-System/
│
├── app.py
├── db_config.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── admin_login.html
│   ├── add_food.html
│   ├── update_food.html
│   ├── view_food.html
│   ├── view_requests.html
│   └── request.html
│
├── static/
│   └── (CSS / Images / Logo)
│
└── README.md

⚙️ Installation & Setup
1️⃣ Clone Repository
git clone https://github.com/Sakshig131/food-waste-system.git
cd food-waste-system

2️⃣ Install Dependencies
pip install flask mysql-connector-python

3️⃣ Setup Database
Create MySQL database:

CREATE DATABASE food_waste;
4️⃣ Create Tables
USERS TABLE
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(10)
);
DONATIONS TABLE
CREATE TABLE donations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(100),
    quantity INT,
    location VARCHAR(100),
    contact VARCHAR(15),
    status VARCHAR(20),
    expiry_date DATE
);
REQUESTS TABLE
CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    donation_id INT,
    requester_name VARCHAR(50),
    status VARCHAR(20),
    arrival_status VARCHAR(20)
);

5️⃣ Configure Database
Open db_config.py and update:

host="localhost",
user="root",
password="your_password",
database="food_waste"

6️⃣ Run Application
python app.py
Open in browser:
http://127.0.0.1:5000

🔐 Default Roles
Admin: manually insert in DB with role = 'admin'
User: register via UI

📊 System Flow
Admin adds food
User views food
User sends request
Admin approves request
User clicks "I am Coming"
User collects food
Status updates

🎯 Future Enhancements
Email/SMS notification
Location-based filtering
Image upload for food
Mobile app integration

👩‍💻 Author
Saishma Dhanwate
