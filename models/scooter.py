import utils.auth as auth
import db.database as db
from datetime import datetime
import random
from datetime import datetime, timedelta
import utils.validate as v

def get_scooters(search_term):
    conn = db.get_db_connection()
    c = conn.cursor()

    like_term = f"%{search_term}%"
    c.execute("""
        SELECT * FROM scooters 
        WHERE id LIKE ? 
            OR brand LIKE ?
            OR model LIKE ? 
            OR serial_number LIKE ? 
    """, (like_term, like_term, like_term, like_term))

    scooter = c.fetchall()
    conn.close()

    if scooter is None:
        return None

    return scooter


def get_scooter_by_id(id):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM scooters WHERE id = ?", (id,))
    scooter = c.fetchone()
    conn.close()

    if scooter is None:
        return None

    return scooter

def get_scooter_by_serial_number(serial_number):
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM scooters WHERE serial_number = ?", (serial_number,))
    scooter = c.fetchone()
    conn.close()

    if scooter is None:
        return None

    return scooter

def get_all_scooters():
    conn = db.get_db_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM scooters")
    scooters = c.fetchall()
    conn.close()

    if scooters is None:
        return None

    return scooters

def add_scooter(scooter_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()
        in_service_date = datetime.now().strftime("%Y-%m-%d")

        c.execute("""
            INSERT INTO scooters (brand, model, serial_number, top_speed, battery_capacity,
            state_of_charge, target_range_soc, location, out_of_service, mileage,
            last_maintenance_date, in_service_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            scooter_data['brand'],
            scooter_data['model'],
            scooter_data['serial_number'],
            scooter_data['top_speed'],
            scooter_data['battery_capacity'],
            scooter_data['state_of_charge'],
            scooter_data['target_range_soc'],
            scooter_data['location'],
            scooter_data['out_of_service'],
            scooter_data['mileage'],
            scooter_data['last_maintenance_date'],
            in_service_date
        ))

        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def update_scooter(id, scooter_data):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("""
            UPDATE scooters
            SET brand = ?, model = ?, serial_number = ?, top_speed = ?, battery_capacity = ?,
                state_of_charge = ?, target_range_soc = ?, location = ?, out_of_service = ?,
                mileage = ?, last_maintenance_date = ?, in_service_date = ?
            WHERE id = ?
        """, (
            scooter_data['brand'],
            scooter_data['model'],
            scooter_data['serial_number'],
            scooter_data['top_speed'],
            scooter_data['battery_capacity'],
            scooter_data['state_of_charge'],
            scooter_data['target_range_soc'],
            scooter_data['location'],
            scooter_data['out_of_service'],
            scooter_data['mileage'],
            scooter_data['last_maintenance_date'],
            scooter_data['in_service_date'],
            id
        ))

        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def delete_scooter(id):
    try:
        conn = db.get_db_connection()
        c = conn.cursor()

        c.execute("DELETE FROM scooters WHERE id = ?", (id,))
        conn.commit()

        return True

    except Exception as e:
        return e
        
    finally:
        conn.close()

def add_50_scooters(count=50):
    brands_models = {
        "JZScooters": ["JZ50", "JZ100"],
        "JJScooters": ["JJ69", "JJ420"],
        "HRLogistics": ["HR10"],
        "RIM": ["R2000", "R2000GX"]
    }

    successful = 0
    attempts = 0
    max_attempts = count * 2

    while successful < count and attempts < max_attempts:
        attempts += 1

        brand = random.choice(list(brands_models.keys()))
        model = random.choice(brands_models[brand])
        
        serial_number = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=random.randint(10, 17)))
        if not v.is_valid_serial_number(serial_number):
            continue

        top_speed = random.randint(15, 30)
        battery_capacity = random.choice([25, 30])
        state_of_charge = random.randint(0, 100)
        target_range_soc = random.randint(70, 95)

        lat = round(random.uniform(51.87419, 51.95052), 5)
        lon = round(random.uniform(4.29313, 4.54623), 5)
        location = f"{lat},{lon}"

        if not (v.is_valid_latitude(str(lat)) and v.is_valid_longitude(str(lon))):
            continue

        out_of_service = 1 if random.random() < 0.05 else 0

        mileage = round(random.uniform(0, 1000), 2)

        today = datetime.now()
        start_of_year = datetime(today.year, 1, 1)
        days_between = (today - start_of_year).days
        last_maintenance_date = start_of_year + timedelta(days=random.randint(0, days_between))
        last_maintenance_date_str = last_maintenance_date.strftime("%Y-%m-%d")

        scooter_data = {
            "brand": brand,
            "model": model,
            "serial_number": serial_number,
            "top_speed": top_speed,
            "battery_capacity": battery_capacity,
            "state_of_charge": state_of_charge,
            "target_range_soc": target_range_soc,
            "location": location,
            "out_of_service": out_of_service,
            "mileage": mileage,
            "last_maintenance_date": last_maintenance_date_str
        }

        result = add_scooter(scooter_data)
        if result is True:
            successful += 1
        else:
            print(f"[!] Failed to add scooter: {result}")

    print(f"[✓] Successfully added {successful} scooters.")
