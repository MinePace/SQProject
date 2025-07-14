import utils.utils as utils
import models.log as l
import time

def show_logs(user):
    if user["role"] not in ["system_admin", "super_admin", "System Administrator", "Super Administrator"]:
        utils.print_colored("[!] ACCESS DENIED", "red")
        time.sleep(1.5)
        return

    while True:
        utils.clear_screen()
        print("\n=== Log Data ===")

        logs = l.get_logs()
        if not logs:
            utils.print_colored("[!] No logs found.", "red")
            time.sleep(1.5)
            return

        print(f"| {'Date':<10} | {'Time':<8} | {'User':<16} | {'Activity':<19} | {'Additional Info':<50} | Suspicious")
        print("-" * 127)

        for log in logs:
            print(f"| {log['date']:<10} | {log['time']:<8} | {log['username']:<16} | {log['activity']:<19} | {log['additional_info']:<50} | {log['suspicious']}")

        input("\nPress any key to go back...")
        utils.print_colored("[↩] Returning to Traveller data Menu...", "blue")
        time.sleep(1)
        return
