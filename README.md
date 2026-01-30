# Golden Spoon Restaurant Website

A Django-based restaurant website with online ordering, reservations, and admin management features.

## Features

- 🍽️ Menu browsing and item details
- 🛒 Shopping cart and checkout system
- 📅 Table reservations
- 👤 User authentication and profiles
- 📊 Admin dashboard for orders and reservations
- 📱 Responsive design

## Tech Stack

- **Backend**: Django 6.0.1
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Vercel

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/spoongolden589-web/GOLDEN-SPOON-RESTAURANT.git
cd GOLDEN-SPOON-RESTAURANT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
```sql
CREATE DATABASE restaurant_db;
```

4. Update database credentials in `restaurant_core/settings.py`

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Deployment on Vercel

### Prerequisites
- GitHub account with this repository
- Vercel account
- MySQL database (e.g., PlanetScale, Railway, or any cloud MySQL)

### Important Notes for Vercel Deployment

⚠️ **Database Limitation**: Vercel doesn't support SQLite or local MySQL. You need to use:
- **PlanetScale** (MySQL compatible, free tier available)
- **Railway** (PostgreSQL, free tier)
- **AWS RDS** or any cloud database

⚠️ **Media Files**: User-uploaded images won't persist on Vercel. For production, use:
- AWS S3
- Cloudinary
- Vercel Blob Storage

### Deployment Steps

1. **Set up a cloud database** (e.g., PlanetScale):
   - Create free account at planetscale.com
   - Create a database
   - Get connection details

2. **Update settings for production**:
   - Create environment variables on Vercel:
     - `DATABASE_URL` or individual DB credentials
     - `SECRET_KEY`
     - `DEBUG=False`

3. **Deploy to Vercel**:

   **Option A: Via Vercel CLI**
   ```bash
   npm i -g vercel
   vercel login
   vercel
   ```

   **Option B: Via Vercel Dashboard**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Configure environment variables
   - Deploy

4. **Add environment variables in Vercel**:
   ```
   DATABASE_NAME=your_db_name
   DATABASE_USER=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOST=your_db_host
   DATABASE_PORT=3306
   SECRET_KEY=your-secret-key
   DEBUG=False
   ```

5. **Update `settings.py` to use environment variables**:
   ```python
   import os
   
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': os.environ.get('DATABASE_NAME'),
           'USER': os.environ.get('DATABASE_USER'),
           'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
           'HOST': os.environ.get('DATABASE_HOST'),
           'PORT': os.environ.get('DATABASE_PORT', '3306'),
       }
   }
   ```

### Alternative: Better Hosting Options for Django

Consider these platforms for easier Django deployment:
- **Railway.app** - Best for Django, includes PostgreSQL
- **Render.com** - Easy Django deployment with database
- **PythonAnywhere** - Django-specific hosting
- **Heroku** - Classic PaaS for Django

## Project Structure

```
├── main/                   # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── restaurant_core/        # Project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # User uploads
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Admin Access

Access the admin panel at `/admin/` with superuser credentials.

## Contact

For questions or support, contact: spoongolden589@gmail.com

## License

All rights reserved.
