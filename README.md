# Valery's Gallery

Valery's Gallery is a Django-based web application that serves as a personal portfolio for showcasing artwork. It supports image categorization, interactive browsing, and integration with Instagram to automatically update new posts into a dedicated category. The project is designed with a focus on simplicity and usability, making it easy to manage and explore content.

![Project Demo](gallery/static/img/gallery-demo.gif)

## Features

- **Admin-Only Content Management**:
  - Admins can add, edit, or delete categories and images.
  - Images are organized into user-defined categories for easy navigation.
- **Public User Features**:
  - Users can browse images by category.
  - View a dynamic carousel featuring selected images.
- **Instagram Integration**:
  - Automatically syncs new Instagram posts to a "Drawing" category.
  - Includes image URLs, captions, and timestamps for each post.
- **Responsive Design**:
  - Optimized for mobile and desktop devices.
- **Email Notifications**:
  - Secure contact form with email notifications sent to the admin.

---

## Installation

### Requirements

- Python 3.10+
- Django 5.0+
- SQLite (default) or PostgreSQL/MySQL for production
- `python-dotenv` for environment variable management
- Requests library for API communication

---

### Step-by-Step Guide

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-repo/valery-gallery.git
   cd valery-gallery
Install dependencies:

Ensure pip is installed and run:

bash
Skopiuj kod
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root directory and add the following:

bash
Skopiuj kod
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
Apply migrations:

Run the following command to set up the database:

bash
Skopiuj kod
python manage.py migrate
Create a superuser:

To access the admin panel, create a superuser account:

bash
Skopiuj kod
python manage.py createsuperuser
Run the development server:

Start the Django development server:

bash
Skopiuj kod
python manage.py runserver
Access the application:

Main page: http://127.0.0.1:8000/
Admin panel: http://127.0.0.1:8000/admin/
Instagram Integration
Set Up Instagram API:

Ensure your Instagram account is a Business or Creator account.
Link your Instagram account to a Facebook Page.
Use the Instagram Graph API to generate an access token.
Sync Instagram Posts:

A scheduled script fetches Instagram posts and saves them to the "Drawing" category.

Example script (fetch_instagram_posts.py):

python
Skopiuj kod
import requests
from gallery.models import InstagramPost, Category

def fetch_instagram_posts():
    token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token={token}"
    response = requests.get(url).json()

    drawing_category, _ = Category.objects.get_or_create(title="Drawing")

    for post in response.get('data', []):
        if post['media_type'] == 'IMAGE':
            InstagramPost.objects.get_or_create(
                image_url=post['media_url'],
                caption=post.get('caption', ''),
                created_at=post['timestamp'],
                category=drawing_category
            )
Schedule this script using a cron job or a task queue like Celery.

Project Structure
plaintext
Skopiuj kod
valery-gallery/
│
├── base/
│   ├── __init__.py
│   ├── settings.py       # Configuration settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py           # WSGI configuration
│
├── gallery/
│   ├── __init__.py
│   ├── apps.py           # App configuration
│   ├── models.py         # Database models (Image, Category, InstagramPost)
│   ├── views.py          # Views for handling requests
│   ├── urls.py           # URL routing for the app
│   ├── templates/        # HTML templates
│
├── static/               # Static files (CSS, JavaScript, Images)
├── media/                # Uploaded media files
├── db.sqlite3            # SQLite database (development use)
├── .env                  # Environment variables
└── manage.py             # Django management script
License
This project is licensed under the MIT License.

Developed by Valery.

Skopiuj kod





