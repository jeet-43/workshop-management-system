# Workshop Management System

A command-line application written in Python for managing academic workshops, from scheduling and participant registration to grading and certificate generation.

I built this as a summer project for my college, mainly to get more practice with object-oriented Python.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)

---

## About

Running an academic workshop by hand usually means juggling spreadsheets, paper registers, and manually tracking who paid, who showed up, and who passed. This project pulls all of that into one simple menu-driven system.

There are two portals: one for the admin running the workshop, and one for participants registering and collecting their certificates. Data is saved to local files using Python's built-in `pickle` module, and it loads back in automatically the next time the program runs.

The system is built around several data classes and manager classes. `WorkshopItem` and `Participant` hold the data for a single workshop or participant, while `AttendanceRecord` and `Transaction` hold the data that gets written out when attendance and payment records are saved. On the logic side, `Workshop` and `User` handle workshop and participant operations, `WorkshopManagement` handles the cross-cutting tasks like payments, attendance, grades, and certificates, `Report` builds the summary dashboard, and `DataManager` takes care of saving and loading everything to disk.

---

## Features

### Admin Portal

Access is protected by a username and password, with a limit of three attempts before the program returns to the main menu.

**Workshop Management**
- Add workshops with an auto-generated ID, name, date, venue, instructor, department, capacity, and fee, with input validation for capacity and fee
- View all workshops with live seat counts and current status
- Search workshops by ID, name, instructor, department, venue, status, or date (year only, month and year, or a full date)
- Update status: Upcoming, Ongoing, Completed, or Cancelled
- Delete a workshop, with a confirmation prompt

**Participant Management**
- View all participants tied to a given workshop
- Search participants by name, roll number, email, department, workshop ID, status, payment status, attendance, or date. Name, roll number, email, and department all do partial, case-insensitive matching, while workshop ID and status fields need an exact match
- Update payment status: Paid, Pending, or Waived
- Mark attendance for a workshop's registered participants, one participant at a time
- Cancel a registration, which frees up the seat on the workshop

**Grades**
- Enter a score from 0 to 100 for any participant marked Present
- Grade is calculated automatically (A+, A, B, C, D, F)
- Pass or Fail result assigned based on score

**Certificates**
- Generate a certificate for any participant who passed
- Each certificate gets a unique ID, for example `CERT-20260814-001-U001`
- View all issued certificates in one list

**Reports**
- A dedicated reports menu covering workshops, participants, attendance, transactions, and an overall summary
- The overview report includes a workshop status breakdown (Upcoming/Ongoing/Completed/Cancelled) and a participant breakdown (Registered/Cancelled/Paid/Present/Passed/Failed)
- Save all workshop, participant, attendance, and transaction data to local files with Python's `pickle` module

### User Portal

- Browse available workshops with seat availability and fees
- Search workshops using the same filters available to the admin
- Register for a workshop, with checks for a full workshop, closed registration, and duplicate sign-ups
- View an assigned grade and result by logging in with email and password
- Print a formatted certificate to the terminal
- Verify any certificate by its ID

---

## Tech Stack

- **Python 3** only, no external libraries or database required

Data persistence is handled with Python's built-in `pickle` module. It serializes the workshop and participant data into four separate local files and loads them back automatically on startup.

---

## Getting Started

### Requirements

Just Python 3. No extra packages to install.

### Running the App

```bash
python workshop_management.py
```

The program loads any existing data from the saved files automatically on startup, and can be saved at any time from the Admin menu (option 15, Save Data).

---

## How to Use

When you run the program, you choose between the Admin and User portal.

```
===== WORKSHOP MANAGEMENT SYSTEM =====
1. Admin
2. User
3. Exit
```

**Admin flow:**
Log in with the admin username and password, then add a workshop. Once participants have registered themselves through the User portal, mark attendance after the session, enter grades, and generate certificates for those who passed. Use the search feature to quickly look up any workshop or participant by a wide range of filters, and check the Reports menu for a full overview at any time.

**User flow:**
View or search available workshops, register with your details, check your grade once it has been assigned, and once the admin has generated a certificate, use the certificate ID to print or verify it.

---

## Project Structure

```
workshop-management-system/
|
|-- workshop_management.py   # All application logic (WorkshopItem, Participant, AttendanceRecord,
|                             # Transaction, Workshop, User, WorkshopManagement, Report, DataManager)
|-- workshop.txt              # Auto-generated on save (pickle format), auto-loaded on startup
|-- participants.txt          # Auto-generated on save (pickle format), auto-loaded on startup
|-- attendance.txt            # Auto-generated on save (pickle format), auto-loaded on startup
|-- transaction.txt           # Auto-generated on save (pickle format), auto-loaded on startup
|-- README.md
```

## Sample Output

**Certificate printed in terminal:**

```
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
**************************************************************
*                                                              *
*                  CERTIFICATE OF COMPLETION                  *
*                                                              *
*                This is proudly presented to                 *
*                            JOHN                              *
*                                                              *
*        for successfully completing Workshop 20260814-001    *
*                          Grade: A                            *
*                                                              *
*             Certificate ID: CERT-20260814-001-U001           *
*                                                              *
**************************************************************
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
```

**Saved data:**

Data is not written out as plain, human-readable text. The Admin's "Save Data" option pickles the workshop list, participant list, attendance records, and transaction records into four separate binary files:

```python
with open("workshop.txt", "wb") as f:
    pickle.dump(workshop.workshops, f)

with open("participants.txt", "wb") as f:
    pickle.dump(user.users, f)
```

Opening these files directly just shows raw binary data, not a formatted table. The program reads them back into memory automatically the next time it starts.

---

## Author

**JEET MAKHIJA**

---
