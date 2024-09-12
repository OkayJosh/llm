"""
Run Custom query Against the db
#TODO: find ways to make this safer:: Running sql like this might pose risk
"""
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Execute a SQL command to check database connectivity and print results'

    def add_arguments(self, parser):
        parser.add_argument('sql', type=str, help='SQL command to execute')

    def handle(self, *args, **kwargs):
        sql_command = kwargs['sql']
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_command)
                results = cursor.fetchall()  # Fetch all results
                if results:
                    for row in results:
                        self.stdout.write(self.style.SUCCESS(f'Result: {row}'))
                else:
                    self.stdout.write(self.style.SUCCESS('No results returned.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error executing SQL command: {e}'))
            exit(1)
