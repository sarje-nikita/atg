from django import forms
from django.utils import timezone
from .models import Appointment

class AppointmentBookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Appointment
        fields = ['specialty', 'date', 'start_time']

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')

        if date is None:
            raise forms.ValidationError("Date field is required.")

        if start_time is None:
            raise forms.ValidationError("Start time field is required.")

        # Combine date and time into a single datetime object
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(date, start_time)
        )

        # Validate the appointment datetime
        if start_datetime <= timezone.now():
            raise forms.ValidationError("Appointment datetime must be in the future.")

        # Check if there are any appointments within 45 minutes before or after the proposed start time
        min_start_time = start_datetime - timezone.timedelta(minutes=45)
        max_start_time = start_datetime + timezone.timedelta(minutes=45)
        conflicting_appointments = Appointment.objects.filter(
            date=date,
            start_time__range=(min_start_time.time(), max_start_time.time())
        )

        if conflicting_appointments.exists():
            # Generate a list of suggested available times
            available_times = []
            current_time = min_start_time
            while current_time <= max_start_time:
                if not Appointment.objects.filter(date=date, start_time=current_time.time()).exists():
                    available_times.append(current_time.strftime("%H:%M"))
                current_time += timezone.timedelta(minutes=15)  # Adjust the interval as needed

            raise forms.ValidationError(f"There is a conflicting appointment within 45 minutes of this time. "
                                          f"You may consider the following available times: {', '.join(available_times)}")

        # Set the combined datetime field
        cleaned_data['start_datetime'] = start_datetime

        return cleaned_data
