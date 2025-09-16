from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Remove invalid reviewlike rows with non-existent user_id.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('''
                DELETE FROM movies_reviewlike
                WHERE user_id NOT IN (SELECT id FROM auth_user)
            ''')
        self.stdout.write(self.style.SUCCESS('Invalid reviewlike rows removed.'))
