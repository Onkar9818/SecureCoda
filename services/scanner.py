import re
from datetime import datetime, timedelta


def mask_value(value):
    if len(value) <= 4:
        return "*" * len(value)
    return "*" * (len(value) - 3) + value[-3:]


SENSITIVE_PATTERNS = [
    r'password\s*[:=]\s*\w+',
    r'\b\d{16}\b',  # credit card
    r'\b\d{10}\b',  # phone
    r'@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # email
]

def check_unused(doc):
    last_updated = datetime.fromisoformat(doc['updatedAt'].replace("Z", ""))
    return (datetime.utcnow() - last_updated) > timedelta(minutes=1)  # for testing

def check_public(doc):
    return "coda.io/d/" in doc.get("browserLink", "")


def find_sensitive_fields(text):
    findings = []

    #PASSWORD DETECTION
    password_matches = re.findall(r'[A-Za-z]+@\d+', text)
    if password_matches:
        masked = [mask_value(p) for p in password_matches]
        findings.append(f"Password ({', '.join(masked)})")

    #CARD
    card_matches = re.findall(r'\b\d{16}\b', text)
    if card_matches:
        masked = [mask_value(c) for c in card_matches]
        findings.append(f"Card Number ({', '.join(masked)})")

    #AADHAAR
    aadhaar_matches = re.findall(r'\b\d{12}\b', text)
    if aadhaar_matches:
        masked = [mask_value(a) for a in aadhaar_matches]
        findings.append(f"Aadhaar ({', '.join(masked)})")

    #PHONE
    phone_matches = re.findall(r'\b\d{10}\b', text)
    if phone_matches:
        masked = [mask_value(p) for p in phone_matches]
        findings.append(f"Phone ({', '.join(masked)})")

    #EMAIL
    email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_matches:
        masked = [mask_value(e) for e in email_matches]
        findings.append(f"Email ({', '.join(masked)})")

    return findings