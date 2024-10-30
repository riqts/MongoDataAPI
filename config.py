from decouple import config

ENVIRONMENT = config('APP_ENV', default='development')
MONGODB_URI = config('MONGODB_URI', default='mongodb://localhost:27017')
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')
TEST = config('TEST', default='0')