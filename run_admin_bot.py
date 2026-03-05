import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cefr_bot.settings')
django.setup()

from admin_bot import main

if __name__ == "__main__":
    main()
