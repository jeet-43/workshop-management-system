# Workshop Management System

A command-line application written in Python to manage college workshops from start to finish, covering scheduling, participant registration, grading, and certificate generation.

Built as a first year summer project to practise object-oriented Python.

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Sample Output](#sample-output)
- [Planned Improvements](#planned-improvements)

---

## About

Managing college workshops by hand means juggling spreadsheets, paper registers, and manually checking who paid, who attended, and who passed. This project replaces all of that with a simple menu-driven system that keeps everything in one place.

There are two separate portals: one for the organizer who runs the workshop, and one for participants who register and collect their certificates. Data is saved to local text files in a readable, database-style layout, and is automatically loaded back in the next time the program runs.

The system is built around four classes — `Workshop`, `User`, `WorkshopManagement`, and `Report` — each responsible for one part of the system.

---

## Features

### Organizer Portal

**Workshop Management**
- Add workshops with name, date, instructor, department, capacity, and fee (with input validation for capacity and fee)
- View all workshops with live seat counts and current status
- Update status: Upcoming, Ongoing, Completed, or Cancelled
- Delete a workshop, with a confirmation prompt

**Participant Management**
- View all participants registered to a given workshop
- Search participants by name, roll number, email, workshop ID, or department (partial and case-insensitive matching)
- Update payment status: Paid, Pending, or Waived
- Mark attendance per workshop, one participant at a time
- Cancel a registration, which frees up the seat on the workshop

**Grades**
- Enter a score from 0 to 100 for any participant marked Present
- Grade is calculated automatically (A+, A, B, C, D, F)
- Pass or Fail result assigned based on score

**Certificates**
- Generate a certificate for any participant who passed
- Each certificate gets a unique ID (e.g. `CERT-W1-P1`)
- View all issued certificates in one list

**Reports**
- Summary dashboard with workshop status breakdown (Upcoming/Ongoing/Completed/Cancelled) and participant breakdown (Registered/Cancelled/Paid/Present/Passed/Failed)
- Save all data to text files in a structured, human-readable format

### Participant Portal

- Browse available workshops with seat availability and fees
- Register for a workshop (checks for a full workshop, closed registration, and duplicate sign-ups)
- View an assigned grade and result
- Print a formatted certificate to the terminal
- Verify any certificate by its ID

---

## Tech Stack

- **Python 3** only — no external libraries or database required

Data persistence is handled with built-in file I/O, writing to structured `.txt` files that double as a simple flat-file database and are loaded back automatically on startup.

---

## Getting Started

### Requirements

Just Python 3. No installation of extra packages is needed.

### Running the App

```bash
python workshop_management.py
```

The program loads any existing data from `workshops.txt` and `participants.txt` automatically on startup, and can be saved at any time from the organizer menu.

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
Add a workshop, register participants, mark attendance after the session, enter grades, and generate certificates for those who passed. Use the search feature to quickly look up any participant by name, roll number, email, workshop, or department.

**Participant flow:**
View available workshops, register, and once the organizer has generated a certificate, use the certificate ID to print or verify it.

---

## Project Structure

```
workshop-management-system/
|
|-- workshop_management.py   # All application logic (Workshop, User, WorkshopManagement, Report classes)
|-- workshops.txt            # Auto-generated on save, auto-loaded on startup
|-- participants.txt         # Auto-generated on save, auto-loaded on startup
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

**Saved data file (`participants.txt`):**

```
===== PARTICIPANTS DATABASE =====

Participant ID : P1
Name           : John
Email          : john@example.com
Roll No        : CS101
Department     : CS
Workshop       : W1
Payment        : Paid
Attendance     : Present
Status         : Registered
Grade          : A
Result         : Pass
Certificate    : CERT-W1-P1
----------------------------------------
```

---

## Planned Improvements

- Grade distribution charts (pie/bar) using Matplotlib and NumPy
- GUI using Tkinter
- SQLite database instead of text files
- Email notification on registration and certificate issue
- PDF export for certificates
- Password-protected organizer login

---

## Author

**JEET MAKHIJA**

---

## License

This project is open source under the [MIT License](LICENSE).
