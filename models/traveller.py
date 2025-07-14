import random
import utils.auth as auth
import db.database as db
from datetime import datetime, timedelta
from utils.cryptography import encrypt_data, decrypt_data
import utils.validate as v
from faker import Faker
import re

def get_travellers(search_term):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM travellers")
    all_rows = c.fetchall()
    conn.close()

    search_term_lower = search_term.lower()
    filtered = []

    for row in all_rows:
        decrypted = decrypt_traveller_row(row)
        if (
            search_term_lower in str(decrypted["id"]).lower()
            or search_term_lower in decrypted["first_name"].lower()
            or search_term_lower in decrypted["last_name"].lower()
            or search_term_lower in decrypted["city"].lower()
            or search_term_lower in decrypted["email"].lower()
        ):
            filtered.append(decrypted)

    return filtered



def get_traveller_by_id(id):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM travellers WHERE id = ?", (id,))
    traveller = c.fetchone()
    conn.close()

    if traveller is None:
        return None

    return decrypt_traveller_row(traveller)

def get_traveller_by_email(email):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM travellers WHERE email = ?", (email,))
    traveller = c.fetchone()
    conn.close()

    if traveller is None:
        return None

    return decrypt_traveller_row(traveller)

def get_all_travellers():
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM travellers")
    travellers = c.fetchall()
    conn.close()

    if travellers is None:
        return None

    return [decrypt_traveller_row(row) for row in travellers]

def add_traveller(traveller_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()
        registration_date = datetime.now().strftime("%Y-%m-%d")

        c.execute("""
            INSERT INTO travellers (first_name, last_name, birthday, gender, 
                  street_name, house_number, zip_code, city, email, 
                  mobile_phone, driving_license, registration_date)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            encrypt_data(traveller_data['first_name']),
            encrypt_data(traveller_data['last_name']),
            encrypt_data(traveller_data['birthday']),
            encrypt_data(traveller_data['gender']),
            encrypt_data(traveller_data['street_name']),
            encrypt_data(traveller_data['house_number']),
            encrypt_data(traveller_data['zip_code']),
            encrypt_data(traveller_data['city']),
            encrypt_data(traveller_data['email']),
            encrypt_data(traveller_data['mobile_phone']),
            encrypt_data(traveller_data['driving_license']),
            registration_date
            ))
        
        conn.commit()
        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def update_traveller(id, traveller_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("""
            UPDATE travellers
            SET first_name = ?, last_name = ?, birthday = ?, gender = ?, 
                street_name = ?, house_number = ?, zip_code = ?, city = ?, 
                email = ?, mobile_phone = ?, driving_license = ?
            WHERE id = ?
        """, (
            encrypt_data(traveller_data['first_name']),
            encrypt_data(traveller_data['last_name']),
            encrypt_data(traveller_data['birthday']),
            encrypt_data(traveller_data['gender']),
            encrypt_data(traveller_data['street_name']),
            encrypt_data(traveller_data['house_number']),
            encrypt_data(traveller_data['zip_code']),
            encrypt_data(traveller_data['city']),
            encrypt_data(traveller_data['email']),
            encrypt_data(traveller_data['mobile_phone']),
            encrypt_data(traveller_data['driving_license']),
            id
        ))

        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def delete_traveller(id):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("DELETE FROM travellers WHERE id = ?", (id,))
        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def decrypt_traveller_row(row):
    return {
        "id": row["id"],
        "first_name": decrypt_data(row["first_name"]),
        "last_name": decrypt_data(row["last_name"]),
        "birthday": decrypt_data(row["birthday"]),
        "gender": decrypt_data(row["gender"]),
        "street_name": decrypt_data(row["street_name"]),
        "house_number": decrypt_data(row["house_number"]),
        "zip_code": decrypt_data(row["zip_code"]),
        "city": decrypt_data(row["city"]),
        "email": decrypt_data(row["email"]),
        "mobile_phone": decrypt_data(row["mobile_phone"]),
        "driving_license": decrypt_data(row["driving_license"]),
        "registration_date": row["registration_date"]
    }

def add_50_travellers(count=50):
    fake = Faker()

    valid_cities = [
        "Rotterdam", "Amsterdam", "The Hague", "Haarlem", "Utrecht",
        "Leeuwarden", "Groningen", "Breda", "Delft", "Zwolle"
    ]

    successful = 0
    attempts = 0
    max_attempts = count * 3

    while successful < count and attempts < max_attempts:
        attempts += 1

        gender = random.choice(["male", "female"])
        first_name = fake.first_name_male() if gender == "male" else fake.first_name_female()
        last_name = fake.last_name()

        age = random.randint(18, 65)
        birthday = (datetime.now() - timedelta(days=age * 365)).strftime("%Y-%m-%d")

        street_name = fake.street_name()
        house_number = str(random.randint(1, 200))

        zip_code = f"{random.randint(1000, 9999)}{random.choice(['AB', 'CD', 'EF', 'GH', 'IJ', 'KL', 'MN', 'OP', 'QR', 'ST'])}"
        if not v.is_valid_zip_code(zip_code):
            continue

        city = random.choice(valid_cities)

        email = fake.email()
        if not v.is_valid_email(email):
            continue

        mobile_phone = str(random.randint(10000000, 99999999))

        prefix = random.choice(["X", "AB", "K", "L"])
        if len(prefix) == 1:
            number_part = f"{random.randint(10000000, 99999999)}"[1:]
        else:
            number_part = f"{random.randint(1000000, 9999999)}"
        driving_license = prefix + number_part

        if not v.is_valid_driving_license(driving_license):
            continue

        traveller_data = {
            "first_name": first_name,
            "last_name": last_name,
            "birthday": birthday,
            "gender": gender,
            "street_name": street_name,
            "house_number": house_number,
            "zip_code": zip_code,
            "city": city,
            "email": email,
            "mobile_phone": mobile_phone,
            "driving_license": driving_license
        }

        result = add_traveller(traveller_data)
        if result is True:
            successful += 1
        else:
            print(f"[!] Failed to add traveller: {result}")

    print(f"[✓] Successfully added {successful} travellers.")