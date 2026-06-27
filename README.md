# Workshop Management System

A command-line application written in Python to manage college workshops from start to finish, covering scheduling, participant registration, grading, and certificate generation.

Built as a first year summer project to practise core Python concepts.

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

There are two separate portals: one for the organizer who runs the workshop, and one for participants who register and collect their certificates. Data is saved to local text files so nothing is lost between sessions.

---

## Features

### Organizer Portal

**Workshop Management**
- Add workshops with name, date, instructor, department, capacity, and fee
- View all workshops with current seat counts and status
- Update status: Upcoming, Ongoing, Completed, or Cancelled
- Delete a workshop from the system

**Participant Management**
- View all registered participants with payment and attendance status
- Search participants by name, roll number, email, workshop, or department (partial and case-insensitive matching)
- Update payment status: Paid, Pending, or Waived
- Mark attendance per workshop

**Grades**
- Enter scores from 0 to 100 for all present participants
- Grade is calculated automatically (A+, A, B, C, D, F)
- Pass or Fail result assigned based on score
- Pie chart report for grade distribution using Matplotlib

**Certificates**
- Generate certificates for all participants who passed
- Each certificate gets a unique ID (e.g. CERT-001-0001)
- View all issued certificates in one list

**Reports**
- Summary dashboard with totals, payment stats, and score averages including highest, lowest, and mean score
- Save all data to text files

### Participant Portal

- Browse available workshops with seat availability and fees
- Register for a workshop (checks for duplicate registration and seat limits)
- Print a formatted certificate to the terminal
- Verify any certificate by its ID

---

## Tech Stack

- **Python 3**
- **Matplotlib** for grade distribution pie chart
- **NumPy** for score statistics
- Built-in file I/O for data persistence

No database or external setup required.

---

## Getting Started

### Requirements

Python 3 must be installed. Install the two dependencies with:

```bash
pip install matplotlib numpy
```

### Running the App

```bash
python workshop_management.py
```

The program loads any existing data automatically on startup and saves on exit.

---

## How to Use

When you run the program, you choose between the Organizer and Participant portal.

```
==============================
  WORKSHOP MANAGEMENT SYSTEM  
==============================
1. Organizer
2. Participant
3. Exit
==============================
```

**Organizer flow:**
Add a workshop, register participants, mark attendance after the session, enter grades, and generate certificates for those who passed. Use the search feature to quickly look up any participant by name, roll number, email, workshop, or department.

**Participant flow:**
View available workshops, register, and once the organizer has generated certificates, use the certificate ID to print or verify it.

---

## Project Structure

```
workshop-management-system/
|
|-- workshop_management.py   # All application logic
|-- workshops.txt            # Auto-generated on save
|-- participants.txt         # Auto-generated on save
|-- grades.txt               # Auto-generated on save
|-- certificates.txt         # Auto-generated on save
|-- README.md
```

## Sample Output

**Certificate printed in terminal:**

```
**************************************************
*                                                *
*          CERTIFICATE OF COMPLETION            *
*                                                *
*           This is to certify that             *
*                  JOHN DOE                     *
*                (CS2024001)                    *
*                                               *
*         has successfully completed            *
*           Python Basics Workshop              *
*            Held on: 15/06/2024               *
*                                               *
*        Score: 85   Grade: A                   *
*       Instructor: Dr. Sharma                  *
*       Cert ID: CERT-001-0001                  *
*                                               *
**************************************************
```

---

## Planned Improvements

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
