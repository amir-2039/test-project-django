from django.db import models


class Consumer(models.Model):
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    previous_jobs_count = models.IntegerField(default=0)
    amount_due = models.DecimalField(max_digits=9, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
