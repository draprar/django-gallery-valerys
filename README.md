# 🎨 Valery's Gallery — Django App (Archived)

A Django-powered portfolio app for showcasing artwork online.
Organize images into categories, sync Instagram posts automatically, browse in style, and let visitors reach out via contact form. Clean, responsive, and easy to manage.

> ⚠️ This repository is archived.  
> This project has been integrated into my main portfolio:
> https://github.com/draprar/django_portfolio-walery (see `/gallery` app)

![Project Demo](gallery/ss.png)

## 📖 Overview
This project is a Django-based gallery app created for showcasing artwork and visual content in a structured, responsive layout.

It started as a standalone application and was later integrated into a larger modular portfolio system.

## 🧠 Project Evolution
- Standalone Django gallery application
- Integrated into the main portfolio project
- Archived as a separate repository for historical reference
  
## ✨ Features

- **Image Gallery**
  - Organize images into categories
  - Display images with descriptions and modal views

- **Instagram Integration**
  - Embed Instagram posts into the gallery based on categories

- **Admin Features**
  - Upload and delete images
  - Create and manage categories

- **Contact Form**
  - Allows users to send messages
  - Sends email notifications for new messages

- **Responsive Design**
  - Optimized for desktop and mobile views

## 🚀 Installation

### Requirements

- Python 3.10+
- Django 5.0+
- SQLite (default) or PostgreSQL/MySQL for production
- `python-dotenv` for environment variable management
- Requests library for API communication

### Step-by-Step Guide

1. **Clone the repository**:

Via:
   ```
   git clone https://github.com/draprar/django-gallery-valerys.git
   cd valery-gallery
   ```
   
3. **Install dependencies**:

Ensure pip is installed and run:

   ```
    pip install -r requirements.txt
   ```

3. **Set up environment variables**:

Create a .env file in the project root directory and add the following:

   ```
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    EMAIL_HOST=smtp.your-email-provider.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-email-password
    DEFAULT_FROM_EMAIL=your-email@example.com
    INSTAGRAM_ACCESS_TOKEN=your-instagram-access-token
   ```

4. **Make migrations**:

Run the following commands to set up the database:
   ```
   python manage.py makemigrations
   ```
   ```
   python manage.py migrate
   ```

5. **Create a superuser**:

Via:
   ```
   python manage.py createsuperuser
   ```

6. **Run the development server**:

Start the Django development server:

   ```
    python manage.py runserver
   ```

7. **Access the application**:

- Main page: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📌 Notes

- This project is no longer maintained as a standalone repository
- The gallery functionality now lives inside the main portfolio project
- This repo remains as an archived reference for the standalone version

## 📜 License

This project is licensed under the MIT License.

## 👤 Author
Developed by Walery ([@draprar](https://github.com/draprar/)).
