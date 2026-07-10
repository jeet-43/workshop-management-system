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

There are two portals: one for the organizer running the workshop, and one for participants registering and collecting their certificates. Data is saved to a local file using Python's built-in `pickle` module, and it loads back in automatically the next time the program runs.

The system is built around six classes. `WorkshopItem` and `Participant` just hold the data for a single workshop or participant. Then there are four manager classes that do the actual work: `Workshop` and `User` handle workshop and participant operations, `WorkshopManagement` handles the cross-cutting stuff like payments, attendance, grades, certificates, and saving/loading, and `Report` builds the summary dashboard.

---

## Features

### Organizer Portal

**Workshop Management**
- Add workshops with name, date, venue, instructor, department, capacity, and fee, with input validation for capacity and fee
- View all workshops with live seat counts and current status
- Update status: Upcoming, Ongoing, Completed, or Cancelled
- Delete a workshop, with a confirmation prompt

**Participant Management**
- View all participants tied to a given workshop
- Search participants by name, roll number, email, workshop ID, or department. Name, roll number, email, and department all do partial, case-insensitive matching; workshop ID needs an exact match
- Update payment status: Paid, Pending, or Waived
- Mark attendance for a workshop's registered participants, one participant at a time
- Cancel a registration, which frees up the seat on the workshop

**Grades**
- Enter a score from 0 to 100 for any participant marked Present
- Grade is calculated automatically (A+, A, B, C, D, F)
- Pass or Fail result assigned based on score

**Certificates**
- Generate a certificate for any participant who passed
- Each certificate gets a unique ID, e.g. `CERT-W1-P1`
- View all issued certificates in one list

**Reports**
- Summary dashboard with a workshop status breakdown (Upcoming/Ongoing/Completed/Cancelled) and a participant breakdown (Registered/Cancelled/Paid/Present/Passed/Failed)
- Save all workshop and participant data to a single local file with Python's `pickle` module

### Participant Portal

- Browse available workshops with seat availability and fees
- Register for a workshop, with checks for a full workshop, closed registration, and duplicate sign-ups
- View an assigned grade and result
- Print a formatted certificate to the terminal
- Verify any certificate by its ID

---

## Tech Stack

- **Python 3** only, no external libraries or database required

Data persistence is handled with Python's built-in `pickle` module. It serializes the workshop and participant objects to a single local file, `workshop_data.txt`, and loads them back automatically on startup.

---

## Getting Started

### Requirements

Just Python 3. No extra packages to install.

### Running the App

```bash
python workshop_management.py
```

The program loads any existing data from `workshop_data.txt` automatically on startup, and can be saved at any time from the Organizer menu (option 14, Save Data).

---

## How to Use

When you run the program, you choose between the Organizer and Participant portal.

```
===== WORKSHOP MANAGEMENT SYSTEM =====
1. Organizer
2. Participant
3. Exit
```

**Organizer flow:**
Add a workshop first. Once participants have registered themselves through the Participant portal, mark attendance after the session, enter grades, and generate certificates for those who passed. Use the search feature to quickly look up any participant by name, roll number, email, workshop, or department.

**Participant flow:**
View available workshops, register, check your grade once it's assigned, and once the organizer has generated a certificate, use the certificate ID to print or verify it.

---

## Project Structure

```
workshop-management-system/
|
|-- workshop_management.py   # All application logic (WorkshopItem, Participant, Workshop, User, WorkshopManagement, Report classes)
|-- workshop_data.txt        # Auto-generated on save (pickle format), auto-loaded on startup
|-- README.md
```

## Sample Output

**Certificate printed in terminal:**

```
----- CERTIFICATE -----
Certificate of Completion
Presented to John
Workshop ID: W1
Grade: A
Certificate ID: CERT-W1-P1
```

**Saved data:**

Data isn't written out as plain, human-readable text. The Organizer's "Save Data" option pickles the full list of workshop and participant objects into a single binary file, `workshop_data.txt`:

```python
with open("workshop_data.txt", "wb") as f:
    pickle.dump(workshop.workshops, f)
    pickle.dump(user.users, f)
```

Opening that file directly just shows raw binary data, not a formatted table. The program reads it back into memory automatically the next time it starts.

---

## Author

**JEET MAKHIJA**

---

## License

This project is open source under the [MIT License](LICENSE).
