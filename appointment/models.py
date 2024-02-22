from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime, timedelta


class Appointment(models.Model):
    specialty = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    doctor = models.ForeignKey('account.User', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        duration = timedelta(minutes=45)
        self.end_time = (datetime.combine(datetime(1, 1, 1), self.start_time) + duration).time()
        super().save(*args, **kwargs)

    def clean(self):
        if self.start_time:
            if self.start_time.hour < 8 or self.start_time.hour >= 18:
                raise ValidationError("Appointment time must be between 8:00 AM and 6:00 PM.")


admin.site.register(Appointment)
