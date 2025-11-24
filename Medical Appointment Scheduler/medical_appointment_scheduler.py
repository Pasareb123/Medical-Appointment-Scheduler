

import json
from datetime import datetime
import os

FILE_NAME = "clinic_data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except:
            return {"patients": {}, "appointments": []}
    else:
        return {"patients": {}, "appointments": []}

def save_data(info):
    with open(FILE_NAME, "w") as f:
        json.dump(info, f)

class Patients:
    def __init__(self, storage):
        self.storage = storage

    def add(self, pid, name, age, phone):
        if pid in self.storage["patients"]:
            print("ID already used.")
            return
        self.storage["patients"][pid] = {
            "name": name,
            "age": age,
            "phone": phone
        }
        save_data(self.storage)
        print("Patient saved.")

    def show(self):
        pats = self.storage["patients"]
        if len(pats) == 0:
            print("No patients yet.")
            return
        for pid, data in pats.items():
            print(pid, data["name"], data["age"], data["phone"])

    def exists(self, pid):
        return pid in self.storage["patients"]

class Appointments:
    def __init__(self, storage):
        self.storage = storage

    def add(self, pid, date, time, reason):
        self.storage["appointments"].append({
            "pid": pid,
            "date": date,
            "time": time,
            "reason": reason
        })
        save_data(self.storage)
        print("Appointment added.")

    def show(self):
        appts = self.storage["appointments"]
        if len(appts) == 0:
            print("No appointments.")
            return
        for a in appts:
            p = self.storage["patients"].get(a["pid"], {})
            print(p.get("name", "Unknown"), a["date"], a["time"], a["reason"])

    def today_reminders(self):
        today = datetime.now().strftime("%Y-%m-%d")
        sent = False
        for a in self.storage["appointments"]:
            if a["date"] == today:
                p = self.storage["patients"][a["pid"]]
                print("Reminder:", p["name"], "has an appointment today.")
                sent = True
        if not sent:
            print("No reminders for today.")

class ClinicSystem:
    def __init__(self):
        self.data = load_data()
        self.pats = Patients(self.data)
        self.apts = Appointments(self.data)

    def run(self):
        while True:
            print("\n1 Add Patient\n2 View Patients\n3 Add Appointment\n4 View Appointments\n5 Today Reminders\n6 Exit")
            choice = input("Pick: ")

            if choice == "1":
                pid = input("ID: ")
                name = input("Name: ")
                age = int(input("Age: "))
                phone = input("Phone: ")
                self.pats.add(pid, name, age, phone)

            elif choice == "2":
                self.pats.show()

            elif choice == "3":
                pid = input("Patient ID: ")
                if not self.pats.exists(pid):
                    print("Patient not found.")
                    continue
                date = input("Date (YYYY-MM-DD): ")
                time = input("Time (HH:MM): ")
                reason = input("Reason: ")
                self.apts.add(pid, date, time, reason)

            elif choice == "4":
                self.apts.show()

            elif choice == "5":
                self.apts.today_reminders()

            elif choice == "6":
                break

            else:
                print("Invalid choice.")

if __name__ == "__main__":
    ClinicSystem().run()
