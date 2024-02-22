import os
import pickle
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, HttpResponse
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from .forms import AppointmentBookingForm
from account.models import User
from .models import Appointment
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_calendar(user):
    flow = InstalledAppFlow.from_client_secrets_file(settings.GOOGLE_API_CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=3000)
    # Storing token in session
    user.google_calendar_token = credentials.to_json()
    user.save()
    return credentials

def calculate_end_time(start_time):
    start_datetime = datetime.combine(datetime.today(), start_time)
    duration = timedelta(minutes=45)
    end_datetime = start_datetime + duration
    end_time = end_datetime.time()
    return end_time


@login_required
def confirmation_page(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.end_time = calculate_end_time(appointment.start_time)
        return render(request, 'confirmation.html', {'appointment': appointment})
    except Appointment.DoesNotExist:
        return HttpResponse("Appointment not found")
    except Exception as e:
        print("Error in confirmation_page:", e)
        return HttpResponse("An error occurred")


@login_required()
def list_view(request):
    users_with_calendar = User.objects.exclude(google_calendar_credentials_path='')
    return render(request, 'doctor_list.html', {'users': users_with_calendar})




def add_event_to_calendar(event, credentials):
    service = build('calendar', 'v3', credentials=credentials)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

    return True


def load_google_calendar_credentials(credentials_path):
    with open(credentials_path, 'rb') as token:
        credentials = pickle.load(token)
        print(credentials)
    return credentials

@login_required()
def book_appointment(request):
    doctor_id = request.GET.get('doctor_id')
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            # Set the doctor_id before saving the form
            form.instance.doctor_id = doctor_id
            appointment = form.save()

            # Load credentials and add event to doctor's calendar
            credentials_path = os.path.join(settings.STATIC_ROOT, f"{appointment.doctor.username}_google_calendar_credentials.pkl")
            credentials = load_google_calendar_credentials(credentials_path)
            # Calculate end time
            start_time = form.cleaned_data.get('start_time')
            duration = timedelta(minutes=45)
            end_time = (datetime.combine(datetime(1, 1, 1), start_time) + duration).time()


            event = {
                'summary': f'Appointment with {request.user.first_name} {request.user.last_name}',
                'location': 'Online',
                'description': f'Appointment regarding {appointment.specialty}',
                'start': {
                    'dateTime': f"{appointment.date.strftime('%Y-%m-%d')}T{start_time.strftime('%H:%M:%S')}-07:00",
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': f"{appointment.date.strftime('%Y-%m-%d')}T{end_time.strftime('%H:%M:%S')}-07:00",
                    'timeZone': 'Asia/Kolkata',
                },
                'attendees': [
                    {'email': f'{request.user.email}'},
                    {'email': 'sbrin@example.com'},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            print(event)
            if add_event_to_calendar(event, credentials):
                # Redirect to a success page or home page
                return render(request, 'confirmation.html', {'appointment': appointment,
                                                             'end_time': end_time})  # Change 'home' to the appropriate URL name
    else:
        # Pass the doctor_id as an initial value to the form
        form = AppointmentBookingForm(initial={'doctor': doctor_id})
    return render(request, 'appointment_form.html', {'form': form})