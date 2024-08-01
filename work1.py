from __future__ import print_function
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']
# Initialize Calendar service with valid OAuth credentials
def searchCalList(service):
    # Call the Calendar API
    lottencList = []
    print('Getting list of calendars')
    calendar_list = service.calendarList().list().execute()

    calendars = calendar_list.get('items', [])
	
    if not calendars:
        print('No calendars found.')
    for calendar in calendars:
        print(f"Calendar ID: {calendar['id']}, Summary: {calendar['summary']}")
        if calendar['summary'].find('건설') != -1:
            lottencList.append(calendar['id'])
    
    #print(lottencList)
    return lottencList
    
def callCalendar(service, calendarList):
     # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    
    for id in calendarList:
        events_result = service.events().list(calendarId=id, timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start[:10], event['summary'])
            #print(start[:10], event)
        
        
def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    calendarIdList =[]
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    calendarIdList = searchCalList(service)
    print(calendarIdList)
   
    callCalendar(service, calendarIdList)

if __name__ == '__main__':
    main()