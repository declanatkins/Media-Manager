import os
SECRET_KEY = os.getenv('SECRET') or 'secret'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024