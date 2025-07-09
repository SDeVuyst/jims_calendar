import base64
import re
from datetime import datetime, timedelta

import requests
from ics import Calendar, Event

from app.config import settings


def generate_calendar():
    c = Calendar()
    
    # Imagine you have session history as a list of dicts
    sessions = fetch_checkins()  # or fetch from local DB/file
    for s in sessions:
        e = Event()
        e.name = "Gym 💪"
        e.begin = re.sub(r"\[.*?\]", "", s["checkinTime"])
        e.end = re.sub(r"\[.*?\]", "", s["checkoutTime"])
        e.location = s["studioName"]
        e.description = "Auto-logged session"
        c.events.add(e)

    return str(c)


USERNAME = settings.jims_email
PASSWORD = settings.jims_password

LOGIN_URL = "https://myjims.jimsfitness.com/login"
CHECKIN_URL = "https://myjims.jimsfitness.com/selfservice/check-in-history"

def login_session():
    session = requests.Session()

    # Encode credentials as base64
    creds = f"{USERNAME}:{PASSWORD}"
    b64_creds = base64.b64encode(creds.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_creds}",
        "Content-Type": "application/json",
        "Origin": "https://myjims.jimsfitness.com",
        "User-Agent": "Mozilla/5.0",
        "x-tenant": "jimsfitness",
        "x-nox-client-type": "WEB",
        "x-public-facility-group": "JIMS-4428297DBB8242B1854D542AEE224B7F",
    }

    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    res = session.post(LOGIN_URL, json=payload, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Login failed: {res.status_code} - {res.text}")

    print("Login successful")
    return session


def fetch_checkins():
    session = login_session()
    today = datetime.today()
    last_year = today - timedelta(days=365)
    checkin_url = (
        f"https://myjims.jimsfitness.com/nox/v1/studios/checkin/history/report"
        f"?from={last_year.strftime('%Y-%m-%d')}&to={today.strftime('%Y-%m-%d')}"
    )

    checkin_headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "x-tenant": "jimsfitness",
        "x-nox-client-type": "WEB",
        "x-public-facility-group": "JIMS-4428297DBB8242B1854D542AEE224B7F",  # fixed or dynamic depending on account
    }

    resp = session.get(checkin_url, headers=checkin_headers)

    if resp.ok:
        checkins = resp.json()
        return checkins
    else:
        raise Exception(f"Failed to fetch check-ins: {resp.status_code} - {resp.text}")

        

if __name__ == "__main__":
    print(fetch_checkins())