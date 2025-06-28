import datetime
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from service account file
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Place your JSON key here

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)
CALENDAR_ID = 'primary'  # or your specific calendar ID

def add_event_to_calendar(summary, date):
    event_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    event = {
        'summary': summary,
        'start': {
            'dateTime': event_date.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (event_date + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }
    event_result = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"Event created: {event_result.get('htmlLink')}"