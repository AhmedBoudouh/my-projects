# Secure Access Control System (Python)

##  Project Description

This project is a **college academic project** developed as part of my studies.

The project topic was selected from a list proposed by my professor, with the following link used only as **initial inspiration for the general theme**:
https://nevonprojects.com/military-access-using-card-scanning-with-otp/

  **Important clarification**  
The reference provided only a **raw concept**.  
**All system ideas, security mechanisms, logic, architecture, and implementation were fully imagined and designed by me**, then implemented from scratch in Python.

This project is a **simulation of a secure access control system**, created to help me understand Python programming, security logic, and application structure.

---

##  Project Goal

The goal of this project is to simulate a secure access control system that:
- Prevents card duplication
- Detects unauthorized (external) scanners
- Protects PIN and OTP data
- Controls access to multiple security zones
- Demonstrates basic security principles in software design

---

##  Key Security Ideas Implemented

### 1️ Scan Count Mechanism (Anti-Cloning)

Each smart card maintains a **scan count** synchronized with the database.

- Every official scan updates the scan count
- If a card is scanned using an external or fake scanner, the scan count becomes incorrect
- On the next official scan, the server detects the mismatch
- The card is identified as potentially duplicated or compromised

 This allows detection of card cloning without destroying the card.

---

### 2️ PIN Train (Hidden PIN Transmission)

Instead of sending the PIN directly:

- The real PIN digits are hidden inside a list of random digits (PIN Train)
- Only specific positions correspond to the real PIN
- Even if intercepted, the real PIN cannot be identified

  Protects against PIN interception.

---

### 3️ OTP Cloud (Secure OTP Display)

Instead of sending the OTP to a mobile phone:

- The OTP is generated internally
- A cloud of 5 OTPs is displayed (1 real + 4 fake)
- The server verifies which OTP is correct

  Makes OTP interception ineffective.

---

##  Access Zones

The system includes **three security zones**, each with increasing authentication requirements:

| Zone | Authentication Required |
|-----|--------------------------|
| Zone 1 | Smart card only |
| Zone 2 | Smart card + PIN + OTP |
| Zone 3 | Smart card + PIN + Biometric (simulated) |

Unauthorized attempts are tracked and may result in **card locking**.

---

##  How It Works (High Level)

1. A user is created and stored in a SQLite database
2. A virtual smart card is loaded for the user
3. Each scan updates the scan count using internal logic
4. Servers validate scan counts and authentication data
5. Access is granted or denied based on zone rules
6. Logs and UI displays show real-time system behavior

---

##  How to Run the Project

1. Clone the repository
2. Navigate to the project folder
3. Run the application:

```bash
python main.py

```
---
##  Skills Demonstrated

- Python programming (Object-Oriented Programming)
- GUI development with Tkinter
- SQLite database integration
- Authentication and access control logic
- Modular and structured project design

---
##  Academic Disclaimer

This project was developed **for educational purposes** as part of a college course.  
It is a **simulation** designed to demonstrate programming and security concepts and is **not intended for production use**.

---
##  Author

Developed by **Ahmed Boudouh**  
College academic project – Secure Access Control System (Python)

Supervised by **Prof. Anderson Duncan**