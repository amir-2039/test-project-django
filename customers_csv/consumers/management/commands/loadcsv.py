import csv

from consumers.models import Consumer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open('consumers.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Consumer.objects.create(
                    id=row['id'],
                    street=row['street'],
                    status=row['status'],
                    previous_jobs_count=row['previous_jobs_count'],
                    amount_due=row['amount_due'],
                    latitude=row['lat'],
                    longitude=row['lng']
                )
