import base64
import re
from datetime import datetime, timedelta

import requests
import uuid
from icalendar import Calendar, Event

from app.config import settings


def generate_calendar():
    cal = Calendar()
    cal.add('prodid', '-//Gym Calendar//EN')
    cal.add('version', '2.0')
    
    sessions = fetch_checkins()  # get your gym check-in data
    
    for s in sessions:
        e = Event()
        e.add("summary", "Gym 💪")
        
        # Clean timestamps
        start_str = re.sub(r"\[.*?\]", "", s["checkinTime"]).strip()
        end_str = re.sub(r"\[.*?\]", "", s["checkoutTime"]).strip()

        # Convert strings to datetime objects
        e.add('dtstart', datetime.fromisoformat(start_str))
        e.add('dtstart', datetime.fromisoformat(end_str))

        # Add required fields
        e.add("uid", str(uuid.uuid5(uuid.NAMESPACE_X500, start_str)))  # unique ID
        e.add("dtstamp", datetime.fromisoformat(start_str))

        # Optional fields
        e.add("location", s.get("studioName", "Gym"))
        e.add("description", "Auto-logged session")

        cal.add_component(e)

    return cal.to_ical()


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