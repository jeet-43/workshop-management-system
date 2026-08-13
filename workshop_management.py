import pickle
import os
from datetime import datetime


class WorkshopItem:
    def __init__(self, wid, name, date, venue, instructor, dept, capacity, fee):
        self.id = wid
        self.name = name
        self.date = date
        self.venue = venue
        self.instructor = instructor
        self.department = dept
        self.capacity = capacity
        self.fee = fee
        self.enrolled = 0
        self.status = "Upcoming"


class Participant:
    def __init__(self, uid, name, email, password, roll_no, dept, year, workshop_id, reg_date):
        self.id = uid
        self.name = name
        self.email = email
        self.password = password
        self.roll_no = roll_no
        self.department = dept
        self.year = year
        self.workshop = workshop_id
        self.registration_date = reg_date
        self.payment = "Pending"
        self.payment_date = None
        self.attendance = "Absent"
        self.attendance_date = None
        self.status = "Registered"
        self.score = None
        self.grade = "Not Assigned"
        self.result = "Not Assigned"
        self.certificate = "Not Generated"


class AttendanceRecord:
    def __init__(self, participant_id, workshop_id, attendance, date):
        self.participant_id = participant_id
        self.workshop_id = workshop_id
        self.attendance = attendance
        self.date = date


class Transaction:
    def __init__(self, participant_id, workshop_id, fee, payment_status, date):
        self.participant_id = participant_id
        self.workshop_id = workshop_id
        self.fee = fee
        self.payment_status = payment_status
        self.date = date


def match_date(date_str, choice, year=None, month=None, day=None):
    if not date_str:
        return False

    parts = date_str.split("/")
    if len(parts) != 3:
        return False

    d, m, y = parts[0].zfill(2), parts[1].zfill(2), parts[2]

    if choice == "1":
        return y == year
    elif choice == "2":
        return m == month and y == year
    elif choice == "3":
        return d == day and m == month and y == year
    return False


def date_choice():
    
    print("1. Year only (e.g. 2026)")
    print("2. Month & Year (e.g. 08/2026)")
    print("3. Full Date (DD/MM/YYYY)")
    choice = input("Choose: ")

    if choice == "1":
        year = input("Enter Year (YYYY): ").strip()
        return choice, year, None, None

    elif choice == "2":
        my = input("Enter Month & Year (MM/YYYY): ").strip()
        my_parts = my.split("/")
        if len(my_parts) != 2:
            print("Invalid format. Please use MM/YYYY.")
            return None
        month, year = my_parts[0].zfill(2), my_parts[1]
        return choice, year, month, None

    elif choice == "3":
        full_date = input("Enter Full Date (DD/MM/YYYY): ").strip()
        fd_parts = full_date.split("/")
        if len(fd_parts) != 3:
            print("Invalid format. Please use DD/MM/YYYY.")
            return None
        day, month, year = fd_parts[0].zfill(2), fd_parts[1].zfill(2), fd_parts[2]
        return choice, year, month, day

    else:
        print("Invalid Choice")
        return None


class Workshop:
    def __init__(self):
        self.workshops = []

    def find_workshop(self, wid):
        for w in self.workshops:
            if w.id == wid:
                return w
        return None

    def generate_workshop_id(self):
        today = datetime.now().strftime("%Y%m%d")
        count = 0
        for w in self.workshops:
            if w.id.startswith(today + "-"):
                count += 1
        count += 1
        return today + "-" + str(count).zfill(3)

    def add_workshop(self):
        wid = self.generate_workshop_id()
        print("Workshop ID (auto-generated):", wid)
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

        new_workshop = WorkshopItem(wid, name, date, venue, instructor, dept, capacity, fee)
        self.workshops.append(new_workshop)
        print("Workshop Added Successfully. Workshop ID:", wid)

    def view_workshops(self):
        if len(self.workshops) == 0:
            print("No workshops available")
        else:
            self._print_workshop_list(self.workshops)

    def _print_workshop_list(self, workshops):
        for w in workshops:
            if w.fee == 0:
                fee_str = "Free"
            else:
                fee_str = "Rs." + str(w.fee)
            seats_left = w.capacity - w.enrolled
            print("\nWorkshop ID :", w.id)
            print("Name        :", w.name)
            print("Date        :", w.date)
            print("Venue       :", w.venue)
            print("Instructor  :", w.instructor, "| Dept:", w.department)
            print("Seats       :", seats_left, "left out of", w.capacity)
            print("Fee         :", fee_str)
            print("Status      :", w.status)

    def search(self):
        print("\n----- Search Workshops -----")
        print("Leave any field blank to skip that filter.\n")

        wid = input("Workshop ID (optional): ").strip()
        name = input("Workshop Name (optional): ").strip().lower()
        instructor = input("Instructor Name (optional): ").strip().lower()
        dept = input("Department (optional): ").strip().lower()
        venue = input("Venue (optional): ").strip().lower()

        print("\nStatus (optional):")
        print("1. Upcoming")
        print("2. Ongoing")
        print("3. Completed")
        print("4. Cancelled")
        print("Leave blank for any status")
        status_choice = input("Choose: ").strip()
        status_map = {"1": "Upcoming", "2": "Ongoing", "3": "Completed", "4": "Cancelled"}
        status = status_map.get(status_choice)

        date_filter = None
        use_date = input("\nFilter by Date too? (yes/no): ").strip().lower()
        if use_date == "yes":
            parsed = date_choice()
            if parsed is not None:
                date_filter = parsed

        results = []
        for w in self.workshops:
            if wid and w.id != wid:
                continue
            if name and name not in w.name.lower():
                continue
            if instructor and instructor not in w.instructor.lower():
                continue
            if dept and dept not in w.department.lower():
                continue
            if venue and venue not in w.venue.lower():
                continue
            if status and w.status != status:
                continue
            if date_filter is not None:
                d_choice, d_year, d_month, d_day = date_filter
                if not match_date(w.date, d_choice, d_year, d_month, d_day):
                    continue
            results.append(w)

        if len(results) == 0:
            print("No workshops found matching the given criteria")
            return

        print(len(results), "workshop(s) found:")
        self._print_workshop_list(results)

    def update_status(self):
        wid = input("Enter Workshop ID: ")
        w = self.find_workshop(wid)

        if w is not None:
            print("Current Status:", w.status)
            print("1. Upcoming")
            print("2. Ongoing")
            print("3. Completed")
            print("4. Cancelled")
            choice = input("Choose new status: ")

            if choice == "1":
                w.status = "Upcoming"
            elif choice == "2":
                w.status = "Ongoing"
            elif choice == "3":
                w.status = "Completed"
            elif choice == "4":
                w.status = "Cancelled"
            else:
                print("Invalid Choice")
                return

            print("Status updated to:", w.status)
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
            if p.id == uid:
                return p
        return None

    def authenticate(self, email, password):
        for p in self.users:
            if p.email == email and p.password == password:
                return p
        return None

    def generate_participant_id(self):
        max_num = 0
        for p in self.users:
            if p.id.startswith("U") and p.id[1:].isdigit():
                num = int(p.id[1:])
                if num > max_num:
                    max_num = num
        return "U" + str(max_num + 1).zfill(3)

    def register(self, workshop):
        uid = self.generate_participant_id()
        print("Participant ID (auto-generated):", uid)
        name = input("Full Name: ")
        email = input("Email: ")

        while True:
            password = input("Create Password: ")
            if len(password.strip()) == 0:
                print("Password cannot be empty.")
                continue
            confirm_password = input("Confirm Password: ")
            if password != confirm_password:
                print("Passwords do not match. Try again.")
                continue
            break

        roll_no = input("Roll / Student ID: ")
        dept = input("Department: ")
        year = input("Year / Semester: ")
        wid = input("Enter Workshop ID: ")

        w = workshop.find_workshop(wid)

        if w is None:
            print("Workshop Not Found")
            return

        if w.status != "Upcoming" and w.status != "Ongoing":
            print("Registration is closed for this workshop")
            return

        if w.enrolled >= w.capacity:
            print("Sorry, this workshop is full")
            return

        for p in self.users:
            if p.email == email and p.workshop == wid and p.status == "Registered":
                print("You have already registered for this workshop")
                return

        reg_date = datetime.now().strftime("%d/%m/%Y")
        new_user = Participant(uid, name, email, password, roll_no, dept, year, wid, reg_date)
        self.users.append(new_user)
        w.enrolled += 1
        print("Registration Confirmed. Participant ID:", uid)
        print("Registration Date:", reg_date)
        if w.fee > 0:
            print("Fee due: Rs." + str(w.fee) + " | Payment: Pending")

    def _print_participant_list(self, results):
        for p in results:
            print("\nParticipant ID :", p.id)
            print("Name           :", p.name)
            print("Email          :", p.email)
            print("Roll No        :", p.roll_no)
            print("Workshop       :", p.workshop)
            print("Reg. Date      :", p.registration_date)
            print("Attendance     :", p.attendance, "| Date:", p.attendance_date)
            print("Payment        :", p.payment, "| Date:", p.payment_date)
            print("Status         :", p.status)

    def search(self):
        print("\n----- Search Participants -----")
        print("Leave any field blank to skip that filter.\n")

        name = input("Name (optional): ").strip().lower()
        roll_no = input("Roll Number (optional): ").strip().lower()
        email = input("Email (optional): ").strip().lower()
        dept = input("Department (optional): ").strip().lower()
        wid = input("Workshop ID (optional): ").strip()

        print("\nStatus (optional):")
        print("1. Registered")
        print("2. Cancelled")
        print("Leave blank for any status")
        status_choice = input("Choose: ").strip()
        status_map = {"1": "Registered", "2": "Cancelled"}
        status = status_map.get(status_choice)

        print("\nPayment (optional):")
        print("1. Paid")
        print("2. Pending")
        print("3. Waived")
        print("Leave blank for any payment status")
        payment_choice = input("Choose: ").strip()
        payment_map = {"1": "Paid", "2": "Pending", "3": "Waived"}
        payment = payment_map.get(payment_choice)

        print("\nAttendance (optional):")
        print("1. Present")
        print("2. Absent")
        print("Leave blank for any attendance")
        attendance_choice = input("Choose: ").strip()
        attendance_map = {"1": "Present", "2": "Absent"}
        attendance = attendance_map.get(attendance_choice)

        date_filter = None
        use_date = input("\nFilter by Date too? (yes/no): ").strip().lower()
        if use_date == "yes":
            print("\nWhich date field?")
            print("1. Registration Date")
            print("2. Attendance Date")
            print("3. Payment Date")
            field_choice = input("Choose: ").strip()
            date_field_map = {
                "1": lambda p: p.registration_date,
                "2": lambda p: p.attendance_date,
                "3": lambda p: p.payment_date,
            }
            get_date = date_field_map.get(field_choice)
            if get_date is not None:
                parsed = date_choice()
                if parsed is not None:
                    date_filter = (get_date, parsed)
            else:
                print("Invalid Choice. Skipping date filter.")

        results = []
        for p in self.users:
            if name and name not in p.name.lower():
                continue
            if roll_no and roll_no not in p.roll_no.lower():
                continue
            if email and email not in p.email.lower():
                continue
            if dept and dept not in p.department.lower():
                continue
            if wid and p.workshop != wid:
                continue
            if status and p.status != status:
                continue
            if payment and p.payment != payment:
                continue
            if attendance and p.attendance != attendance:
                continue
            if date_filter is not None:
                get_date, (d_choice, d_year, d_month, d_day) = date_filter
                if not match_date(get_date(p), d_choice, d_year, d_month, d_day):
                    continue
            results.append(p)

        if len(results) == 0:
            print("No participants found matching the given criteria")
            return

        print(len(results), "participant(s) found:")
        self._print_participant_list(results)

    def cancel_registration(self, workshop):
        uid = input("Enter Participant ID to cancel: ")
        p = self.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p.status == "Cancelled":
            print("This registration is already cancelled")
            return

        confirm = input("Cancel registration for " + p.name + "? (yes/no): ")
        if confirm.lower() != "yes":
            print("Cancellation Aborted")
            return

        p.status = "Cancelled"
        w = workshop.find_workshop(p.workshop)
        if w is not None and w.enrolled > 0:
            w.enrolled -= 1
        print("Registration Cancelled")

    def view_grades(self):
        email = input("Enter Registered Email: ")
        password = input("Enter Password: ")
        p = self.authenticate(email, password)

        if p is not None:
            print("Grade:", p.grade)
            print("Result:", p.result)
        else:
            print("Invalid Email or Password")

    def print_certificate(self):
        email = input("Enter Registered Email: ")
        password = input("Enter Password: ")
        p = self.authenticate(email, password)

        if p is not None:
            if p.certificate != "Not Generated":
                lines = [
                    "CERTIFICATE OF COMPLETION",
                    "",
                    "This is proudly presented to",
                    p.name.upper(),
                    "",
                    "for successfully completing Workshop " + p.workshop,
                    "Grade: " + p.grade,
                    "",
                    "Certificate ID: " + p.certificate,
                ]
                print_certificate_box(lines)
            else:
                print("Certificate Not Generated")
        else:
            print("Invalid Email or Password")

    def verify_certificate(self):
        cert_id = input("Enter Certificate ID: ")

        for p in self.users:
            if p.certificate == cert_id:
                lines = [
                    "CERTIFICATE VERIFIED",
                    "",
                    "Issued to: " + p.name,
                    "Workshop: " + p.workshop,
                    "Grade: " + p.grade,
                    "Certificate ID: " + cert_id,
                ]
                print_certificate_box(lines)
                return

        print("Certificate Invalid")


def print_star_square(size=7):
    for i in range(size):
        print("* " * size)


def print_certificate_box(lines, min_width=54, padding=2):
    content_width = max((len(line) for line in lines), default=0)
    width = max(min_width, content_width + padding * 2 + 2)

    star_flourish = ("* " * (width // 2 + 1))[:width]
    border_line = "*" * width
    blank_line = "*" + " " * (width - 2) + "*"

    print()
    print(star_flourish)
    print(border_line)
    print(blank_line)
    for line in lines:
        print("*" + line.center(width - 2) + "*")
    print(blank_line)
    print(border_line)
    print(star_flourish)
    print()


class WorkshopManagement:
    def view_participants(self, workshop, user):
        wid = input("Enter Workshop ID: ")
        w = workshop.find_workshop(wid)

        if w is not None:
            print("\nParticipants:")
            found_any = False
            for p in user.users:
                if p.workshop == wid:
                    print(p.id, "-", p.name, "|", p.email, "|", p.status, "| Reg:", p.registration_date)
                    found_any = True
            if not found_any:
                print("No participants yet")
        else:
            print("Workshop Not Found")

    def update_payment_status(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is not None:
            print("Current Payment:", p.payment)
            print("1. Paid")
            print("2. Pending")
            print("3. Waived")
            choice = input("Choose: ")

            if choice == "1":
                p.payment = "Paid"
            elif choice == "2":
                p.payment = "Pending"
            elif choice == "3":
                p.payment = "Waived"
            else:
                print("Invalid Choice")
                return

            p.payment_date = datetime.now().strftime("%d/%m/%Y")
            print("Payment Status Updated on", p.payment_date)
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
            if p.workshop == wid and p.status == "Registered":
                roster.append(p)

        if len(roster) == 0:
            print("No registered participants for this workshop")
            return

        today = datetime.now().strftime("%d/%m/%Y")
        for p in roster:
            print("\n" + p.name, "- Current:", p.attendance)
            print("1. Present")
            print("2. Absent")
            choice = input("Mark: ")
            if choice == "1":
                p.attendance = "Present"
                p.attendance_date = today
            elif choice == "2":
                p.attendance = "Absent"
                p.attendance_date = today
            else:
                print("Skipped")

        print("Attendance Updated")

    def add_update_grades(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p.attendance != "Present":
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

        p.score = score
        p.grade = grade
        p.result = result
        print("Grade Saved:", grade, "(" + result + ")")

        

    def generate_certificate(self, user):
        uid = input("Enter Participant ID: ")
        p = user.find_user(uid)

        if p is None:
            print("Participant Not Found")
            return

        if p.result != "Pass":
            print("Certificate can only be generated for participants who passed")
            return

        cert_id = "CERT-" + p.workshop + "-" + p.id
        p.certificate = cert_id

        lines = [
            "CERTIFICATE OF COMPLETION",
            "",
            "This is proudly presented to",
            p.name.upper(),
            "",
            "for successfully completing Workshop " + p.workshop,
            "Grade: " + p.grade,
            "",
            "Certificate ID: " + cert_id,
        ]
        print_certificate_box(lines)
        print("Certificate Generated Successfully!")

    def view_certificates(self, user):
        found_any = False
        for p in user.users:
            if p.certificate != "Not Generated":
                print(p.certificate, "-", p.name)
                found_any = True
        if not found_any:
            print("No certificates issued yet")


class DataManager:
    def __init__(self):
        self.workshop_file = "workshop.txt"
        self.participant_file = "participants.txt"
        self.attendance_file = "attendance.txt"
        self.transaction_file = "transaction.txt"

    def save_workshops(self, workshop):
        with open(self.workshop_file, "wb") as f:
            pickle.dump(workshop.workshops, f)

    def save_participants(self, user):
        with open(self.participant_file, "wb") as f:
            pickle.dump(user.users, f)

    def save_attendance(self, user):
        records = []
        for p in user.users:
            records.append(AttendanceRecord(p.id, p.workshop, p.attendance, p.attendance_date))
        with open(self.attendance_file, "wb") as f:
            pickle.dump(records, f)

    def save_transactions(self, user, workshop):
        records = []
        for p in user.users:
            w = workshop.find_workshop(p.workshop)
            fee = w.fee if w is not None else 0
            records.append(Transaction(p.id, p.workshop, fee, p.payment, p.payment_date))
        with open(self.transaction_file, "wb") as f:
            pickle.dump(records, f)

    def save_all(self, workshop, user):
        self.save_workshops(workshop)
        self.save_participants(user)
        self.save_attendance(user)
        self.save_transactions(user, workshop)
        print("Data Saved Successfully")
        print("(workshop.txt, participants.txt, attendance.txt, transaction.txt)")

    def load_workshops(self, workshop):
        if not os.path.exists(self.workshop_file):
            return False
        try:
            with open(self.workshop_file, "rb") as f:
                workshop.workshops = pickle.load(f)
            return True
        except (pickle.UnpicklingError, EOFError):
            print("workshop.txt is corrupted. Skipping workshop data.")
            return False

    def load_participants(self, user):
        if not os.path.exists(self.participant_file):
            return False
        try:
            with open(self.participant_file, "rb") as f:
                user.users = pickle.load(f)
            return True
        except (pickle.UnpicklingError, EOFError):
            print("participants.txt is corrupted. Skipping participant data.")
            return False

    def load_attendance(self, user):
        if not os.path.exists(self.attendance_file):
            return
        try:
            with open(self.attendance_file, "rb") as f:
                records = pickle.load(f)
            for rec in records:
                p = user.find_user(rec.participant_id)
                if p is not None:
                    p.attendance = rec.attendance
                    p.attendance_date = getattr(rec, "date", None)
        except (pickle.UnpicklingError, EOFError):
            print("attendance.txt is corrupted. Skipping attendance data.")

    def load_transactions(self, user):
        if not os.path.exists(self.transaction_file):
            return
        try:
            with open(self.transaction_file, "rb") as f:
                records = pickle.load(f)
            for rec in records:
                p = user.find_user(rec.participant_id)
                if p is not None:
                    p.payment = rec.payment_status
                    p.payment_date = getattr(rec, "date", None)
        except (pickle.UnpicklingError, EOFError):
            print("transaction.txt is corrupted. Skipping transaction data.")

    def load_all(self, workshop, user):
        loaded_workshops = self.load_workshops(workshop)
        loaded_participants = self.load_participants(user)

        if loaded_participants:
            self.load_attendance(user)
            self.load_transactions(user)

        if not loaded_workshops and not loaded_participants:
            print("No saved data found. Starting fresh.")
        else:
            print("Workshops loaded:", len(workshop.workshops))
            print("Participants loaded:", len(user.users))


class Report:
    def report_menu(self, workshop, user):
        while True:
            print("\n===== REPORTS =====")
            print("1. Workshops")
            print("2. Participants")
            print("3. Attendance")
            print("4. Transactions")
            print("5. Overview")
            print("6. Back")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.workshop_report(workshop)
            elif choice == "2":
                self.participant_report(user)
            elif choice == "3":
                self.attendance_report(user)
            elif choice == "4":
                self.transaction_report(user, workshop)
            elif choice == "5":
                self.overview(workshop, user)
            elif choice == "6":
                break
            else:
                print("Invalid Choice")

    def workshop_report(self, workshop):
        print("\n----- WORKSHOP REPORT -----")
        if len(workshop.workshops) == 0:
            print("No workshops available")
            return
        print("Total Workshops:", len(workshop.workshops))
        workshop._print_workshop_list(workshop.workshops)

    def participant_report(self, user):
        print("\n----- PARTICIPANT REPORT -----")
        if len(user.users) == 0:
            print("No participants available")
            return
        print("Total Participants:", len(user.users))
        user._print_participant_list(user.users)

    def attendance_report(self, user):
        print("\n----- ATTENDANCE REPORT -----")
        if len(user.users) == 0:
            print("No attendance records available")
            return

        present = sum(1 for p in user.users if p.attendance == "Present")
        absent = sum(1 for p in user.users if p.attendance == "Absent")
        print("Total Records:", len(user.users))
        print("Present     :", present)
        print("Absent      :", absent)

        for p in user.users:
            print("\nParticipant ID :", p.id)
            print("Name           :", p.name)
            print("Workshop ID    :", p.workshop)
            print("Attendance     :", p.attendance)
            print("Marked On      :", p.attendance_date)

    def transaction_report(self, user, workshop):
        print("\n----- TRANSACTION REPORT -----")
        if len(user.users) == 0:
            print("No transaction records available")
            return

        total_collected = 0.0
        paid = 0
        pending = 0
        waived = 0

        for p in user.users:
            w = workshop.find_workshop(p.workshop)
            fee = w.fee if w is not None else 0
            if p.payment == "Paid":
                paid += 1
                total_collected += fee
            elif p.payment == "Pending":
                pending += 1
            elif p.payment == "Waived":
                waived += 1

        print("Total Records    :", len(user.users))
        print("Paid             :", paid)
        print("Pending          :", pending)
        print("Waived           :", waived)
        print("Total Collected  : Rs." + str(total_collected))

        for p in user.users:
            w = workshop.find_workshop(p.workshop)
            fee = w.fee if w is not None else 0
            fee_str = "Free" if fee == 0 else "Rs." + str(fee)
            print("\nParticipant ID :", p.id)
            print("Name           :", p.name)
            print("Workshop ID    :", p.workshop)
            print("Fee            :", fee_str)
            print("Payment Status :", p.payment)
            print("Payment Date   :", p.payment_date)

    def overview(self, workshop, user):
        print("\n----- OVERVIEW -----")
        print("Total Workshops:", len(workshop.workshops))
        print("Total Participants:", len(user.users))

        if len(workshop.workshops) > 0:
            upcoming = 0
            ongoing = 0
            completed = 0
            cancelled = 0
            for w in workshop.workshops:
                if w.status == "Upcoming":
                    upcoming += 1
                elif w.status == "Ongoing":
                    ongoing += 1
                elif w.status == "Completed":
                    completed += 1
                elif w.status == "Cancelled":
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
                if p.status == "Registered":
                    registered += 1
                elif p.status == "Cancelled":
                    cancelled += 1
                if p.payment == "Paid":
                    paid += 1
                if p.attendance == "Present":
                    present += 1
                if p.result == "Pass":
                    passed += 1
                elif p.result == "Fail":
                    failed += 1
            print("\nParticipant Status:")
            print("Registered:", registered)
            print("Cancelled :", cancelled)
            print("Paid      :", paid)
            print("Present   :", present)
            print("Passed    :", passed)
            print("Failed    :", failed)


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin@123"

workshop = Workshop()
user = User()
management = WorkshopManagement()
report = Report()
data_manager = DataManager()
print("Loading saved data...")
data_manager.load_all(workshop, user)

while True:
    print("\n===== WORKSHOP MANAGEMENT SYSTEM =====")
    print("1. Admin")
    print("2. User")
    print("3. Exit")

    main_choice = int(input("Enter Choice: "))

    if main_choice == 1:

        login_success = False
        attempts = 3
        while attempts > 0:
            username = input("Admin Username: ")
            password = input("Admin Password: ")
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                login_success = True
                break
            attempts -= 1
            print("Invalid Username or Password. Attempts left:", attempts)

        if not login_success:
            print("Too many failed attempts. Returning to main menu.")
            continue

        while True:
            print("\n===== ADMIN MENU =====")
            print("1. Add Workshop")
            print("2. View Workshops")
            print("3. Search Workshop")
            print("4. Update Workshop Status")
            print("5. Delete Workshop")
            print("6. View Participants")
            print("7. Search Participant")
            print("8. Update Payment Status")
            print("9. Mark Attendance")
            print("10. Cancel Registration")
            print("11. Add/Update Grades")
            print("12. Generate Certificate")
            print("13. View Certificates")
            print("14. Report")
            print("15. Save Data")
            print("16. Back")

            choice = int(input("Enter Choice: "))

            if choice == 1:
                workshop.add_workshop()

            elif choice == 2:
                workshop.view_workshops()

            elif choice == 3:
                workshop.search()

            elif choice == 4:
                workshop.update_status()

            elif choice == 5:
                workshop.delete_workshop()

            elif choice == 6:
                management.view_participants(workshop, user)

            elif choice == 7:
                user.search()

            elif choice == 8:
                management.update_payment_status(user)

            elif choice == 9:
                management.mark_attendance(workshop, user)

            elif choice == 10:
                user.cancel_registration(workshop)

            elif choice == 11:
                management.add_update_grades(user)

            elif choice == 12:
                management.generate_certificate(user)

            elif choice == 13:
                management.view_certificates(user)

            elif choice == 14:
                report.report_menu(workshop, user)

            elif choice == 15:
                data_manager.save_all(workshop, user)

            elif choice == 16:
                break

            else:
                print("Invalid Choice")

    elif main_choice == 2:

        while True:
            print("\n===== USER MENU =====")
            print("1. View Workshops")
            print("2. Search Workshop")
            print("3. Register for Workshop")
            print("4. View Grades")
            print("5. Print Certificate")
            print("6. Verify Certificate")
            print("7. Back")

            choice = int(input("Enter Choice: "))

            if choice == 1:
                workshop.view_workshops()

            elif choice == 2:
                workshop.search()

            elif choice == 3:
                user.register(workshop)

            elif choice == 4:
                user.view_grades()

            elif choice == 5:
                user.print_certificate()

            elif choice == 6:
                user.verify_certificate()

            elif choice == 7:
                break

            else:
                print("Invalid Choice")

    elif main_choice == 3:
        print("Thank You")
        break

    else:
        print("Invalid Choice")
