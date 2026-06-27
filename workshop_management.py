import matplotlib.pyplot as plt
import numpy as np

workshops = []
participants = []
grades = []
certificates = []


# ── WORKSHOP FUNCTIONS ────────────────────────────────────────

def add_workshop():
    print("\n--- Add Workshop ---")
    name       = input("Workshop name: ")
    date       = input("Date (DD/MM/YYYY): ")
    instructor = input("Instructor name: ")
    dept       = input("Department: ")

    while True:
        try:
            capacity = int(input("Capacity: "))
            break
        except ValueError:
            print("Enter a whole number.")

    while True:
        try:
            fee = float(input("Fee (0 if free): "))
            if fee >= 0:
                break
            print("Fee cannot be negative.")
        except ValueError:
            print("Enter a valid number.")

    workshops.append({
        "id": len(workshops) + 1,
        "name": name, "date": date,
        "instructor": instructor, "department": dept,
        "capacity": capacity, "fee": fee,
        "enrolled": 0, "status": "Upcoming"
    })
    print(f"Workshop '{name}' added!")


def view_workshops():
    print("\n--- Workshops ---")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    for w in workshops:
        if w["fee"] == 0:
            fee_str = "Free"
        else:
            fee_str = "Rs." + str(w["fee"])
        print("ID      :", w["id"])
        print("Name    :", w["name"])
        print("Date    :", w["date"])
        print("Instructor:", w["instructor"])
        print("Seats   :", str(w["enrolled"]) + "/" + str(w["capacity"]))
        print("Fee     :", fee_str)
        print("Status  :", w["status"])
        print("-" * 30)


def update_workshop_status():
    print("\n--- Update Workshop Status ---")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    workshop = None
    for w in workshops:
        if w["id"] == wid:
            workshop = w
            break

    if workshop == None:
        print("Workshop not found.")
        return

    print("1. Upcoming")
    print("2. Ongoing")
    print("3. Completed")
    print("4. Cancelled")
    choice = input("Choose: ")

    if choice == "1":
        workshop["status"] = "Upcoming"
    elif choice == "2":
        workshop["status"] = "Ongoing"
    elif choice == "3":
        workshop["status"] = "Completed"
    elif choice == "4":
        workshop["status"] = "Cancelled"
    else:
        print("Invalid choice.")
        return

    print("Status updated to: " + workshop["status"])


def delete_workshop():
    print("\n--- Delete Workshop ---")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    for i in range(len(workshops)):
        if workshops[i]["id"] == wid:
            print("Deleted: " + workshops[i]["name"])
            workshops.pop(i)
            return
    print("Workshop not found.")


# ── PARTICIPANT FUNCTIONS ─────────────────────────────────────

def register_participant():
    print("\n--- Register Participant ---")
    if len(workshops) == 0:
        print("No workshops available.")
        return

    name    = input("Full name: ")
    email   = input("Email: ")
    roll_no = input("Roll / Student ID: ")
    dept    = input("Department: ")
    year    = input("Year / Semester: ")

    print("\nAvailable Workshops:")
    for w in workshops:
        if w["status"] == "Upcoming" or w["status"] == "Ongoing":
            if w["enrolled"] < w["capacity"]:
                seats_left = w["capacity"] - w["enrolled"]
                if w["fee"] == 0:
                    fee_str = "Free"
                else:
                    fee_str = "Rs." + str(w["fee"])
                print(str(w["id"]) + ". " + w["name"] + " | " + w["date"] +
                      " | Seats left: " + str(seats_left) + " | " + fee_str)

    try:
        wid = int(input("Choose workshop ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    selected = None
    for w in workshops:
        if w["id"] == wid:
            selected = w
            break

    if selected == None:
        print("Workshop not found.")
        return
    if selected["enrolled"] >= selected["capacity"]:
        print("Workshop is full!")
        return
    if selected["status"] != "Upcoming" and selected["status"] != "Ongoing":
        print("Registration closed for this workshop.")
        return

    already_registered = False
    for p in participants:
        if p["email"] == email and p["workshop_id"] == wid:
            already_registered = True
            break
    if already_registered:
        print("Already registered!")
        return

    participants.append({
        "id": len(participants) + 1,
        "name": name, "email": email,
        "roll_no": roll_no, "department": dept, "year": year,
        "workshop_id": wid, "workshop": selected["name"],
        "payment": "Pending", "attendance": "Absent"
    })
    selected["enrolled"] += 1
    print(name + " registered for '" + selected["name"] + "' successfully!")
    if selected["fee"] > 0:
        print("Fee due: Rs." + str(selected["fee"]) + " | Payment: Pending")


def view_participants():
    print("\n--- Participants ---")
    if len(participants) == 0:
        print("No participants yet.")
        return
    for p in participants:
        print("ID      :", p["id"])
        print("Name    :", p["name"])
        print("Roll No :", p["roll_no"])
        print("Workshop:", p["workshop"])
        print("Payment :", p["payment"])
        print("Attendance:", p["attendance"])
        print("-" * 30)


def search_participant():
    print("\n--- Search Participant ---")
    if len(participants) == 0:
        print("No participants found.")
        return

    print("Search by:")
    print("1. Name")
    print("2. Roll Number")
    print("3. Email")
    print("4. Workshop")
    print("5. Department")
    choice = input("Choose: ")

    if choice == "1":
        keyword = input("Enter name (or part of it): ").lower()
        results = [p for p in participants if keyword in p["name"].lower()]
    elif choice == "2":
        keyword = input("Enter roll number: ").lower()
        results = [p for p in participants if keyword in p["roll_no"].lower()]
    elif choice == "3":
        keyword = input("Enter email (or part of it): ").lower()
        results = [p for p in participants if keyword in p["email"].lower()]
    elif choice == "4":
        keyword = input("Enter workshop name (or part of it): ").lower()
        results = [p for p in participants if keyword in p["workshop"].lower()]
    elif choice == "5":
        keyword = input("Enter department (or part of it): ").lower()
        results = [p for p in participants if keyword in p["department"].lower()]
    else:
        print("Invalid choice.")
        return

    if len(results) == 0:
        print("No participants found matching your search.")
        return

    print("\n" + str(len(results)) + " result(s) found:")
    print("-" * 30)
    for p in results:
        print("ID        :", p["id"])
        print("Name      :", p["name"])
        print("Roll No   :", p["roll_no"])
        print("Email     :", p["email"])
        print("Department:", p["department"])
        print("Year      :", p["year"])
        print("Workshop  :", p["workshop"])
        print("Payment   :", p["payment"])
        print("Attendance:", p["attendance"])
        print("-" * 30)


def update_payment():
    print("\n--- Update Payment ---")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_participants()
    try:
        pid = int(input("Participant ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    participant = None
    for p in participants:
        if p["id"] == pid:
            participant = p
            break

    if participant == None:
        print("Participant not found.")
        return

    print("Current payment:", participant["payment"])
    print("1. Paid")
    print("2. Pending")
    print("3. Waived")
    choice = input("Choose: ")

    if choice == "1":
        participant["payment"] = "Paid"
    elif choice == "2":
        participant["payment"] = "Pending"
    elif choice == "3":
        participant["payment"] = "Waived"
    else:
        print("Invalid choice.")
        return

    print("Payment updated to: " + participant["payment"])


def mark_attendance():
    print("\n--- Mark Attendance ---")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    workshop_found = False
    for w in workshops:
        if w["id"] == wid:
            workshop_found = True
            break
    if workshop_found == False:
        print("Workshop not found.")
        return

    workshop_participants = []
    for p in participants:
        if p["workshop_id"] == wid:
            workshop_participants.append(p)

    if len(workshop_participants) == 0:
        print("No participants for this workshop.")
        return

    for p in workshop_participants:
        print("\n" + p["name"] + " (" + p["roll_no"] + ") - Current: " + p["attendance"])
        print("1. Present")
        print("2. Absent")
        ch = input("Mark: ")
        if ch == "1":
            p["attendance"] = "Present"
        elif ch == "2":
            p["attendance"] = "Absent"
        else:
            print("Skipped.")
    print("Attendance updated!")


# ── GRADE FUNCTIONS ───────────────────────────────────────────

def add_grades():
    print("\n--- Add / Update Grades ---")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    workshop = None
    for w in workshops:
        if w["id"] == wid:
            workshop = w
            break
    if workshop == None:
        print("Workshop not found.")
        return

    present_list = []
    for p in participants:
        if p["workshop_id"] == wid and p["attendance"] == "Present":
            present_list.append(p)

    if len(present_list) == 0:
        print("No present participants for this workshop.")
        return

    for p in present_list:
        print("\n" + p["name"] + " (" + p["roll_no"] + ")")
        while True:
            try:
                score = float(input("  Score (0-100): "))
                if 0 <= score <= 100:
                    break
                print("Enter between 0 and 100.")
            except ValueError:
                print("Invalid input.")

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

        existing = None
        for g in grades:
            if g["participant_id"] == p["id"] and g["workshop_id"] == wid:
                existing = g
                break

        if existing != None:
            existing["score"] = score
            existing["grade"] = grade
            existing["result"] = result
            print("  Updated: " + str(score) + "/100 -> " + grade + " (" + result + ")")
        else:
            grades.append({
                "id": len(grades) + 1,
                "participant_id": p["id"],
                "participant_name": p["name"],
                "roll_no": p["roll_no"],
                "workshop_id": wid,
                "workshop_name": workshop["name"],
                "score": score,
                "grade": grade,
                "result": result
            })
            print("  Saved: " + str(score) + "/100 -> " + grade + " (" + result + ")")


def view_grades():
    print("\n--- Grades ---")
    if len(grades) == 0:
        print("No grades recorded yet.")
        return
    for g in grades:
        print("Name    :", g["participant_name"])
        print("Roll No :", g["roll_no"])
        print("Workshop:", g["workshop_name"])
        print("Score   :", str(g["score"]) + "/100")
        print("Grade   :", g["grade"])
        print("Result  :", g["result"])
        print("-" * 30)


def grading_report():
    print("\n--- Grading Report (Pie Chart) ---")
    if len(grades) == 0:
        print("No grades found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID (0 = all): "))
    except ValueError:
        print("Invalid ID.")
        return

    if wid == 0:
        subset = grades
        title  = "All Workshops"
    else:
        workshop = None
        for w in workshops:
            if w["id"] == wid:
                workshop = w
                break
        if workshop == None:
            print("Workshop not found.")
            return
        subset = []
        for g in grades:
            if g["workshop_id"] == wid:
                subset.append(g)
        title = workshop["name"]

    if len(subset) == 0:
        print("No grades for selection.")
        return

    grade_list = []
    for g in subset:
        grade_list.append(g["grade"])

    unique, counts = np.unique(np.array(grade_list), return_counts=True)
    plt.figure(figsize=(6, 5))
    plt.pie(counts, labels=unique, autopct="%1.1f%%", startangle=140)
    plt.title("Grade Distribution - " + title)
    plt.tight_layout()
    plt.show()


# ── CERTIFICATE FUNCTIONS ─────────────────────────────────────

def generate_certificates():
    print("\n--- Generate Certificates ---")
    if len(grades) == 0:
        print("No grades found.")
        return
    view_workshops()
    try:
        wid = int(input("Workshop ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    workshop = None
    for w in workshops:
        if w["id"] == wid:
            workshop = w
            break
    if workshop == None:
        print("Workshop not found.")
        return

    count = 0
    for g in grades:
        if g["workshop_id"] != wid:
            continue
        if g["result"] != "Pass":
            continue

        already_issued = False
        for c in certificates:
            if c["participant_id"] == g["participant_id"] and c["workshop_id"] == wid:
                already_issued = True
                break
        if already_issued:
            continue

        participant = None
        for p in participants:
            if p["id"] == g["participant_id"]:
                participant = p
                break

        if participant != None:
            roll_no    = participant["roll_no"]
            department = participant["department"]
        else:
            roll_no    = ""
            department = ""

        wid_str = str(wid)
        pid_str = str(g["participant_id"])
        while len(wid_str) < 3:
            wid_str = "0" + wid_str
        while len(pid_str) < 4:
            pid_str = "0" + pid_str
        cert_id = "CERT-" + wid_str + "-" + pid_str
        certificates.append({
            "cert_id": cert_id,
            "participant_id": g["participant_id"],
            "participant_name": g["participant_name"],
            "roll_no": roll_no,
            "department": department,
            "workshop_id": wid,
            "workshop_name": workshop["name"],
            "instructor": workshop["instructor"],
            "date": workshop["date"],
            "score": g["score"],
            "grade": g["grade"]
        })
        count += 1

    print(str(count) + " certificate(s) generated for '" + workshop["name"] + "'.")


def view_certificates():
    print("\n--- Certificates ---")
    if len(certificates) == 0:
        print("No certificates issued yet.")
        return
    for c in certificates:
        print("Cert ID :", c["cert_id"])
        print("Name    :", c["participant_name"])
        print("Workshop:", c["workshop_name"])
        print("Date    :", c["date"])
        print("Score   :", str(c["score"]) + "/100")
        print("Grade   :", c["grade"])
        print("-" * 30)


def print_certificate():
    print("\n--- Print Certificate ---")
    cert_id = input("Certificate ID: ")

    c = None
    for cert in certificates:
        if cert["cert_id"] == cert_id:
            c = cert
            break

    if c == None:
        print("Certificate not found.")
        return

    border = "*" * 50
    gap    = "*" + " " * 48 + "*"
    print("\n" + border)
    print(gap)
    print("*" + "CERTIFICATE OF COMPLETION".center(48) + "*")
    print(gap)
    print("*" + "This is to certify that".center(48) + "*")
    print("*" + c["participant_name"].upper().center(48) + "*")
    print("*" + ("(" + c["roll_no"] + ")").center(48) + "*")
    print(gap)
    print("*" + "has successfully completed".center(48) + "*")
    print("*" + c["workshop_name"].center(48) + "*")
    print("*" + ("Held on: " + c["date"]).center(48) + "*")
    print(gap)
    print("*" + ("Score: " + str(c["score"]) + "   Grade: " + c["grade"]).center(48) + "*")
    print("*" + ("Instructor: " + c["instructor"]).center(48) + "*")
    print("*" + ("Cert ID: " + c["cert_id"]).center(48) + "*")
    print(gap)
    print(border)


def verify_certificate():
    print("\n--- Verify Certificate ---")
    cert_id = input("Certificate ID: ")

    c = None
    for cert in certificates:
        if cert["cert_id"] == cert_id:
            c = cert
            break

    if c != None:
        print("[VALID] Certificate found!")
        print("Issued to:", c["participant_name"])
        print("Workshop :", c["workshop_name"])
        print("Grade    :", c["grade"])
    else:
        print("[INVALID] Certificate not found.")


# ── SUMMARY & STATS ───────────────────────────────────────────

def show_summary():
    print("\n--- Summary ---")
    print("Total Workshops   :", len(workshops))
    print("Total Participants:", len(participants))
    print("Total Grades      :", len(grades))
    print("Total Certificates:", len(certificates))

    if len(workshops) > 0:
        upcoming  = 0
        ongoing   = 0
        completed = 0
        cancelled = 0
        for w in workshops:
            if w["status"] == "Upcoming":
                upcoming += 1
            elif w["status"] == "Ongoing":
                ongoing += 1
            elif w["status"] == "Completed":
                completed += 1
            elif w["status"] == "Cancelled":
                cancelled += 1
        print("Upcoming :", upcoming)
        print("Ongoing  :", ongoing)
        print("Completed:", completed)
        print("Cancelled:", cancelled)

    if len(participants) > 0:
        paid    = 0
        pending = 0
        present = 0
        for p in participants:
            if p["payment"] == "Paid":
                paid += 1
            elif p["payment"] == "Pending":
                pending += 1
            if p["attendance"] == "Present":
                present += 1
        print("Paid    :", paid)
        print("Pending :", pending)
        print("Present :", present)

    if len(grades) > 0:
        scores = np.array([g["score"] for g in grades])
        passed = 0
        for g in grades:
            if g["result"] == "Pass":
                passed += 1
        print("Passed  :", passed)
        print("Failed  :", len(grades) - passed)
        print("Average :", round(float(np.mean(scores)), 2))
        print("Highest :", float(np.max(scores)))
        print("Lowest  :", float(np.min(scores)))


# ── FILE I/O ──────────────────────────────────────────────────

def save_to_file():
    with open("workshops.txt", "w") as f:
        for w in workshops:
            line = (str(w["id"]) + "|" + w["name"] + "|" + w["date"] + "|" +
                    w["instructor"] + "|" + w["department"] + "|" +
                    str(w["capacity"]) + "|" + str(w["fee"]) + "|" +
                    str(w["enrolled"]) + "|" + w["status"])
            f.write(line + "\n")

    with open("participants.txt", "w") as f:
        for p in participants:
            line = (str(p["id"]) + "|" + p["name"] + "|" + p["email"] + "|" +
                    p["roll_no"] + "|" + p["department"] + "|" + p["year"] + "|" +
                    str(p["workshop_id"]) + "|" + p["workshop"] + "|" +
                    p["payment"] + "|" + p["attendance"])
            f.write(line + "\n")

    with open("grades.txt", "w") as f:
        for g in grades:
            line = (str(g["id"]) + "|" + str(g["participant_id"]) + "|" +
                    g["participant_name"] + "|" + g["roll_no"] + "|" +
                    str(g["workshop_id"]) + "|" + g["workshop_name"] + "|" +
                    str(g["score"]) + "|" + g["grade"] + "|" + g["result"])
            f.write(line + "\n")

    with open("certificates.txt", "w") as f:
        for c in certificates:
            line = (c["cert_id"] + "|" + str(c["participant_id"]) + "|" +
                    c["participant_name"] + "|" + c["roll_no"] + "|" +
                    c["department"] + "|" + str(c["workshop_id"]) + "|" +
                    c["workshop_name"] + "|" + c["instructor"] + "|" +
                    c["date"] + "|" + str(c["score"]) + "|" + c["grade"])
            f.write(line + "\n")

    print("Data saved successfully.")


def load_from_file():
    workshops.clear()
    participants.clear()
    grades.clear()
    certificates.clear()

    try:
        with open("workshops.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 9:
                    workshops.append({
                        "id": int(p[0]), "name": p[1], "date": p[2],
                        "instructor": p[3], "department": p[4],
                        "capacity": int(p[5]), "fee": float(p[6]),
                        "enrolled": int(p[7]), "status": p[8]
                    })
        print("Workshops loaded:", len(workshops))
    except FileNotFoundError:
        print("Starting fresh (no workshops.txt).")

    try:
        with open("participants.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 10:
                    participants.append({
                        "id": int(p[0]), "name": p[1], "email": p[2],
                        "roll_no": p[3], "department": p[4], "year": p[5],
                        "workshop_id": int(p[6]), "workshop": p[7],
                        "payment": p[8], "attendance": p[9]
                    })
        print("Participants loaded:", len(participants))
    except FileNotFoundError:
        pass

    try:
        with open("grades.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 9:
                    grades.append({
                        "id": int(p[0]), "participant_id": int(p[1]),
                        "participant_name": p[2], "roll_no": p[3],
                        "workshop_id": int(p[4]), "workshop_name": p[5],
                        "score": float(p[6]), "grade": p[7], "result": p[8]
                    })
        print("Grades loaded:", len(grades))
    except FileNotFoundError:
        pass

    try:
        with open("certificates.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 11:
                    certificates.append({
                        "cert_id": p[0], "participant_id": int(p[1]),
                        "participant_name": p[2], "roll_no": p[3],
                        "department": p[4], "workshop_id": int(p[5]),
                        "workshop_name": p[6], "instructor": p[7],
                        "date": p[8], "score": float(p[9]), "grade": p[10]
                    })
        print("Certificates loaded:", len(certificates))
    except FileNotFoundError:
        pass


# ── MENUS ─────────────────────────────────────────────────────

def organizer_menu():
    while True:
        print("\n==============================")
        print("       ORGANIZER MENU         ")
        print("==============================")
        print("1.  Add Workshop")
        print("2.  View Workshops")
        print("3.  Update Workshop Status")
        print("4.  Delete Workshop")
        print("------------------------------")
        print("5.  View Participants")
        print("6.  Search Participant")
        print("7.  Update Payment Status")
        print("8.  Mark Attendance")
        print("------------------------------")
        print("9.  Add / Update Grades")
        print("10. View Grades")
        print("11. Grading Report (Pie Chart)")
        print("------------------------------")
        print("12. Generate Certificates")
        print("13. View Certificates")
        print("------------------------------")
        print("14. Summary")
        print("15. Save Data")
        print("16. Back")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            add_workshop()
        elif choice == "2":
            view_workshops()
        elif choice == "3":
            update_workshop_status()
        elif choice == "4":
            delete_workshop()
        elif choice == "5":
            view_participants()
        elif choice == "6":
            search_participant()
        elif choice == "7":
            update_payment()
        elif choice == "8":
            mark_attendance()
        elif choice == "9":
            add_grades()
        elif choice == "10":
            view_grades()
        elif choice == "11":
            grading_report()
        elif choice == "12":
            generate_certificates()
        elif choice == "13":
            view_certificates()
        elif choice == "14":
            show_summary()
        elif choice == "15":
            save_to_file()
        elif choice == "16":
            break
        else:
            print("Invalid choice. Please try again.")


def participant_menu():
    while True:
        print("\n==============================")
        print("      PARTICIPANT MENU        ")
        print("==============================")
        print("1. View Workshops")
        print("2. Register for a Workshop")
        print("3. Print My Certificate")
        print("4. Verify a Certificate")
        print("5. Back")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            view_workshops()
        elif choice == "2":
            register_participant()
        elif choice == "3":
            print_certificate()
        elif choice == "4":
            verify_certificate()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    load_from_file()
    while True:
        print("\n==============================")
        print("  WORKSHOP MANAGEMENT SYSTEM  ")
        print("==============================")
        print("1. Organizer")
        print("2. Participant")
        print("3. Exit")
        print("==============================")
        choice = input("Choice: ")
        if choice == "1":
            organizer_menu()
        elif choice == "2":
            participant_menu()
        elif choice == "3":
            save_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


main()
