from datetime import datetime


def is_valid_zip_code(zip_code: str) -> bool:
    return (
        len(zip_code) == 6 and
        zip_code[:4].isdigit() and
        zip_code[4:].isalpha() and
        zip_code[4:].isupper()
    )

def is_valid_phone_number(phone_number: str) -> bool:
    return (
        len(phone_number) == 8 and
        phone_number[:8].isdigit()
    )

def is_valid_driving_license(driving_license: str) -> bool:
    return (
        len(driving_license) == 9 and
        (driving_license[:1].isalpha() or driving_license[:2].isalpha()) and
        (driving_license[2:9].isdigit() or driving_license[3:9].isdigit())
    )

def is_valid_serial_number(serial_number: str) -> bool:
    return (
        len(serial_number) <= 17 and
        len(serial_number) >= 10 and
        serial_number.isalpha()
    )

def is_valid_latitude(latitude: str) -> bool:
    try:
        lat = float(latitude)
        return 51.87419 <= lat <= 51.95052
    except ValueError:
        return False

def is_valid_longitude(longitude: str) -> bool:
    try:
        lon = float(longitude)
        return 4.29313 <= lon <= 4.54623
    except ValueError:
        return False
    
def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_charge_state(charge_state: str) -> bool:
    try:
        charge = int(charge_state)
        return 0 <= charge <= 100
    except ValueError:
        return False
    
def is_valid_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    local_part, domain = email.split("@")
    return (
        "@" in email and 
        "." in email and
        len(local_part) > 0 and 
        len(domain) > 0 and
        domain.count(".") == 1
    )

def is_valid_house_number(housenumber: str) -> bool:
    if not housenumber:
        return False
    if housenumber.isdigit() and int(housenumber) > 0:
        return True
    if len(housenumber) > 1 and housenumber[:-1].isdigit() and housenumber[-1].isalpha():
        return True
    return False

def is_valid_street_name(street_name: str) -> bool:
    if not street_name:
        return False
    if len(street_name) > 3 and len(street_name) < 75:
        return True
    return False