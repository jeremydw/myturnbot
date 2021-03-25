#!/usr/bin/python3
import requests
import time, schedule
import smtplib, ssl
import pync
from datetime import datetime, timedelta, date
from getpass import getpass

url = "https://api.myturn.ca.gov/public/locations/a2ut0000006eUhiAAE/availability"

payload = {
    'vaccineData': 'WyJhM3F0MDAwMDAwMDFBZExBQVUiXQ==',
    'doseNumber': 1,
    'url': 'https://myturn.ca.gov/appointment-select'
}

headers = {
  'Content-Type': 'application/json',
  'Cookie': 'ak_bmsc=ABCCA0D94E1D434C5C91DE8CCBCB6AB0B81CDBDE176B000032104B60AD8BE900~plQR29tOQ/HcPPmAQ1XjLuPmzL6vij7jQiDx6NSTEZuUmYBkrw67NhmctYPlqNX4iBtDe35eBWuQ8PlffOb8pBCYp7OaP+U5buZN7OkInSekN5+DAtR/ULdXA+SPyjnQMmkO6JV0rNDSzKhHKMEumNFOQvLzbqjhBL1Ci7/tV0kvuh8yJx3TEz0GWD2MD9mr4C7zoNphesWv6SlamQzLyvhCmuhqhLVPTmBqhrDzkisdw=; bm_sz=CAE44E75F08380FDBF010A699FFA6049~YAAQ3tscuCxZHhN4AQAAgUY3JQttf0KJ+/MJsTgZTXUSygSAGM4IdxW6kVOce2vZhYuTP8SWFeyxqM8OyzT0GOzGhvcg+fCX4WP877FxhheHfc03mJsfKMLatQmLGTYrcfAdsosdrLVWLMXdB8j4Lc2mwfRSoZMEZNjPBKY8QL27jeNn68qk1VuBfH8=; _abck=4C820600C383E54905DA497D3AB1E339~-1~YAAQ3tscuC1ZHhN4AQAAgUY3JQWjD0Z5IbC1kufJdinq1C/PIiTPhlzMiS80stkQSLOHf39ZbrnRt5D9m5OExAr+XJKrR799CmLS3d26EF7KDEfZ3IpQ+2WlGpMXDjwNbOI1VpZOTM0BtLEjKaGKZ/lGrZErDacBHmonPNwXf9p7smJxihkPxyKDrzSvTks7zel8qMWmdbTHhIgZpsnTUr+269xLhI3xkV7ZuUFKMFGkoEkerWxGkUwHYpHPR8oiwfkep32W4TorIkJZdisbFAUddg4Ywr174ML3cgxYnf5xpaRTx/Id8K7s+5NimpCOKHBrgBP+hwf/qkwiTrHu8Rvfra6kAwf27ZVcZh92ACD8iiGHMw==~-1~-1~-1; bm_sv=10E30DF0EAFC7FC159560B8F1E882EA4~dze7LjZ4upxPiqJlO8Oszkl7DloCfIM9fOnLCbldBd0aXwPdaDu43rpsiRob2f+X2erMd7HGFbTIdEf2obGtU/1CXvj/3nl09lXgtiahucXyKDGa0SNHBv74V+vAhtnWY/v2mLBSUQNuzerEXs0hiZ7YTI6y+nGR+W5gWGpUB2o='
}

port = 465
smtp_server = "smtp.gmail.com"
message = "Subject: Moscone Center Appointment Found for "
context = ssl.create_default_context()

#initialize to yesterday
last_sent = datetime.now() - timedelta(1)

def input_password(username):
    password_1 = getpass('Enter the sender\'s gmail password:')
    password_2 = getpass('Confirm the gmail password:')
    if password_1 == password_2:
        try:
            check_password(username, password_1)
            print('Login was successful')
            return password_1
        except:
            print('Login failed. If you are sure the username and passwords are correct, \
you probably didn\'t enable "Less secure app access". To do so, go to \
http://myaccount.google.com/u/5/lesssecureapps')
    else:
        print('Passwords do not match')
    input_password(username)

def check_password(username, password):
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.quit()

def send_email(appt_date):
    global last_sent
    global message
    if (datetime.now() - last_sent).total_seconds() / 60 < 5:
        print('Suppressing the email; the last one was sent within 5 minutes')
        return

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message + appt_date)
        last_sent = datetime.now()

def job():
    today = date.today()

    payload['startDate'] = today.strftime('%Y-%m-%d')
    payload['endDate'] = (today + timedelta(days=30)).strftime('%Y-%m-%d')

    response = requests.request("POST", url, headers=headers, json = payload)

    for date_obj in response.json()['availability']:
        if date_obj['available']:
            print('FOUND ONE!!!!!!!!!!!!!!! ' + date_obj['date'])
            pync.notify('Appointment found for ' + date_obj['date'], title='Appointment available', open='http://myturn.ca.gov')
            send_email(date_obj['date'])
            return

    print('Nothing yet at', datetime.now().strftime("%H:%M:%S"))

sender_email = 'jeremydw.robot@gmail.com' or input('Enter the sender\'s gmail address:')
password = open('password.txt').read() or input_password(sender_email)
receiver_email = 'jeremydw@gmail.com' or input('Enter the recipient\'s email address:')

schedule.every(30).seconds.do(job)

print('Starting...')

while True:
    schedule.run_pending()
    time.sleep(1)
