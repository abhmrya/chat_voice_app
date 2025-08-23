# Django Chat & Voice App - Setup and Workflow Guide

This guide explains how to set up and work with a Django-based chat and voice messaging application using Channels, JWT authentication, Google login, MySQL, Tailwind CSS, and WebSockets.

---
## 📂 Project Structure
```
channel_layers_project/
├─ manage.py
├─ django_chat_voice/ # Project Core
│ ├─ asgi.py
│ ├─ settings.py
│ ├─ urls.py
│ └─ wsgi.py
├─ channel_layers_app/ # Main App
│ ├─ consumers.py
│ ├─ models.py
│ ├─ routing.py
│ ├─ serializers.py
│ ├─ signals.py
│ ├─ templates/
│ │ ├─ base.html
│ │ ├─ index.html
│ │ ├─ group_chat.html
│ │ ├─ one_to_one.html
│ │ ├─ login.html
│ │ ├─ register.html
│ │ └─ token_landing.html
│ ├─ urls.py
│ └─ views.py
├─ static/
└─ media/
```

---

## ⚙️ Step 1: Install Django
- Install Django using pip in a virtual environment.
- Start a new Django project.

---
```
pip install django
```

## ⚙️ Step 2: Create Chat App
- Create an app named **`channel_layers_app`**.
- This app manages chat, group, and one-to-one messaging.

---
```
django-admin startproject channel_layers_project
```

## 🎨 Step 3: Setup Tailwind CSS
- Install and configure Tailwind for styling templates.
- Run Tailwind watcher for live CSS updates.
---

you instal here  [django tailwind ](https://django-tailwind.readthedocs.io/en/latest/installation.html)

```
INSTALLED_APPS=[
        'tailwind',
        'theme',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

TAILWIND_APP_NAME = 'theme'

NPM_BIN_PATH

MIDDLEWARE = [  'social_django.middleware.SocialAuthExceptionMiddleware',
]

LOGIN_URL = '/base/'

# LOGIN_REDIRECT_URL = '/base/'
LOGOUT_REDIRECT_URL = '/login/'

```

## 🔑 Step 4: Google Console Keys
- Create a Google Cloud Console project.
- Enable OAuth2 and generate **Client ID** and **Secret Key**.
- These keys are used for Google login.
---
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ="xxxxxxxxxx.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

```
## 🔐 Step 5: Google Login (Social Authentication)
- Configure Django Social Auth with Google OAuth2.
- Setup login, redirect, and logout URLs.
---
```
LOGIN_URL = '/base/'
LOGOUT_REDIRECT_URL = '/login/'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/get-jwt-token-after-google-login/'
SOCIAL_AUTH_URL_NAMESPACE = "social"

```

## 🛠️ Step 6: Install Django REST Framework
- Install **DRF** for building API endpoints (login, registration, chat, audio).

---
```
    'rest_framework',
```

you install here  [django rest framwork  ](https://www.django-rest-framework.org/)

## 🔑 Step 7: JWT Authentication
- Setup **JWT** authentication with DRF SimpleJWT.
- Tokens issued after login or Google login.

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

```
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
}
```
you install here  [django rest framwork  ](https://www.django-rest-framework.org/)
---

## 🗄️ Step 8: MySQL Database Connection
- Connect Django to a MySQL database.
- Add database credentials in settings.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': '********',
        'USER': 'root',
        'PASSWORD': '*****',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
---

## 🔄 Step 9: Google Login → JWT Flow
- On Google login, user is redirected.
- Backend issues a JWT token.
- Token sent to frontend for secure requests.

---

## 🎨 Step 10: Tailwind Development
- Run Tailwind CLI/watch mode for styling updates.

```
python manage.py tailwind start
```
---

## 🚀 Step 11: Cache Server (Redis)
- Install and start Redis server.
- Redis handles WebSocket connections for Django Channels.
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
```
```
redis server start
```
you install here  [redis](https://redis.io/)

---

## 🖥️ Step 12: Run Django Server
- Start Django development server using `python manage.py runserver`.
```
python manage.py runserver
```
---

## 📝 Step 13: First URL → Register Page
- First page shown: **Register form**.
- Registration API saves user in DB.

---
Gmail setup

```

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT =587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

```
---
## 🔑 Step 14: Login & JWT Tokens
- Login issues JWT token stored on frontend.
```
On login/logout, Gmail notification sent via Django signals.

```
---

## 🏠 Step 15: Base Template (Index)
- After login, users are redirected to **index page** showing:
  - Groups
  - One-to-one chats
  - Online users

---

## 📦 Step 16: Models Overview
- **Group** → Group names.  
- **ChatMessage** → User, group, message, timestamp, audio.  
- **OneToOneMessage** → Sender, receiver, message, time.  
- **UserProfile** → User, online/offline status, profile info.

---

## 🗂️ Step 17: Index Page Rendering
- Index shows all groups & one-to-one chats.
- If no group exists → create new one.

---

## 💬 Step 18: Group Chat Workflow
- Group chat via URL `/index/<group_name>/`.
- WebSocket connection: `/ws/ac/<group_name>/`.

---

## 🗄️ Step 19: Chat Storage
- All chat messages stored in DB.
- Previous messages displayed when joining.

---

## 🎤 Step 20: Audio Recording & Upload
- User records audio in browser.
- Audio sent to API → saved in DB.
- WebSocket shares audio link with group.

---

## 💌 Step 21: One-to-One Messaging
- Users can select a contact for private chat.
- Real-time messages if online, stored if offline.

---

## 👤 Step 22: Online/Offline Tracking
- Django signals + WebSocket consumers track status.
- Online/offline displayed in profile.

---

## 🖼️ Step 23: Profile & Messaging
- Each user has profile (avatar, status).
- Messages handled differently if recipient is online/offline.

---

# ✅ Final Workflow

1. User registers or logs in (JWT/Google).  
2. JWT token issued → used in frontend.  
3. Redirect to index page.  
4. User can:  
   - Join/create group chat  
   - Send text/audio messages  
   - Start private chat  
   - View online users  
5. All messages stored in DB.  
6. Real-time updates via WebSockets.  
7. Audio saved in media and shared via chat.  

---
This completes the **systematic setup and workflow documentation** for the Django Chat & Voice App.
"""