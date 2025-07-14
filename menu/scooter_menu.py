import time
import json
from datetime import datetime
import utils.validate as v
import utils.utils as utils
import models.scooter as s
import models.log as log


def scooter_data_menu(user):
    while True:
        choices = ["1", "2", "3", "4", "5", "6", 
                   "e", "a", "d", "v", "s", "q",
                   "E", "A", "D", "V", "S", "Q"]
        
        se_choices = ["1", "2", "3", "4", 
                      "e", "v", "s", "q",
                      "E", "V", "S", "Q"]
        choice = None

        if user['role'] == "system_admin" or user['role'] == "super_admin":
            while choice not in choices:
                utils.clear_screen()
                print("\n=== Scooter data Menu ===")
                print("1. [e] Edit a Scooter")
                print("2. [a] Add Scooter")
                print("3. [d] Delete Scooter")
                print("4. [v] View all Scooters")
                print("5. [s] Search for Scooters")
                utils.print_colored("6. [q] Quit to Main Menu", "blue")
                choice = input("\nSelect an option: ").strip()
                if choice not in se_choices:
                    utils.print_colored("\n[!] Invalid option. Please try again.", "red")
                    time.sleep(0.5)
                    continue
        elif user['role'] == "service_engineer":
            while choice not in se_choices:
                utils.clear_screen()
                print("\n=== Scooter data Menu ===")
                print("1. [e] Edit a Scooter")
                print("2. [v] View all Scooters")
                print("3. [s] Search for Scooters")
                utils.print_colored("4. [q] Quit to Main Menu", "blue")
                choice = input("\nSelect an option: ").strip()
                if choice not in choices:
                    utils.print_colored("\n[!] Invalid option. Please try again.", "red")
                    time.sleep(0.5)
                    continue
        else:
            utils.clear_screen()
            utils.print_colored("[!] Access Denied. You do not have permission to access this menu.", "red")
            time.sleep(1.5)
            return
            
        utils.clear_screen()


        if user['role'] == "system_admin" or user['role'] == "super_admin":
            match choice:
                case "1" | "e" | "E":
                    while True:
                        utils.clear_screen()
                        print("\n=== Edit Scooter data ===")

                        print("Available scooters:")
                        scooters = s.get_all_scooters()
                        if not scooters:
                            utils.print_colored("[!] No scooters found.", "red")
                            input("Press Enter to continue...")
                            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                            time.sleep(1)
                            break
                        print(f"ID | Serial Number")
                        print("-" * 20)
                        for scooter in scooters:
                            print(f"{scooter['id']:<3}| {scooter['serial_number']:<17}")

                        print("Which scooter do you want to modify?")
                        scooter = input("\nEnter Scooter ID or Serial Number: ").strip()
                        if scooter.isdigit():
                            scooter_data = s.get_scooter_by_id(scooter)
                            choice = "id"

                        elif v.is_valid_serial_number(scooter):
                            scooter_data = s.get_scooter_by_serial_number(scooter)
                            choice = "serial_number"
                        elif choice.lower() == "q":
                            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                            time.sleep(1)
                            return

                        else:
                            utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
                            time.sleep(1.5)
                            utils.remove_last_line()
                            continue

                        if scooter_data:
                            edit_scooter(scooter_data, user, choice)
                        else:
                            utils.print_colored("[!] Scooter not found.", "red")
                            time.sleep(1.5)
                            utils.remove_last_line()
                            choice = input("Do you want to try again? (y/n): ").strip().lower()
                            if choice == "y":
                                continue
                            else:
                                utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                                time.sleep(1)

                        break

                case "2" | "a" | "A":
                    add_scooter(user)
                case "3" | "d" | "D":
                    delete_scooter_data(user)
                case "4" | "v" | "V":
                    view_all_scooters()
                case "5" | "s" | "S":
                    search_scooter(user)
                case "6" | "q" | "Q":
                    utils.print_colored("[↩] Returning to Main Menu...\n", "blue")
                    time.sleep(1)
                    break
        elif user['role'] == "service_engineer":
            match choice:
                case "1" | "e" | "E":
                    while True:
                        utils.clear_screen()
                        print("\n=== Edit Scooter data ===")

                        print("Available scooters:")
                        scooters = s.get_all_scooters()
                        if not scooters:
                            utils.print_colored("[!] No scooters found.", "red")
                            input("Press Enter to continue...")
                            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                            time.sleep(1)
                            break
                        print(f"ID | Serial Number")
                        print("-" * 20)
                        for scooter in scooters:
                            print(f"{scooter['id']:<3}| {scooter['serial_number']:<17}")

                        print("Which scooter do you want to modify?")
                        scooter = input("\nEnter Scooter ID or Serial Number: ").strip()
                        if scooter.isdigit():
                            scooter_data = s.get_scooter_by_id(scooter)
                            choice = "id"

                        elif v.is_valid_serial_number(scooter):
                            scooter_data = s.get_scooter_by_serial_number(scooter)
                            choice = "serial_number"
                        elif choice.lower() == "q":
                            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                            time.sleep(1)
                            return

                        else:
                            utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
                            time.sleep(1.5)
                            utils.remove_last_line()
                            continue

                        if scooter_data:
                            edit_scooter(scooter_data, user, choice)
                        else:
                            utils.print_colored("[!] Scooter not found.", "red")
                            time.sleep(1.5)
                            utils.remove_last_line()
                            choice = input("Do you want to try again? (y/n): ").strip().lower()
                            if choice == "y":
                                continue
                            else:
                                utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                                time.sleep(1)

                        break

                case "2" | "v" | "V":
                    view_all_scooters()
                case "3" | "s" | "S":
                    search_scooter(user)
                case "4" | "q" | "Q":
                    utils.print_colored("[↩] Returning to Main Menu...\n", "blue")
                    time.sleep(1)
                    break


def view_all_scooters():
    print("\n=== All Scooter data ===")
    scooters = s.get_all_scooters()
    if scooters:
        print(f"ID | {'Brand':<14} | {'Model':<7} | {'Serial Number':<17} | Top Speed | Battery Cap | SOC | Target Range | {'Location':<16} | Out of Service | Mileage | Last Maintenance | In Service")
        print("-" * 166)
        for scooter in scooters:
            print(f"{scooter['id']:<3}| {scooter['brand']:<14} | {scooter['model']:<8}| {scooter['serial_number']:<17} | {scooter['top_speed']:<10}| {scooter['battery_capacity']:<12}| {scooter['state_of_charge']:<4}| {scooter['target_range_soc']:<13}| {scooter['location']:<17}| {scooter['out_of_service']:<15}| {scooter['mileage']:<8}| {scooter['last_maintenance_date']:<17}| {scooter['in_service_date']:<12}")
        input("\nPress Enter to continue...")
    else:
        utils.print_colored("[!] No scooters found.", "red")
        input("Press Enter to continue...")
    utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
    time.sleep(1)
    utils.clear_screen()


def view_scooters(scooters):
    print("\n=== Scooter data ===")
    if scooters:
        print(f"ID | {'Brand':<8} | Model | {'Serial Number':<17} | Top Speed | Battery Cap | SOC | Target Range | {'Location':<16} | Out of Service | Mileage | Last Maintenance | In Service")
        print("-" * 166)
        for scooter in scooters:
            print(f"{scooter['id']:<3}| {scooter['brand']:<8} | {scooter['model']:<6}| {scooter['serial_number']:<17} | {scooter['top_speed']:<10}| {scooter['battery_capacity']:<12}| {scooter['state_of_charge']:<4}| {scooter['target_range_soc']:<13}| {scooter['location']:<17}| {scooter['out_of_service']:<15}| {scooter['mileage']:<8}| {scooter['last_maintenance_date']:<17}| {scooter['in_service_date']:<12}")
    else:
        utils.print_colored("[!] No scooters found.", "red")
    input("\nPress Enter to continue...")


def add_scooter(user):
    utils.clear_screen()
    print("\n=== Add Scooter data ===")

    while True:
        brand = input("Brand: ").strip()
        if brand is None or brand == "":
            utils.print_colored("[!] Brand cannot be empty.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        else:
            break

    while True:
        model = input("Model: ").strip()
        if model is None or model == "":
            utils.print_colored("[!] Model cannot be empty.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        else:
            break

    while True:
        serial_number = input("Serial Number: ").strip()
        if v.is_valid_serial_number(serial_number):
            break
        else:
            utils.print_colored("[!] Invalid Serial Number. It should be 10 characters long and not longer than 17 characters.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    while True:  
        top_speed = input("Top Speed (km/h): ").strip()
        if top_speed.isdigit():
            top_speed = float(top_speed)
            if top_speed > 0:
                break
            else:
                utils.print_colored("[!] Top Speed should be greater than 0.", "red")
                time.sleep(1)
                utils.remove_last_line()
                continue
        else:
            utils.print_colored("[!] Invalid Speed should. It should be a number.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
    
    while True:  
        battery_capacity = input("Battery Capacity (Ah): ").strip()
        if battery_capacity.isdigit():
            battery_capacity = float(battery_capacity)
            if battery_capacity > 0:
                break
            else:
                utils.print_colored("[!] Battery Capacity should be greater than 0.", "red")
                time.sleep(1)
                utils.remove_last_line()
                continue
        else:
            utils.print_colored("[!] Invalid Battery Capacity. It should be a number.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    while True:
        state_of_charge = input("State of Charge (%): ").strip()
        if v.is_valid_charge_state(state_of_charge):
            break
        else:
            utils.print_colored("[!] Invalid State of Charge. It should be between 0 and 100.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
    while True:
        target_range_soc = input("Target Range SOC: ").strip()
        if v.is_valid_charge_state(target_range_soc):
            break
        else:
            utils.print_colored("[!] Invalid Target Range SOC. It should be between 0 and 100.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    while True:
        latitude = input("Location Latitude (xx.xxxxx): ").strip()
        if v.is_valid_latitude(latitude):
            break
        else:
            utils.print_colored("[!] Invalid Latitude. It should be between 51.87419 and 51.95052.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue
        
    while True:
        longitude = input("Location Longitude (x.xxxxx): ").strip()
        if v.is_valid_longitude(longitude):
            break
        else:
            utils.print_colored("[!] Invalid Longitude. It should be between 4.29313 and 4.54623.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    location = latitude + ", " + longitude

    while True:
        out_of_service = input("Out of Service (0 for No, 1 for Yes): ").strip()
        if out_of_service in ["0", "1"]:
            break
        else:
            utils.print_colored("[!] Invalid input. Please enter 0 or 1.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    while True:
        mileage = input("Mileage (km): ").strip()
        if mileage.isdigit() and float(mileage) >= 0:
            mileage = float(mileage)
            break
        else:
            utils.print_colored("[!] Invalid Mileage. It should be a number and higher than 0.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue            

    while True:
        last_maintenance_date = input("Last Maintenance Date (YYYY-MM-DD): ").strip()
        if v.is_valid_date(last_maintenance_date):
            break
        else:
            utils.print_colored("[!] Invalid date format. Please use YYYY-MM-DD.", "red")
            time.sleep(1)
            utils.remove_last_line()
            continue

    in_service_date = datetime.now().strftime("%Y-%m-%d")
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
        "last_maintenance_date": last_maintenance_date,
        "in_service_date": in_service_date
    }
    print("\n[..] Adding scooter to Database.")
    time.sleep(1)

    if s.add_scooter(scooter_data):
        utils.print_colored("[✓] Scooter data added successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Add Scooter",
            "additional_info": f"Added scooter with serial number {serial_number}",
            "suspicious": 0
        }
        log.add_log(log_data)

        time.sleep(0.5)
    else:
        utils.print_colored("[!] Failed to add scooter data.", "red")
        time.sleep(0.5)
    utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
    time.sleep(1)


def edit_scooter(scooter_data, user, search,):
    utils.clear_screen()
    print("\n=== Edit Scooter data ===")
    if search == "id":
        print(f"Editing Scooter ID: {scooter_data[search]}\n")
    elif search == "serial_number":
        print(f"Editing Scooter Serial Number: {scooter_data[search]}\n")
    
    scooter_dict = dict(scooter_data)

    for key, value in scooter_dict.items():
        if key == "in_service_date":
            continue
        print(f"{key.replace('_', ' ').title()}: \033[1m{value}\033[0m")
        print("-" * 40)

    if user['role'] == "service_engineer":
        editable_fields = [
            "state_of_charge", "target_range_soc", "location", "out_of_service",
            "mileage", "last_maintenance_date"
        ]
    else:
        editable_fields = [
            "brand", "model", "serial_number", "top_speed", "battery_capacity",
            "state_of_charge", "target_range_soc", "location", "out_of_service",
            "mileage", "last_maintenance_date"
        ]

    for field in editable_fields:
        if field == "brand":
            while True:
                new_value = input("Enter new Brand (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                else:
                    scooter_dict[field] = new_value
                break
        elif field == "model":
            while True:
                new_value = input("Enter new Model (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                else:
                    scooter_dict[field] = new_value
                break
        elif field == "serial_number":
            while True:
                new_value = input("Enter new Serial Number (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif v.is_valid_serial_number(new_value):
                    scooter_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid Serial Number. It should be 10 characters long and not longer than 17 characters.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "top_speed":
            while True:
                new_value = input("Enter new Top Speed (km/h) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif new_value.isdigit() and float(new_value) >= 0:
                    scooter_dict[field] = float(new_value)
                else:
                    utils.print_colored("[!] Invalid Speed. It should be a number and higher than 0.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "battery_capacity":
            while True:
                new_value = input("Enter new Battery Capacity (Ah) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif new_value.isdigit() and float(new_value) >= 0:
                    scooter_dict[field] = float(new_value)
                else:
                    utils.print_colored("[!] Invalid Battery Capacity. It should be a number and higher than 0.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "state_of_charge":
            while True:
                new_value = input("Enter new State of Charge (%) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif v.is_valid_charge_state(new_value):
                    scooter_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid State of Charge. It should be between 0 and 100.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "target_range_soc":
            while True:
                new_value = input("Enter new Target Range SOC (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif v.is_valid_charge_state(new_value):
                    scooter_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid Target Range SOC. It should be between 0 and 100.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "location":
            while True:
                latitude = input("Enter new Location Latitude (xx.xxxxx) (leave empty to keep current): ").strip()
                if latitude == "":
                    latitude = scooter_dict['location'].split(", ")[0]
                elif v.is_valid_latitude(latitude):
                    longitude = input("Enter new Location Longitude (x.xxxxx): ").strip()
                    if v.is_valid_longitude(longitude):
                        scooter_dict['location'] = f"{latitude}, {longitude}"
                    else:
                        utils.print_colored("[!] Invalid Longitude. It should be between 4.29313 and 4.54623.", "red")
                        time.sleep(1)
                        utils.remove_last_line()
                        continue
                else:
                    utils.print_colored("[!] Invalid Latitude. It should be between 51.87419 and 51.95052.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "out_of_service":
            while True:
                new_value = input("Enter new Out of Service (0 for No, 1 for Yes) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif new_value in ["0", "1"]:
                    scooter_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid input. Please enter 0 or 1.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "mileage":
            while True:
                new_value = input("Enter new Mileage (km) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif new_value.isdigit() and float(new_value) >= 0:
                    scooter_dict[field] = float(new_value)
                else:
                    utils.print_colored("[!] Invalid Mileage. It should be a number and higher than 0.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break
        elif field == "last_maintenance_date":
            while True:
                new_value = input("Enter new Last Maintenance Date (YYYY-MM-DD) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = scooter_dict[field]
                elif v.is_valid_date(new_value):
                    scooter_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid date format. Please use YYYY-MM-DD.", "red")
                    time.sleep(1)
                    utils.remove_last_line()
                    continue
                break

    if s.update_scooter(scooter_dict['id'], scooter_dict):
        utils.print_colored("[✓] Scooter data updated successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Edit Scooter",
            "additional_info": f"Edited scooter with serial number {scooter_dict['serial_number']}",
            "suspicious": 0
        }
        log.add_log(log_data)
        time.sleep(1)
    else:
        utils.print_colored("[!] Failed to update scooter data.", "red")
        time.sleep(1)
                

def delete_scooter_data(user):
    utils.clear_screen()
    print("\n=== Delete Scooter data ===")
    print("Press 'q' to return to the Scooter data Menu.")
    while True:
        scooter = input("Enter Scooter ID or Serial Number to delete: ").strip()
        if scooter == "q":
            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
            time.sleep(1)
            return
        if scooter.isdigit():
            scooter_data = s.get_scooter_by_id(scooter)
            break
        elif v.is_valid_serial_number(scooter):
            scooter_data = s.get_scooter_by_serial_number(scooter)
            break
        else:
            utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            continue
    
    if scooter_data:
        print(f"Are you sure you want to delete the scooter with Serial Number: {scooter_data['serial_number']}? (y/n)")
        choice = input().strip().lower()
        if choice == "y":
            if s.delete_scooter(scooter_data['id']):
                utils.print_colored("[✓] Scooter data deleted successfully.", "green")
                log.add_log({
                    "username": user['username'],
                    "activity": "Delete Scooter",
                    "additional_info": f"Deleted scooter with serial number {scooter_data['serial_number']}",
                    "suspicious": 0
                })
                time.sleep(1)
                utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
                time.sleep(1)
            else:
                utils.print_colored("[!] Failed to delete scooter data.", "red")
                time.sleep(1)

        else:
            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
            time.sleep(1)
    else:
        utils.print_colored("[!] Scooter not found.", "red")
        time.sleep(1.5)
        utils.remove_last_line()
        utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
        time.sleep(1)


def search_scooter(user):
    utils.clear_screen()
    print("\n=== Search Scooter data ===")
    print("Press 'q' to return to the Scooter data Menu.")
    while True:
        search_key = input("Enter Search Key: ").strip()
        if search_key == "q":
            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
            time.sleep(1)
            return
        if search_key.isdigit():
            scooter_data = s.get_scooters(search_key)
            break
        elif search_key.isalpha():
            scooter_data = s.get_scooters(search_key)
            break
        elif search_key.__contains__("-", ",", ":",";", "{", "}", "[", "]", "(", ")", "/"):
            utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            log.add_log({
                "username": user['username'],
                "activity": "Search Scooter",
                "additional_info": f"Failed search with Search Key: {search_key}",
                "suspicious": 1
            })
        else:
            utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            continue
    
    if scooter_data:
        log.add_log({
            "username": user['username'],
            "activity": "Search Scooter",
            "additional_info": f"Searched for scooter with Search Key: {search_key}",
            "suspicious": 0
        })
        view_scooters(scooter_data)
    else:
        utils.print_colored("[!] Scooter not found.", "red")
        time.sleep(1.5)
        utils.remove_last_line()
    
    utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
    time.sleep(1)