import time
import utils.utils as utils
import utils.validate as v
import models.traveller as t
import models.log as log

def traveller_data_menu(user):
    while True:
        choices = ["1", "2", "3", "4", "5", "6", 
                   "e", "a", "d", "v", "s", "q",
                   "E", "A", "D", "V", "S", "Q"]
        choice = None

        if user['role'] == "system_admin" or user['role'] == "super_admin":
            while choice not in choices:
                utils.clear_screen()
                print("\n=== Traveller data Menu ===")
                print("1. [e] Edit a Traveller")
                print("2. [a] Add Traveller")
                print("3. [d] Delete Traveller")
                print("4. [v] View all Travellers")
                print("5. [s] Search for Traveller")
                utils.print_colored("6. [q] Quit to Main Menu", "blue")
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

        match choice:
            case "1" | "e":
                while True:
                    utils.clear_screen()
                    print("\n=== Edit Traveller data ===")

                    print("Available travellers:")
                    travellers = t.get_all_travellers()
                    if not travellers:
                        utils.print_colored("[!] No travellers found.", "red")
                        input("Press Enter to continue...")
                        utils.print_colored("[↩] Returning to traveller data Menu...\n", "blue")
                        time.sleep(1)
                        break
                    print(f"ID | Email")
                    print("-" * 20)
                    for traveller in travellers:
                        print(f"{traveller['id']:<3}| {traveller['email']:<17}")

                    print("Which traveller do you want to modify?")
                    key = input("\nEnter Traveller ID or email: ").strip()
                    if key.isdigit():
                        traveller_data = t.get_traveller_by_id(key)
                        choice = "id"

                    elif v.is_valid_email(key):
                        traveller_data = t.get_traveller_by_email(key)
                        choice = "serial_number"
                    elif key.lower() == "q":
                        utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
                        time.sleep(1)
                        return
                    else:
                        utils.print_colored("[!] Invalid input. Please enter a valid Scooter ID or Serial Number.", "red")
                        time.sleep(1.5)
                        utils.remove_last_line()
                        continue

                    if traveller_data:
                        edit_traveller(traveller_data, user, choice)
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
                add_traveller(user)
            case "3" | "d" | "D":
                delete_traveller_data(user)
            case "4" | "v" | "V":
                view_all_travellers()
            case "5" | "s" | "S":
                search_traveller(user)
            case "6" | "q" | "Q":
                utils.print_colored("[↩] Returning to Main Menu...\n", "blue")
                time.sleep(1)
                return

def view_all_travellers():
    print("\n=== All Traveller data ===")
    travellers = t.get_all_travellers()
    if travellers:
        print(f"ID | {'First Name':<12} | {'Last Name':<12} | {'Email':<30} | {'City':<12}")
        print("-" * 78)
        for traveller in travellers:
            print(f"{traveller['id']:<3}| {traveller['first_name']:<12} | {traveller['last_name']:<12} | {traveller['email']:<30} | {traveller['city']:<12}")

        input("\nPress Enter to continue...")
    else:
        utils.print_colored("[!] No travellers found.", "red")
        input("Press Enter to continue...")
    utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
    time.sleep(1)
    utils.clear_screen()


def view_travellers(travellers):
    print("\n=== Traveller data ===")
    if travellers:
        print(f"ID | {'First Name':<12} | {'Last Name':<12} | {'Email':<25} | {'City':<12}")
        print("-" * 78)
        for traveller in travellers:
            print(f"{traveller['id']:<3}| {traveller['first_name']:<12} | {traveller['last_name']:<12} | {traveller['email']:<25} | {traveller['city']:<12}")
    else:
        utils.print_colored("[!] No scooters found.", "red")
    input("\nPress Enter to continue...")    


def add_traveller(user):
    print("\n=== Add Traveller data ===")
    first_name = input("First Name: ").strip()

    last_name = input("Last Name: ").strip()

    while True:
        gender_choice = input("Select an option: \n1. Male\n2. Female\n3. Other\n").strip()
        match gender_choice:
            case "1":
                gender = "Male"
                print("Gender: Male")
                break
            case "2":
                gender = "Female"
                print("Gender: Female")
                break
            case "3":
                gender = input("What is your Gender: ").strip()
                break
            case _:
                utils.print_colored("[!] Invalid option. Please try again.", "red")
                continue

    while True:
        street_name = input("Street Name: ").strip()
        if v.is_valid_street_name(street_name):
            break
        else:
            utils.print_colored("[!] Invalid Street Name.", "red")
            continue
    
    while True:
        house_number = input("House Number: ").strip()
        if v.is_valid_house_number(house_number):
            break
        else:
            utils.print_colored("[!] Invalid House Number.", "red")
            continue

    while True:
        zip_code = input("Zip Code: ").strip()
        if len(zip_code) == 6 and v.is_valid_zip_code(zip_code):
            break
        else:
            utils.print_colored("[!] Invalid Zip Code.", "red")
            continue
    
    while True:
        print("Select an option: \n1. Rotterdam\n2. Amsterdam\n3. The Hague\n4. Haarlem\n5. Utrecht\n6. Leeuwarden\n7. Groningen\n8. Breda\n9. Delft\n10. Zwolle")
        city_choice = input("City: ").strip()
        match city_choice.lower():
            case "1":
                city = "Rotterdam"
                break
            case "2":
                city = "Amsterdam"
                break
            case "3":
                city = "The Hague"
                break
            case "4":
                city = "Haarlem"
                break
            case "5":
                city = "Utrecht"
                break
            case "6":
                city = "Leeuwarden"
                break
            case "7":
                city = "Groningen"
                break
            case "8":
                city = "Breda"
                break
            case "9":
                city = "Delft"
                break
            case "10":
                city = "Zwolle"
                break
            case _:
                utils.print_colored("[!] Invalid option. Please try again.", "red")
                continue

    while True:
        email = input("Email: ").strip()
        if v.is_valid_email(email):
            break
        else:
            utils.print_colored("[!] Invalid Email.", "red")
            continue
    
    while True:
        mobile_phone = input("Mobile Phone: +31-6-").strip()
        if v.is_valid_phone_number(mobile_phone):
            break
        else:
            utils.print_colored("[!] Invalid Mobile Phone number.", "red")
            continue

    while True:
        driving_license = input("Driving License (XDDDDDDDD): ").strip()
        if v.is_valid_driving_license(driving_license):
            break
        else:
            utils.print_colored("[!] Invalid Driving License. Please use the following format: XDDDDDDDD", "red")
            continue

    traveller_data = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "street_name": street_name,
        "house_number": house_number,
        "zip_code": zip_code,
        "city": city,
        "email": email,
        "mobile_phone": mobile_phone,
        "driving_license": driving_license,
    }

    print("\n[..] Adding traveller to Database.")
    time.sleep(1)

    if t.add_traveller(traveller_data):
        utils.print_colored("[✓] Traveller data added successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Add Traveller",
            "additional_info": f"Added traveller with email {email}",
            "suspicious": 0
        }
        log.add_log(log_data)

        time.sleep(0.5)
    else:
        utils.print_colored("[!] Failed to add traveller data.", "red")
        time.sleep(0.5)
    utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
    time.sleep(1)

def edit_traveller(traveller_data, user, key):
    utils.clear_screen()
    print("\n=== Edit Traveller data ===")
    if key == "id":
        print(f"Editing Traveller ID: {traveller_data[key]}\n")
    elif key == "email":
        print(f"Editing Traveller Email: {traveller_data[key]}\n")
    
    traveller_dict = dict(traveller_data)

    for key, value in traveller_dict.items():
        if key == "registration_date":
            continue
        print(f"{key.replace('_', ' ').title()}: \033[1m{value}\033[0m")
        print("-" * 40)

    editable_fields = [
        "first_name", "last_name", "birthday", "gender", 
        "street_name", "house_number", "zip_code", "city", "email", 
        "mobile_phone", "driving_license", "registration_date"
    ]

    for field in editable_fields:
        if field == "first_name":
            while True:
                new_value = input("Enter new first name (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                else:
                    traveller_dict[field] = new_value
                break
        elif field == "last_name":
            while True:
                new_value = input("Enter new last name (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                else:
                    traveller_dict[field] = new_value
                break
        elif field == "birthday":
            while True:
                new_value = input("Enter new birthday (YYYY-MM-DD) (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                else:
                    if v.is_valid_date(new_value):
                        traveller_dict[field] = new_value
                    else:
                        utils.print_colored("[!] Invalid date format. Please use YYYY-MM-DD.", "red")
                        continue
                break
        elif field == "gender":
            while True:
                new_value = input("Enter new gender (male, female): ").strip().lower()
                if new_value == "":
                    new_value = traveller_dict[field]
                elif new_value in ["male", "female"]:
                    traveller_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid gender. Please choose male/female", "red")
                    continue
                break
        elif field == "street_name":
            while True:
                new_value = input("Enter new street name (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                else:
                    traveller_dict[field] = new_value
                break
        elif field == "house_number":
            while True:
                new_value = input("Enter new house number (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                else:
                    traveller_dict[field] = new_value
                break
        elif field == "zip_code":
            while True:
                new_value = input("Enter new zip code (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                elif v.is_valid_zip_code(new_value):
                    traveller_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid zip code. Please enter a valid 6-digit zip code.", "red")
                    continue
                break
        elif field == "city":
            while True:
                print("Select a new city: \n1. Rotterdam\n2. Amsterdam\n3. The Hague\n4. Haarlem\n5. Utrecht\n6. Leeuwarden\n7. Groningen\n8. Breda\n9. Delft\n10. Zwolle")
                new_value = input("City: ").strip()
                match new_value:
                    case "":
                        new_value = traveller_dict[field]
                        continue
                    case "1":
                        new_value = "Rotterdam"
                    case "2":
                        new_value = "Amsterdam"
                    case "3":
                        new_value = "The Hague"
                    case "4":
                        new_value = "Haarlem"
                    case "5":
                        new_value = "Utrecht"
                    case "6":
                        new_value = "Leeuwarden"
                    case "7":
                        new_value = "Groningen"
                    case "8":
                        new_value = "Breda"
                    case "9":
                        new_value = "Delft"
                    case "10":
                        new_value = "Zwolle"
                    case _:
                        utils.print_colored("[!] Invalid option. Please try again.", "red")
                        continue
                traveller_dict[field] = new_value
                break
        elif field == "email":
            while True:
                new_value = input("Enter new email (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                elif v.is_valid_email(new_value):
                    traveller_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid email format. Please try again.", "red")
                    continue
                break
        elif field == "mobile_phone":
            while True:
                new_value = input("Enter new mobile phone number (leave empty to keep current): 31-6-").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                elif v.is_valid_phone_number(new_value):
                    traveller_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid mobile phone number. Please try again.", "red")
                    continue
                break
        elif field == "driving_license":
            while True:
                new_value = input("Enter new driving license (leave empty to keep current): ").strip()
                if new_value == "":
                    new_value = traveller_dict[field]
                elif v.is_valid_driving_license(new_value):
                    traveller_dict[field] = new_value
                else:
                    utils.print_colored("[!] Invalid driving licence number (XDDDDDDDD/XXDDDDDDD). Please try again.", "red")
                    continue
                break
    
    if t.update_traveller(traveller_dict['id'], traveller_dict):
        utils.print_colored("[✓] Traveller data updated successfully.", "green")
        log_data = {
            "username": user['username'],
            "activity": "Edit Traveller",
            "additional_info": f"Edited traveller with email {traveller_dict['email']}",
            "suspicious": 0
        }
        log.add_log(log_data)
        time.sleep(1)
    else:
        utils.print_colored("[!] Failed to update traveller data.", "red")
        time.sleep(1)

def delete_traveller_data(user):
    utils.clear_screen()
    print("\n=== Delete Traveller data ===")
    print("Press 'q' to return to the Traveller data Menu.")
    while True:
        key = input("Enter Traveller ID or Email to delete: ").strip()
        if key == "q":
            utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
            time.sleep(1)
            return
        if key.isdigit():
            traveller_data = t.get_traveller_by_id(key)
            break
        elif v.is_valid_email(key):
            traveller_data = t.get_traveller_by_email(key)
            break
        else:
            utils.print_colored("[!] Invalid input. Please enter a valid Traveller ID or Email.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            continue
    
    if traveller_data:
        print(f"Are you sure you want to delete the traveller with Email: {traveller_data['email']}? (y/n)")
        choice = input().strip().lower()
        if choice == "y":
            if t.delete_traveller(traveller_data['id']):
                utils.print_colored("[✓] Traveller data deleted successfully.", "green")
                log.add_log({
                    "username": user['username'],
                    "activity": "Delete Traveller",
                    "additional_info": f"Deleted traveller with email {traveller_data['email']}",
                    "suspicious": 0
                })
                time.sleep(1)
                utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
                time.sleep(1)
            else:
                utils.print_colored("[!] Failed to delete traveller data.", "red")
                time.sleep(1)

        else:
            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
            time.sleep(1)
    else:
        utils.print_colored("[!] traveller not found.", "red")
        time.sleep(1.5)
        utils.remove_last_line()
        utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
        time.sleep(1)


def search_traveller(user):
    utils.clear_screen()
    print("\n=== Search Traveller data ===")
    print("Press 'q' to return to the Scooter data Menu.")
    while True:
        search_key = input("Enter Search Key: ").strip()
        if search_key == "q":
            utils.print_colored("[↩] Returning to Scooter data Menu...\n", "blue")
            time.sleep(1)
            return
        if search_key.isdigit():
            traveller_data = t.get_travellers(search_key)
            break
        elif search_key.isalpha():
            traveller_data = t.get_travellers(search_key)
            break
        elif search_key == "":
            utils.print_colored("[!] Search Key cannot be empty.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            continue
        elif search_key.__contains__("-", ",", ":",";", "{", "}", "[", "]", "(", ")", "/"):
            utils.print_colored("[!] Invalid input.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            log.add_log({
                "username": user['username'],
                "activity": "Search Traveller",
                "additional_info": f"Failed search with Search Key: {search_key}",
                "suspicious": 1
            })
        else:
            utils.print_colored("[!] Invalid input.", "red")
            time.sleep(1.5)
            utils.remove_last_line()
            continue
    
    if traveller_data:
        log.add_log({
            "username": user['username'],
            "activity": "Search Traveller",
            "additional_info": f"Searched for traveller with Search Key: {search_key}",
            "suspicious": 0
        })
        view_travellers(traveller_data)
    else:
        utils.print_colored("[!] Traveller not found.", "red")
        time.sleep(1.5)
        utils.remove_last_line()
    
    utils.print_colored("[↩] Returning to Traveller data Menu...\n", "blue")
    time.sleep(1)