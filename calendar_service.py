import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials_file = 'calendar_credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=['https://www.googleapis.com/auth/calendar']
)
service = build('calendar', 'v3', credentials=credentials)

event = {
    'summary': 'Örnek Etkinlik',
    'location': 'Etkinlik Yeri',
    'description': 'Bu bir örnek etkinliktir.',
    'start': {
        'dateTime': '2023-12-31T10:00:00',
        'timeZone': 'UTC',
    },
    'end': {
        'dateTime': '2023-12-31T12:00:00',
        'timeZone': 'UTC',
    },
}

event = service.events().insert(calendarId='primary', body=event).execute()
print('Etkinlik oluşturuldu: %s' % (event.get('htmlLink')))
