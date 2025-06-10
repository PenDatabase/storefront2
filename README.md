
---

````markdown
# FollowUp Buddy

**FollowUp Buddy** is a Django-based web application that helps users track evangelism efforts and follow-up activities. Built using Django templates (not DRF), it offers a simple, user-friendly interface to stay intentional and accountable in soul-winning.

---

## ✨ Features

- Log and manage evangelism records
- Schedule and monitor follow-up progress
- Beautiful admin interface powered by [Jazzmin](https://github.com/farridav/django-jazzmin)
- Form customization with `django-widget-tweaks`
- Debugging tools with `django-debug-toolbar`
- Preload test data with a single command
- Uses default SQLite database (no external DB setup needed)

---

## 🛠 Requirements

- Python 3.10 or higher
- Django 5.2.1
- All dependencies listed in `requirements.txt`

---

## 📦 Tech Stack

- **Framework**: Django (Template-based)
- **Database**: SQLite (default)
- **UI**: HTML/CSS with Django Templates
- **Admin Dashboard**: Jazzmin

---

## 🧪 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/followup-buddy.git
cd followup-buddy
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin User

To explore the admin panel and play around with the system:

```bash
python manage.py createsuperuser
```

Then visit [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and log in using the credentials you just created.

### 6. Populate the Database with Sample Data

Optionally, seed the database with mock evangelism and follow-up entries:

```bash
python seed.py
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🗂 Project Structure Overview

```
followup_buddy/
├── evangelism/             # Core app logic
├── templates/              # HTML templates
├── static/                 # CSS/JS assets (optional)
├── seed.py                 # Database seeding script
├── db.sqlite3              # Default SQLite database
├── manage.py
└── requirements.txt
```

---

## 🛠 Development Tools

* **django-debug-toolbar** – Inspect queries, cache, and templates
* **django-widget-tweaks** – Easily customize forms in HTML
* **django-jazzmin** – Stylish and modern admin interface

---

## 🙌 Contribution

We welcome contributions and suggestions! Feel free to fork the repository and submit a pull request, or open an issue to propose new features or bug fixes.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ✝️ Inspiration

> *“Go therefore and make disciples of all nations...”* — **Matthew 28:19**

**FollowUp Buddy** helps believers act on the Great Commission with intentionality by tracking outreach and nurturing follow-up.

---