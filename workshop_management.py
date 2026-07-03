class Workshop:
    def __init__(self):
        self.workshops = []

    def find_workshop(self, wid):
        for w in self.workshops:
            if w["id"] == wid:
                return w
        return None

    def add_workshop(self):
        wid = input("Enter Workshop ID: ")
        name = input("Workshop Name: ")
        date = input("Date (DD/MM/YYYY): ")
        venue = input("Venue: ")
        instructor = input("Instructor Name: ")
        dept = input("Department: ")

        while True:
            try:
                capacity = int(input("Capacity: "))
                if capacity > 0:
                    break
                print("Capacity must be at least 1.")
            except ValueError:
                print("Please enter a whole number.")

        while True:
            try:
                fee = float(input("Fee (0 = Free): "))
                if fee >= 0:
                    break
                print("Fee cannot be negative.")
            except ValueError:
                print("Please enter a valid number.")

        new_workshop = {
            "id": wid,
            "name": name,
            "date": date,
            "venue": venue,
            "instructor": instructor,
            "department": dept,
            "capacity": capacity,
            "fee": fee,
            "enrolled": 0,
            "status": "Upcoming"
        }

        self.workshops.append(new_workshop)
        print("Workshop Added Successfully")

    def view_workshops(self):
        if len(self.workshops) == 0:
            print("No workshops available")
        else:
            for w in self.workshops:
                if w["fee"] == 0:
                    fee_str = "Free"
                else:
                    fee_str = "Rs." + str(w["fee"])
                seats_left = w["capacity"] - w["enrolled"]
                print("\nWorkshop ID :", w["id"])
                print("Name        :", w["name"])
                print("Date        :", w["date"])
                print("Venue       :", w["venue"])
                print("Instructor  :", w["instructor"], "| Dept:", w["department"])
                print("Seats       :", seats_left, "left out of", w["capacity"])
                print("Fee         :", fee_str)
                print("Status      :", w["status"])

    def update_status(self):
        wid = input("Enter Workshop ID: ")
        w = self.find_workshop(wid)

        if w is not None:
            print("Current Status:", w["status"])
            print("1. Upcoming")
            print("2. Ongoing")
            print("3. Completed")
            print("4. Cancelled")
            choice = input("Choose new status: ")

            if choice == "1":
                w["status"] = "Upcoming"
            elif choice == "2":
                w["status"] = "Ongoing"
            elif choice == "3":
                w["status"] = "Completed"
            elif choice == "4":
                w["status"] = "Cancelled"
            else:
                print("Invalid Choice")
                return

            print("Status updated to:", w["status"])
        else:
            print("Workshop Not Found")

    def delete_workshop(self):
        wid = input("Enter Workshop ID: ")
        w = self.find_workshop(wid)

        if w is not None:
            confirm = input("Are you sure you want to delete this workshop? (yes/no): ")
            if confirm.lower() == "yes":
                self.workshops.remove(w)
                print("Workshop Deleted")
            else:
                print("Deletion Cancelled")
        else:
            print("Workshop Not Found")


class User:
    def __init__(self):
        self.users = []

    def find_user(self, uid):
        for p in self.users:
            if p["id"] == uid:
                return p
        return None

    def register(self, workshop):
        uid = input("Enter Participant ID: ")
        name = input("Full Name: ")
        email = input("Email: ")
        roll_no = input("Roll / Student ID: ")
        dept = input("Department: ")
        year = input("Year / Semester: ")
        wid = input("Enter Workshop ID: ")

        w = workshop.find_workshop(wid)

        if w is None:
            print("Workshop Not Found")
            return

        if w["status"] != "Upcoming" and w["status"] != "Ongoing":
            print("Registration is closed for this workshop")
            return

        if w["enrolled"] >= w["capacity"]:
            print("Sorry, this workshop is full")
            return

        for p in self.users:
            if p["email"] == email and p["workshop"] == wid and p["status"] == "Registered":
                print("You have already registered for this workshop")
                return

        new_user = {
            "id": uid,
            "name": name,
            "email": email,
            "roll_no": roll_no,
            "department": dept,
            "year": year,
            "workshop": wid,
            "payment": "Pending",
            "attendance": "Absent",
            "status": "Registered",
            "score": None,
            "grade": "Not Assigned",
            "result": "Not Assigned",
            "certificate": "Not Generated"
        }

        self.users.append(new_user)
        w["enrolled"] += 1
        print("Registration Confirmed")
        if w["fee"] > 0:
            print("Fee due: Rs." + str(w["fee"]) + " | Payment: Pending")

    def search(self):
        print("Search by:")
        print("1. Name")
        print("2. Roll Number")
        print("3. Email")
        print("4. Workshop ID")
        print("5. Department")
        choice = input("Choose: ")

        results = []

        if choice == "1":
            keyword = input("Enter Name: ").lower()
            for p in self.users:
                if keyword in p["name"].lower():
                    results.append(p)
        elif choice == "2":
            keyword = input("Enter Roll Number: ").lower()
            for p in self.users:
                if keyword in p["roll_no"].lower():
                    results.append(p)
        elif choice == "3":
            keyword = input("Enter Email: ").lower()
            for p in self.users:
                if keyword in p["email"].lower():
                    results.append(p)
        elif choice == "4":
            keyword = input("Enter Workshop ID: ")
            for p in self.users:
                if p["workshop"] == keyword:
                    results.append(p)
        elif choice == "5":
            keyword = input("Enter Department: ").lower()
            for p in self.users:
                if keyword in p["department"].lower():
                    results.append(p)
        else:
            print("Invalid Choice")
            return

        if len(results) == 0:
            print("No participants found")
            return

        print(len(results), "result(s) found:")
        for p in results:
            print("\nParticipant ID :", p["id"])
            print("Name           :", p["name"])
            print("Email          :", p["email"])
            print("Roll No        :", p["roll_no"])
            print("Workshop       :", p["workshop"])
            print("Status         :", p["status"])

    def cancel_registration(self, workshop):
        uid = input("Enter Participant ID to cancel: ")
        p = self.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p["status"] == "Cancelled":
            print("This registration is already cancelled")
            return

        confirm = input("Cancel registration for " + p["name"] + "? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancellation Aborted")
            return

        p["status"] = "Cancelled"
        w = workshop.find_workshop(p["workshop"])
        if w is not None and w["enrolled"] > 0:
            w["enrolled"] -= 1
        print("Registration Cancelled")

    def view_grades(self):
        uid = input("Enter Participant ID: ")
        p = self.find_user(uid)

        if p is not None:
            print("Grade:", p["grade"])
            print("Result:", p["result"])
        else:
            print("Participant Not Found")

    def print_certificate(self):
        uid = input("Enter Participant ID: ")
        p = self.find_user(uid)

        if p is not None:
            if p["certificate"] != "Not Generated":
                print("\n----- CERTIFICATE -----")
                print("Certificate of Completion")
                print("Presented to", p["name"])
                print("Workshop ID:", p["workshop"])
                print("Grade:", p["grade"])
                print("Certificate ID:", p["certificate"])
            else:
                print("Certificate Not Generated")
        else:
            print("Participant Not Found")

    def verify_certificate(self):
        cert_id = input("Enter Certificate ID: ")

        for p in self.users:
            if p["certificate"] == cert_id:
                print("Certificate Verified")
                print("Issued to:", p["name"])
                print("Grade:", p["grade"])
                return

        print("Certificate Invalid")


class WorkshopManagement:
    def view_participants(self, workshop, user):
        wid = input("Enter Workshop ID: ")
        w = workshop.find_workshop(wid)

        if w is not None:
            print("\nParticipants:")
            found_any = False
            for p in user.users:
                if p["workshop"] == wid:
                    print(p["id"], "-", p["name"], "|", p["status"])
                    found_any = True
            if not found_any:
                print("No participants yet")
        else:
            print("Workshop Not Found")

    def update_payment_status(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is not None:
            print("Current Payment:", p["payment"])
            print("1. Paid")
            print("2. Pending")
            print("3. Waived")
            choice = input("Choose: ")

            if choice == "1":
                p["payment"] = "Paid"
            elif choice == "2":
                p["payment"] = "Pending"
            elif choice == "3":
                p["payment"] = "Waived"
            else:
                print("Invalid Choice")
                return

            print("Payment Status Updated")
        else:
            print("Participant Not Found")

    def mark_attendance(self, workshop, user):
        wid = input("Enter Workshop ID: ")
        w = workshop.find_workshop(wid)

        if w is None:
            print("Workshop Not Found")
            return

        roster = []
        for p in user.users:
            if p["workshop"] == wid and p["status"] == "Registered":
                roster.append(p)

        if len(roster) == 0:
            print("No registered participants for this workshop")
            return

        for p in roster:
            print("\n" + p["name"], "- Current:", p["attendance"])
            print("1. Present")
            print("2. Absent")
            choice = input("Mark: ")
            if choice == "1":
                p["attendance"] = "Present"
            elif choice == "2":
                p["attendance"] = "Absent"
            else:
                print("Skipped")

        print("Attendance Updated")

    def add_update_grades(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p["attendance"] != "Present":
            print("Participant must attend the workshop first")
            return

        while True:
            try:
                score = float(input("Score (0-100): "))
                if 0 <= score <= 100:
                    break
                print("Enter a number between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

        if score >= 90:
            grade = "A+"
        elif score >= 80:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 50:
            grade = "D"
        else:
            grade = "F"

        if score >= 50:
            result = "Pass"
        else:
            result = "Fail"

        p["score"] = score
        p["grade"] = grade
        p["result"] = result
        print("Grade Saved:", grade, "(" + result + ")")

    def generate_certificate(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p["result"] != "Pass":
            print("Certificate can only be generated for participants who passed")
            return

        cert_id = "CERT-" + p["workshop"] + "-" + p["id"]
        p["certificate"] = cert_id
        print("Certificate Generated:", cert_id)

    def view_certificates(self, user):
        found_any = False
        for p in user.users:
            if p["certificate"] != "Not Generated":
                print(p["certificate"], "-", p["name"])
                found_any = True
        if not found_any:
            print("No certificates issued yet")

    def save_data(self, workshop, user):
        file1 = open("workshops.txt", "w")
        file1.write("===== WORKSHOPS DATABASE =====\n\n")
        for w in workshop.workshops:
            file1.write("Workshop ID : " + w["id"] + "\n")
            file1.write("Name        : " + w["name"] + "\n")
            file1.write("Date        : " + w["date"] + "\n")
            file1.write("Venue       : " + w["venue"] + "\n")
            file1.write("Instructor  : " + w["instructor"] + "\n")
            file1.write("Department  : " + w["department"] + "\n")
            file1.write("Capacity    : " + str(w["capacity"]) + "\n")
            file1.write("Enrolled    : " + str(w["enrolled"]) + "\n")
            file1.write("Fee         : " + str(w["fee"]) + "\n")
            file1.write("Status      : " + w["status"] + "\n")
            file1.write("-" * 40 + "\n\n")
        file1.close()

        file2 = open("participants.txt", "w")
        file2.write("===== PARTICIPANTS DATABASE =====\n\n")
        for p in user.users:
            file2.write("Participant ID : " + p["id"] + "\n")
            file2.write("Name           : " + p["name"] + "\n")
            file2.write("Email          : " + p["email"] + "\n")
            file2.write("Roll No        : " + p["roll_no"] + "\n")
            file2.write("Department     : " + p["department"] + "\n")
            file2.write("Workshop       : " + p["workshop"] + "\n")
            file2.write("Payment        : " + p["payment"] + "\n")
            file2.write("Attendance     : " + p["attendance"] + "\n")
            file2.write("Status         : " + p["status"] + "\n")
            file2.write("Grade          : " + p["grade"] + "\n")
            file2.write("Result         : " + p["result"] + "\n")
            file2.write("Certificate    : " + p["certificate"] + "\n")
            file2.write("-" * 40 + "\n\n")
        file2.close()

        print("Data Saved Successfully")

    def load_data(self, workshop, user):
        try:
            file1 = open("workshops.txt", "r")
            lines = file1.readlines()
            file1.close()

            current = {}
            for line in lines:
                line = line.strip()
                if line.startswith("Workshop ID"):
                    current["id"] = line.split(":", 1)[1].strip()
                elif line.startswith("Name"):
                    current["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("Date"):
                    current["date"] = line.split(":", 1)[1].strip()
                elif line.startswith("Venue"):
                    current["venue"] = line.split(":", 1)[1].strip()
                elif line.startswith("Instructor"):
                    current["instructor"] = line.split(":", 1)[1].strip()
                elif line.startswith("Department"):
                    current["department"] = line.split(":", 1)[1].strip()
                elif line.startswith("Capacity"):
                    current["capacity"] = int(line.split(":", 1)[1].strip())
                elif line.startswith("Enrolled"):
                    current["enrolled"] = int(line.split(":", 1)[1].strip())
                elif line.startswith("Fee"):
                    current["fee"] = float(line.split(":", 1)[1].strip())
                elif line.startswith("Status"):
                    current["status"] = line.split(":", 1)[1].strip()
                elif line.startswith("---"):
                    if len(current) > 0:
                        workshop.workshops.append(current)
                        current = {}

            print("Workshops loaded:", len(workshop.workshops))
        except FileNotFoundError:
            print("No saved workshops found. Starting fresh.")

        try:
            file2 = open("participants.txt", "r")
            lines = file2.readlines()
            file2.close()

            current = {}
            for line in lines:
                line = line.strip()
                if line.startswith("Participant ID"):
                    current["id"] = line.split(":", 1)[1].strip()
                elif line.startswith("Name"):
                    current["name"] = line.split(":", 1)[1].strip()
                elif line.startswith("Email"):
                    current["email"] = line.split(":", 1)[1].strip()
                elif line.startswith("Roll No"):
                    current["roll_no"] = line.split(":", 1)[1].strip()
                elif line.startswith("Department"):
                    current["department"] = line.split(":", 1)[1].strip()
                elif line.startswith("Workshop"):
                    current["workshop"] = line.split(":", 1)[1].strip()
                elif line.startswith("Payment"):
                    current["payment"] = line.split(":", 1)[1].strip()
                elif line.startswith("Attendance"):
                    current["attendance"] = line.split(":", 1)[1].strip()
                elif line.startswith("Status"):
                    current["status"] = line.split(":", 1)[1].strip()
                elif line.startswith("Grade"):
                    current["grade"] = line.split(":", 1)[1].strip()
                elif line.startswith("Result"):
                    current["result"] = line.split(":", 1)[1].strip()
                elif line.startswith("Certificate"):
                    current["certificate"] = line.split(":", 1)[1].strip()
                elif line.startswith("---"):
                    if len(current) > 0:
                        current["score"] = None
                        user.users.append(current)
                        current = {}

            print("Participants loaded:", len(user.users))
        except FileNotFoundError:
            print("No saved participants found. Starting fresh.")


class Report:
    def summary(self, workshop, user):
        print("\n----- SUMMARY -----")
        print("Total Workshops:", len(workshop.workshops))
        print("Total Participants:", len(user.users))

        if len(workshop.workshops) > 0:
            upcoming = 0
            ongoing = 0
            completed = 0
            cancelled = 0
            for w in workshop.workshops:
                if w["status"] == "Upcoming":
                    upcoming += 1
                elif w["status"] == "Ongoing":
                    ongoing += 1
                elif w["status"] == "Completed":
                    completed += 1
                elif w["status"] == "Cancelled":
                    cancelled += 1
            print("\nWorkshop Status:")
            print("Upcoming :", upcoming)
            print("Ongoing  :", ongoing)
            print("Completed:", completed)
            print("Cancelled:", cancelled)

        if len(user.users) > 0:
            registered = 0
            cancelled = 0
            paid = 0
            present = 0
            passed = 0
            failed = 0
            for p in user.users:
                if p["status"] == "Registered":
                    registered += 1
                elif p["status"] == "Cancelled":
                    cancelled += 1
                if p["payment"] == "Paid":
                    paid += 1
                if p["attendance"] == "Present":
                    present += 1
                if p["result"] == "Pass":
                    passed += 1
                elif p["result"] == "Fail":
                    failed += 1
            print("\nParticipant Status:")
            print("Registered:", registered)
            print("Cancelled :", cancelled)
            print("Paid      :", paid)
            print("Present   :", present)
            print("Passed    :", passed)
            print("Failed    :", failed)


workshop = Workshop()
user = User()
management = WorkshopManagement()
report = Report()

print("Loading saved data...")
management.load_data(workshop, user)

while True:
    print("\n===== WORKSHOP MANAGEMENT SYSTEM =====")
    print("1. Organizer")
    print("2. Participant")
    print("3. Exit")

    main_choice = int(input("Enter Choice: "))

    if main_choice == 1:

        while True:
            print("\n===== ORGANIZER MENU =====")
            print("1. Add Workshop")
            print("2. View Workshops")
            print("3. Update Workshop Status")
            print("4. Delete Workshop")
            print("5. View Participants")
            print("6. Search Participant")
            print("7. Update Payment Status")
            print("8. Mark Attendance")
            print("9. Cancel Registration")
            print("10. Add/Update Grades")
            print("11. Generate Certificate")
            print("12. View Certificates")
            print("13. Summary")
            print("14. Save Data")
            print("15. Back")

            choice = int(input("Enter Choice: "))

            if choice == 1:
                workshop.add_workshop()

            elif choice == 2:
                workshop.view_workshops()

            elif choice == 3:
                workshop.update_status()

            elif choice == 4:
                workshop.delete_workshop()

            elif choice == 5:
                management.view_participants(workshop, user)

            elif choice == 6:
                user.search()

            elif choice == 7:
                management.update_payment_status(user)

            elif choice == 8:
                management.mark_attendance(workshop, user)

            elif choice == 9:
                user.cancel_registration(workshop)

            elif choice == 10:
                management.add_update_grades(user)

            elif choice == 11:
                management.generate_certificate(user)

            elif choice == 12:
                management.view_certificates(user)

            elif choice == 13:
                report.summary(workshop, user)

            elif choice == 14:
                management.save_data(workshop, user)

            elif choice == 15:
                break

            else:
                print("Invalid Choice")

    elif main_choice == 2:

        while True:
            print("\n===== PARTICIPANT MENU =====")
            print("1. View Workshops")
            print("2. Register for Workshop")
            print("3. View Grades")
            print("4. Print Certificate")
            print("5. Verify Certificate")
            print("6. Back")

            choice = int(input("Enter Choice: "))

            if choice == 1:
                workshop.view_workshops()

            elif choice == 2:
                user.register(workshop)

            elif choice == 3:
                user.view_grades()

            elif choice == 4:
                user.print_certificate()

            elif choice == 5:
                user.verify_certificate()

            elif choice == 6:
                break

            else:
                print("Invalid Choice")

    elif main_choice == 3:
        print("Thank You")
        break

    else:
        print("Invalid Choice")
