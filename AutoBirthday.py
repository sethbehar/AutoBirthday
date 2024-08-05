import os.path
from datetime import datetime, timedelta, timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Path to the birthdays file
BIRTHDAYS_FILE = 'birthdays.txt'

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def read_birthdays(file_path):
    birthdays = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    name, date_str = line.split(': ')
                    date_obj = datetime.strptime(date_str, '%m/%d').replace(year=datetime.now().year)
                    birthdays.append((name, date_obj))
                except ValueError as e:
                    print(f"Skipping line due to error: {line} - {e}")
    return birthdays

def get_todays_birthdays(birthdays):
    today = datetime.now().date()
    todays_birthdays = [name for name, date_obj in birthdays if date_obj.date() == today]
    return todays_birthdays

def get_tomorrows_birthdays(birthdays):
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    tomorrows_birthdays = [name for name, date_obj in birthdays if date_obj.date() == tomorrow]
    return tomorrows_birthdays

def create_message(sender, to, subject, body):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def email_birthdays(service):
    birthdays = read_birthdays(BIRTHDAYS_FILE)
    todays_birthdays = get_todays_birthdays(birthdays)
    tomorrows_birthdays = get_tomorrows_birthdays(birthdays)
    
    subject = "Today's and Tomorrow's Birthdays"

    if todays_birthdays:
        body = "Here are the birthdays for today:\n\n" + "\n".join(todays_birthdays)
    else:
        body = "There are no birthdays today\n\n" 
    
    if tomorrows_birthdays:
        body += "\n\nHere are the birthdays for tomorrow:\n\n" + "\n".join(tomorrows_birthdays)
    else:
        body += "There are no birthdays tomorrow\n\n" 
    
    message = create_message('me', 'your_email@gmail.com', subject, body)
    send_message(service, 'me', message)

def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    email_birthdays(service)

if __name__ == '__main__':
    main()
