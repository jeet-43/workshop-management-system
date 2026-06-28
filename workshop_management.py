import matplotlib.pyplot as plt
import numpy as np

workshops    = []
participants = []
grades       = []
certificates = []


# -----------------------------------------------
#  WORKSHOP FUNCTIONS
# -----------------------------------------------

def add_workshop():
    print("")
    print("------------------------------")
    print("       ADD NEW WORKSHOP       ")
    print("------------------------------")
    name       = input("Workshop name          : ")
    date       = input("Date (DD/MM/YYYY)      : ")
    instructor = input("Instructor name        : ")
    dept       = input("Department             : ")

    while True:
        try:
            capacity = int(input("Capacity               : "))
            if capacity > 0:
                break
            print("Capacity must be at least 1.")
        except ValueError:
            print("Please enter a whole number.")

    while True:
        try:
            fee = float(input("Fee (0=Free)           : "))
            if fee >= 0:
                break
            print("Fee cannot be negative.")
        except ValueError:
            print("Please enter a valid number.")

    workshops.append({
        "id"         : len(workshops) + 1,
        "name"       : name,
        "date"       : date,
        "instructor" : instructor,
        "department" : dept,
        "capacity"   : capacity,
        "fee"        : fee,
        "enrolled"   : 0,
        "status"     : "Upcoming"
    })
    print("Workshop added: " + name)


def view_workshops():
    print("")
    print("------------------------------")
    print("         ALL WORKSHOPS        ")
    print("------------------------------")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    for w in workshops:
        if w["fee"] == 0:
            fee_str = "Free"
        else:
            fee_str = "Rs." + str(w["fee"])
        seats_left = w["capacity"] - w["enrolled"]
        print("ID         : " + str(w["id"]))
        print("Name       : " + w["name"])
        print("Instructor : " + w["instructor"] + " | Dept: " + w["department"])
        print("Schedule   : " + w["date"])
        print("Seats      : " + str(seats_left) + " left out of " + str(w["capacity"]))
        print("Fee        : " + fee_str)
        print("Status     : " + w["status"])
        print("------------------------------")


def update_workshop_status():
    print("")
    print("------------------------------")
    print("    UPDATE WORKSHOP STATUS    ")
    print("------------------------------")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    view_workshops()
    try:
        wid = int(input("Enter Workshop ID: "))
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

    print("Current Status: " + workshop["status"])
    print("1. Upcoming")
    print("2. Ongoing")
    print("3. Completed")
    print("4. Cancelled")
    choice = input("Choose new status: ")

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
    print("")
    print("------------------------------")
    print("        DELETE WORKSHOP       ")
    print("------------------------------")
    if len(workshops) == 0:
        print("No workshops found.")
        return
    view_workshops()
    try:
        wid = int(input("Enter Workshop ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    for i in range(len(workshops)):
        if workshops[i]["id"] == wid:
            confirm = input("Are you sure you want to delete this workshop? (yes/no): ")
            if confirm.lower() == "yes":
                workshops.pop(i)
                print("Workshop deleted.")
            else:
                print("Deletion cancelled.")
            return
    print("Workshop not found.")


# -----------------------------------------------
#  PARTICIPANT FUNCTIONS
# -----------------------------------------------

def register_participant():
    print("")
    print("------------------------------")
    print("     REGISTER FOR WORKSHOP    ")
    print("------------------------------")
    if len(workshops) == 0:
        print("No workshops available.")
        return

    name    = input("Your full name         : ")
    email   = input("Email address          : ")
    roll_no = input("Roll / Student ID      : ")
    dept    = input("Department             : ")
    year    = input("Year / Semester        : ")

    print("")
    print("-- Available Workshops --")
    found_any = False
    for w in workshops:
        if w["status"] == "Upcoming" or w["status"] == "Ongoing":
            if w["enrolled"] < w["capacity"]:
                if w["fee"] == 0:
                    fee_str = "Free"
                else:
                    fee_str = "Rs." + str(w["fee"])
                seats_left = w["capacity"] - w["enrolled"]
                print(str(w["id"]) + ". " + w["name"] + " | " + w["date"] +
                      " | Seats left: " + str(seats_left) +
                      " | " + fee_str)
                found_any = True

    if found_any == False:
        print("No seats available right now.")
        return

    try:
        wid = int(input("Enter Workshop ID to register: "))
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
        print("Sorry, this workshop is full!")
        return
    if selected["status"] != "Upcoming" and selected["status"] != "Ongoing":
        print("Registration is closed for this workshop.")
        return

    for p in participants:
        if p["email"] == email and p["workshop_id"] == wid and p["status"] == "Registered":
            print("You have already registered for this workshop!")
            return

    participants.append({
        "id"          : len(participants) + 1,
        "name"        : name,
        "email"       : email,
        "roll_no"     : roll_no,
        "department"  : dept,
        "year"        : year,
        "workshop_id" : wid,
        "workshop"    : selected["name"],
        "payment"     : "Pending",
        "attendance"  : "Absent",
        "status"      : "Registered"
    })
    selected["enrolled"] += 1
    print("")
    print("Registration Confirmed!")
    print(name + " registered for: " + selected["name"])
    if selected["fee"] > 0:
        print("Fee due: Rs." + str(selected["fee"]) + " | Payment: Pending")


def view_participants():
    print("")
    print("------------------------------")
    print("        ALL PARTICIPANTS      ")
    print("------------------------------")
    if len(participants) == 0:
        print("No participants found.")
        return
    for p in participants:
        print("ID         : " + str(p["id"]))
        print("Name       : " + p["name"])
        print("Roll No    : " + p["roll_no"])
        print("Workshop   : " + p["workshop"])
        print("Payment    : " + p["payment"])
        print("Attendance : " + p["attendance"])
        print("Status     : " + p["status"])
        print("------------------------------")


def search_participant():
    print("")
    print("------------------------------")
    print("      SEARCH PARTICIPANT      ")
    print("------------------------------")
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

    results = []

    if choice == "1":
        keyword = input("Enter name: ").lower()
        for p in participants:
            if keyword in p["name"].lower():
                results.append(p)
    elif choice == "2":
        keyword = input("Enter roll number: ").lower()
        for p in participants:
            if keyword in p["roll_no"].lower():
                results.append(p)
    elif choice == "3":
        keyword = input("Enter email: ").lower()
        for p in participants:
            if keyword in p["email"].lower():
                results.append(p)
    elif choice == "4":
        keyword = input("Enter workshop: ").lower()
        for p in participants:
            if keyword in p["workshop"].lower():
                results.append(p)
    elif choice == "5":
        keyword = input("Enter department: ").lower()
        for p in participants:
            if keyword in p["department"].lower():
                results.append(p)
    else:
        print("Invalid choice.")
        return

    if len(results) == 0:
        print("No participants found.")
        return

    print(str(len(results)) + " result(s) found:")
    print("------------------------------")
    for p in results:
        print("ID         : " + str(p["id"]))
        print("Name       : " + p["name"])
        print("Email      : " + p["email"])
        print("Roll No    : " + p["roll_no"])
        print("Department : " + p["department"])
        print("Workshop   : " + p["workshop"])
        print("Payment    : " + p["payment"])
        print("Attendance : " + p["attendance"])
        print("Status     : " + p["status"])
        print("------------------------------")


def update_payment():
    print("")
    print("------------------------------")
    print("     UPDATE PAYMENT STATUS    ")
    print("------------------------------")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_participants()
    try:
        pid = int(input("Enter Participant ID: "))
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

    print("Current payment: " + participant["payment"])
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
    print("")
    print("------------------------------")
    print("        MARK ATTENDANCE       ")
    print("------------------------------")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_workshops()
    try:
        wid = int(input("Enter Workshop ID: "))
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

    roster = []
    for p in participants:
        if p["workshop_id"] == wid and p["status"] == "Registered":
            roster.append(p)

    if len(roster) == 0:
        print("No registered participants for this workshop.")
        return

    for p in roster:
        print("")
        print(p["name"] + " (" + p["roll_no"] + ") - Current: " + p["attendance"])
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


def cancel_registration():
    print("")
    print("------------------------------")
    print("      CANCEL REGISTRATION     ")
    print("------------------------------")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_participants()
    try:
        pid = int(input("Enter Participant ID to cancel: "))
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
    if participant["status"] == "Cancelled":
        print("This registration is already cancelled.")
        return

    confirm = input("Cancel registration for " + participant["name"] + "? (yes/no): ")
    if confirm.lower() != "yes":
        print("Cancellation aborted.")
        return

    participant["status"] = "Cancelled"
    for w in workshops:
        if w["id"] == participant["workshop_id"]:
            if w["enrolled"] > 0:
                w["enrolled"] -= 1
            break
    print("Registration cancelled for: " + participant["name"])


# -----------------------------------------------
#  GRADE FUNCTIONS
# -----------------------------------------------

def add_grades():
    print("")
    print("------------------------------")
    print("      ADD / UPDATE GRADES     ")
    print("------------------------------")
    if len(participants) == 0:
        print("No participants found.")
        return
    view_workshops()
    try:
        wid = int(input("Enter Workshop ID to grade: "))
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
    if workshop["status"] != "Completed":
        print("Grades can only be added for Completed workshops.")
        return

    present_list = []
    for p in participants:
        if p["workshop_id"] == wid and p["status"] == "Registered" and p["attendance"] == "Present":
            present_list.append(p)

    if len(present_list) == 0:
        print("No present participants for this workshop.")
        return

    for p in present_list:
        print("")
        print("Participant: " + p["name"] + " (" + p["roll_no"] + ")")
        while True:
            try:
                score = float(input("Score (0-100): "))
                if 0 <= score <= 100:
                    break
                print("Enter a number between 0 and 100.")
            except ValueError:
                print("Invalid input.")

        remarks = input("Remarks (press Enter to skip): ")

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
            existing["score"]   = score
            existing["grade"]   = grade
            existing["result"]  = result
            existing["remarks"] = remarks
            print("Updated: " + str(score) + "/100 -> " + grade + " (" + result + ")")
        else:
            grades.append({
                "id"               : len(grades) + 1,
                "participant_id"   : p["id"],
                "participant_name" : p["name"],
                "roll_no"          : p["roll_no"],
                "workshop_id"      : wid,
                "workshop_name"    : workshop["name"],
                "score"            : score,
                "grade"            : grade,
                "result"           : result,
                "remarks"          : remarks
            })
            print("Saved: " + str(score) + "/100 -> " + grade + " (" + result + ")")


def view_grades():
    print("")
    print("------------------------------")
    print("           ALL GRADES         ")
    print("------------------------------")
    if len(grades) == 0:
        print("No grades recorded yet.")
        return
    for g in grades:
        print("Participant : " + g["participant_name"])
        print("Workshop    : " + g["workshop_name"])
        print("Score       : " + str(g["score"]) + "/100")
        print("Grade       : " + g["grade"] + " (" + g["result"] + ")")
        if g["remarks"] == "":
            print("Remarks     : None")
        else:
            print("Remarks     : " + g["remarks"])
        print("------------------------------")


def grading_charts():
    print("")
    print("------------------------------")
    print("         GRADING CHARTS       ")
    print("------------------------------")
    if len(grades) == 0:
        print("No grades found.")
        return

    view_workshops()
    try:
        wid = int(input("Workshop ID (0 = all workshops): "))
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
        print("No grades found for this selection.")
        return

    print("Choose chart type:")
    print("1. Pie Chart  (result wise)")
    print("2. Bar Chart  (grade wise)")
    chart_choice = input("Choose: ")

    result_list = []
    grade_list  = []
    for g in subset:
        result_list.append(g["result"])
        grade_list.append(g["grade"])

    if chart_choice == "1":
        unique, counts = np.unique(np.array(result_list), return_counts=True)
        colors = ["#4caf50", "#f44336"]
        plt.figure(figsize=(6, 5))
        plt.pie(counts, labels=unique, autopct="%1.1f%%", startangle=140,
                colors=colors[:len(unique)])
        plt.title("Result Distribution - " + title)
        plt.tight_layout()
        plt.show()

    elif chart_choice == "2":
        grade_counts = []
        for gr in ["A+", "A", "B", "C", "D", "F"]:
            grade_counts.append(grade_list.count(gr))
        bar_colors = ["#4caf50", "#8bc34a", "#cddc39", "#ffc107", "#ff5722", "#f44336"]
        plt.figure(figsize=(6, 5))
        plt.bar(["A+", "A", "B", "C", "D", "F"], grade_counts, color=bar_colors)
        plt.title("Grade-wise Distribution - " + title)
        plt.xlabel("Grade")
        plt.ylabel("Number of Participants")
        plt.tight_layout()
        plt.show()

    else:
        print("Invalid choice.")


# -----------------------------------------------
#  CERTIFICATE FUNCTIONS
# -----------------------------------------------

def generate_certificates():
    print("")
    print("------------------------------")
    print("     GENERATE CERTIFICATES    ")
    print("------------------------------")
    if len(grades) == 0:
        print("Please add grades before generating certificates.")
        return
    view_workshops()
    try:
        wid = int(input("Enter Workshop ID: "))
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
        if participant == None:
            continue

        wid_str = str(wid)
        pid_str = str(g["participant_id"])
        while len(wid_str) < 3:
            wid_str = "0" + wid_str
        while len(pid_str) < 4:
            pid_str = "0" + pid_str
        cert_id = "CERT-" + wid_str + "-" + pid_str

        certificates.append({
            "cert_id"          : cert_id,
            "participant_id"   : g["participant_id"],
            "participant_name" : g["participant_name"],
            "roll_no"          : participant["roll_no"],
            "department"       : participant["department"],
            "workshop_id"      : wid,
            "workshop_name"    : workshop["name"],
            "instructor"       : workshop["instructor"],
            "date"             : workshop["date"],
            "score"            : g["score"],
            "grade"            : g["grade"]
        })
        count += 1

    print(str(count) + " certificate(s) generated for: " + workshop["name"])


def view_certificates():
    print("")
    print("------------------------------")
    print("        ALL CERTIFICATES      ")
    print("------------------------------")
    if len(certificates) == 0:
        print("No certificates issued yet.")
        return
    for c in certificates:
        print("Cert ID    : " + c["cert_id"])
        print("Participant: " + c["participant_name"])
        print("Workshop   : " + c["workshop_name"])
        print("Date       : " + c["date"])
        print("Score      : " + str(c["score"]) + "/100 | Grade: " + c["grade"])
        print("------------------------------")


def print_certificate():
    print("")
    print("------------------------------")
    print("       PRINT CERTIFICATE      ")
    print("------------------------------")
    cert_id = input("Enter Certificate ID: ")

    c = None
    for cert in certificates:
        if cert["cert_id"] == cert_id:
            c = cert
            break
    if c == None:
        print("Certificate not found.")
        return

    print("")
    print("******************************************")
    print("*                                        *")
    print("*     WORKSHOP COMPLETION CERTIFICATE    *")
    print("*                                        *")
    print("******************************************")
    print("*  PARTICIPANT                           *")
    print("*  Name    : " + c["participant_name"])
    print("*  Roll No : " + c["roll_no"])
    print("*  Dept    : " + c["department"])
    print("******************************************")
    print("*  WORKSHOP                              *")
    print("*  Name    : " + c["workshop_name"])
    print("*  Date    : " + c["date"])
    print("******************************************")
    print("*  INSTRUCTOR                            *")
    print("*  Name    : " + c["instructor"])
    print("******************************************")
    print("*  Score   : " + str(c["score"]) + "/100")
    print("*  Grade   : " + c["grade"])
    print("*  Cert ID : " + c["cert_id"])
    print("*                                        *")
    print("******************************************")


def verify_certificate():
    print("")
    print("------------------------------")
    print("       VERIFY CERTIFICATE     ")
    print("------------------------------")
    cert_id = input("Enter Certificate ID: ")

    c = None
    for cert in certificates:
        if cert["cert_id"] == cert_id:
            c = cert
            break

    if c != None:
        print("")
        print("VALID CERTIFICATE!")
        print("Issued to : " + c["participant_name"])
        print("Workshop  : " + c["workshop_name"])
        print("Grade     : " + c["grade"])
    else:
        print("")
        print("INVALID - Certificate not found.")


# -----------------------------------------------
#  SUMMARY
# -----------------------------------------------

def show_summary():
    print("")
    print("------------------------------")
    print("        SYSTEM SUMMARY        ")
    print("------------------------------")
    print("Total Workshops    : " + str(len(workshops)))
    print("Total Participants : " + str(len(participants)))
    print("Total Grades       : " + str(len(grades)))
    print("Total Certificates : " + str(len(certificates)))

    if len(workshops) > 0:
        print("")
        print("-- Workshop Status --")
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
        print("Upcoming  : " + str(upcoming))
        print("Ongoing   : " + str(ongoing))
        print("Completed : " + str(completed))
        print("Cancelled : " + str(cancelled))

    if len(participants) > 0:
        print("")
        print("-- Participant Status --")
        registered = 0
        cancelled  = 0
        paid       = 0
        pending    = 0
        present    = 0
        for p in participants:
            if p["status"] == "Registered":
                registered += 1
            elif p["status"] == "Cancelled":
                cancelled += 1
            if p["payment"] == "Paid":
                paid += 1
            elif p["payment"] == "Pending":
                pending += 1
            if p["attendance"] == "Present":
                present += 1
        print("Registered : " + str(registered))
        print("Cancelled  : " + str(cancelled))
        print("Paid       : " + str(paid))
        print("Pending    : " + str(pending))
        print("Present    : " + str(present))

    if len(grades) > 0:
        print("")
        print("-- Grade Stats --")
        scores = np.array([g["score"] for g in grades])
        print("Average : " + str(round(float(np.mean(scores)), 2)))
        print("Highest : " + str(float(np.max(scores))))
        print("Lowest  : " + str(float(np.min(scores))))
        print("")
        print("-- Grade Breakdown --")
        a_plus = 0
        a      = 0
        b      = 0
        c      = 0
        d      = 0
        f      = 0
        passed = 0
        failed = 0
        for g in grades:
            if g["grade"] == "A+":
                a_plus += 1
            elif g["grade"] == "A":
                a += 1
            elif g["grade"] == "B":
                b += 1
            elif g["grade"] == "C":
                c += 1
            elif g["grade"] == "D":
                d += 1
            elif g["grade"] == "F":
                f += 1
            if g["result"] == "Pass":
                passed += 1
            else:
                failed += 1
        print("A+ : " + str(a_plus))
        print("A  : " + str(a))
        print("B  : " + str(b))
        print("C  : " + str(c))
        print("D  : " + str(d))
        print("F  : " + str(f))
        print("Passed : " + str(passed))
        print("Failed : " + str(failed))

    print("------------------------------")


# -----------------------------------------------
#  FILE SAVE / LOAD
# -----------------------------------------------

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
                    p["payment"] + "|" + p["attendance"] + "|" + p["status"])
            f.write(line + "\n")

    with open("grades.txt", "w") as f:
        for g in grades:
            line = (str(g["id"]) + "|" + str(g["participant_id"]) + "|" +
                    g["participant_name"] + "|" + g["roll_no"] + "|" +
                    str(g["workshop_id"]) + "|" + g["workshop_name"] + "|" +
                    str(g["score"]) + "|" + g["grade"] + "|" + g["result"] + "|" +
                    g["remarks"])
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
                        "id"         : int(p[0]),
                        "name"       : p[1],
                        "date"       : p[2],
                        "instructor" : p[3],
                        "department" : p[4],
                        "capacity"   : int(p[5]),
                        "fee"        : float(p[6]),
                        "enrolled"   : int(p[7]),
                        "status"     : p[8]
                    })
        print("Workshops loaded    : " + str(len(workshops)))
    except FileNotFoundError:
        print("Starting fresh (no saved workshops found).")

    try:
        with open("participants.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 11:
                    participants.append({
                        "id"          : int(p[0]),
                        "name"        : p[1],
                        "email"       : p[2],
                        "roll_no"     : p[3],
                        "department"  : p[4],
                        "year"        : p[5],
                        "workshop_id" : int(p[6]),
                        "workshop"    : p[7],
                        "payment"     : p[8],
                        "attendance"  : p[9],
                        "status"      : p[10]
                    })
        print("Participants loaded : " + str(len(participants)))
    except FileNotFoundError:
        pass

    try:
        with open("grades.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 10:
                    grades.append({
                        "id"               : int(p[0]),
                        "participant_id"   : int(p[1]),
                        "participant_name" : p[2],
                        "roll_no"          : p[3],
                        "workshop_id"      : int(p[4]),
                        "workshop_name"    : p[5],
                        "score"            : float(p[6]),
                        "grade"            : p[7],
                        "result"           : p[8],
                        "remarks"          : p[9]
                    })
        print("Grades loaded       : " + str(len(grades)))
    except FileNotFoundError:
        pass

    try:
        with open("certificates.txt") as f:
            for line in f:
                p = line.strip().split("|")
                if len(p) == 11:
                    certificates.append({
                        "cert_id"          : p[0],
                        "participant_id"   : int(p[1]),
                        "participant_name" : p[2],
                        "roll_no"          : p[3],
                        "department"       : p[4],
                        "workshop_id"      : int(p[5]),
                        "workshop_name"    : p[6],
                        "instructor"       : p[7],
                        "date"             : p[8],
                        "score"            : float(p[9]),
                        "grade"            : p[10]
                    })
        print("Certificates loaded : " + str(len(certificates)))
    except FileNotFoundError:
        pass


# -----------------------------------------------
#  MENUS
# -----------------------------------------------

def organizer_menu():
    while True:
        print("")
        print("==============================")
        print("        ORGANIZER PANEL       ")
        print("==============================")
        print("  -- WORKSHOPS --")
        print("  1.  Add Workshop")
        print("  2.  View All Workshops")
        print("  3.  Update Workshop Status")
        print("  4.  Delete Workshop")
        print("------------------------------")
        print("  -- PARTICIPANTS --")
        print("  5.  View All Participants")
        print("  6.  Search Participant")
        print("  7.  Update Payment Status")
        print("  8.  Mark Attendance")
        print("  9.  Cancel a Registration")
        print("------------------------------")
        print("  -- GRADES --")
        print("  10. Add / Update Grades")
        print("  11. View All Grades")
        print("  12. Grading Charts")
        print("------------------------------")
        print("  -- CERTIFICATES --")
        print("  13. Generate Certificates")
        print("  14. View All Certificates")
        print("------------------------------")
        print("  15. Summary")
        print("  16. Save Data")
        print("  0.  Back to Main Menu")
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
            cancel_registration()
        elif choice == "10":
            add_grades()
        elif choice == "11":
            view_grades()
        elif choice == "12":
            grading_charts()
        elif choice == "13":
            generate_certificates()
        elif choice == "14":
            view_certificates()
        elif choice == "15":
            show_summary()
        elif choice == "16":
            save_to_file()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def participant_menu():
    while True:
        print("")
        print("==============================")
        print("      PARTICIPANT PORTAL      ")
        print("==============================")
        print("  1. View Available Workshops")
        print("  2. Register for a Workshop")
        print("  3. Print My Certificate")
        print("  4. Verify a Certificate")
        print("  0. Back to Main Menu")
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
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    print("Loading saved data...")
    load_from_file()

    while True:
        print("")
        print("==============================")
        print(" WORKSHOP MANAGEMENT SYSTEM   ")
        print("==============================")
        print("  1. Organizer Panel")
        print("  2. Participant Portal")
        print("  3. Exit")
        print("==============================")

        choice = input("Choice: ")

        if choice == "1":
            organizer_menu()
        elif choice == "2":
            participant_menu()
        elif choice == "3":
            save_to_file()
            print("Data saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
