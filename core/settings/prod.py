from .base import *
DEBUG = False

ALLOWED_HOSTS = ['django-booking.onrender.com']

DATABASES = {
 'default': {
   'ENGINE': 'django.db.backends.postgresql',
   'NAME': os.getenv('POSTGRES_DB'),
   'USER': os.getenv('POSTGRES_USER'),
   'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
   'HOST': os.getenv('POSTGRES_HOST'),
   'PORT': os.getenv('POSTGRES_DB_PORT', 5432),
   'OPTIONS': {'sslmode': 'require'},
 }
}
print('DEBUG ENV VALUES:')
print('DB:', os.getenv('POSTGRES_DB'))
print('USER:', os.getenv('POSTGRES_USER'))
print('HOST:', os.getenv('POSTGRES_HOST'))
print('SETTINGS:', os.getenv('DJANGO_SETTINGS_MODULE'))