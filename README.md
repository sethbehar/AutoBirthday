# AutoBirthday Reminder

This script automatically sends an email with the birthdays of your friends and family for today and tomorrow. It uses the Gmail API to send the emails.

## Sample email that I have configured to send everyday

![ex](https://github.com/user-attachments/assets/cd83c793-2afd-4f77-b739-baa8bf340369)

## Features

- Reads birthdays from a file (`birthdays.txt`).
- Sends an email with today's and tomorrow's birthdays.
- Uses the Gmail API to send emails securely.

## Prerequisites

- Python 3.6 or later.
- A Gmail account.
- OAuth 2.0 credentials from the Google Cloud Console.

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/AutoBirthday.git
cd AutoBirthday
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set Up Google Gmail API
Follow the instructions to set up the Gmail API and obtain your credentials.json file 

### 4. Prepare 'birthdays.txt'
Create a birthdays.txt following the format of 'birthdayexample.txt'

### 5. Next steps
Schedule the script to run daily using task scheduler for Windows or 'cron' for macOS/Linux

