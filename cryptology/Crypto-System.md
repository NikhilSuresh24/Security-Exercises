
# Table of Contents
- [Table of Contents](#table-of-contents)
- [Security System: Security Gate of Corporate Parking Garage](#security-system-security-gate-of-corporate-parking-garage)
    - [Threat Model](#threat-model)
    - [Cryptographic Components](#cryptographic-components)
    - [Protocol Procedure](#protocol-procedure)
    - [Simple Implementation](#simple-implementation)


# Security System: Security Gate of Corporate Parking Garage

## Threat Model

In order to maintain good security of a parking garage, especially a corporate one, it is important to only let in authorized vehicles, and only allow them in at the times they should be allowed in at. With this in mind, listed below are some of the main threats to the sound security of a parking garage.

1. Former Employees
    1. If former employees retain their access to parking lots, they can get past the security.
2. Employees Provide Access to Others
    1. If employees provide access to outsiders, they can evade the security gate
3. Drive Through
    1. If a car drives through the beam preventing access to the parking lot, the cryptography cannot do anything.
4. Crack Password
    1. If an outsider is able to crack the password, either by brute force or by gaining additional information, they can get past the security

This security system aims to prevent situations 1 and 4 from occurring, and make it harder for situation 2 to happen.

## Cryptographic Components

This security system uses the fingerprint of an employee along with a random 10 - 12 character password (on an id card in the form of a QR code) to verify their identity. The password is sent to the server with a timestamp. The password is then salted and hashed with SHA-256 and compared to the hash in the database. If the hash, fingerprint, and time period (employees can only enter at certain times) are correct, the user is let through. Otherwise, they are denied. By requiring a fingerprint, the system requires the authorized employee to be present, making it difficult for employees to easily provide access to others. Addtionally, by removing the passwords of former employees from the database, former employees cannot enter as well. Finally, by doing most of the processing server side, it is hard for crackers to steal extra information.

## Protocol Procedure

1. Employee's fingerprint, QR code, and access times registered in database and QR code card given to employee
2. Employee drives to security gate
3. Employee puts finger on fingerprint scanner and scans QR code on QR code scanner
4. Fingerprint, QR code, and timestamp sent to the server
5. Server hashs QR code with SHA-256 and compares it to hash in database
6. If the hashs match, the time period is ok, and fingerprint is in confidence interval, server sends back unique server hash (not password hash), and yes or no result. If server hash matches (to confirm that the gate is not being given verification data from a foreign source), and the result is yes, access is provided.

## Simple Implementation

Since it will be difficult to implement a method to analyze and convert fingerprints to numbers, I have only implemented the hashing of the password using SHA-256 using the pycrpyto library in python.

    from Crypto.Hash import SHA256
    hash = SHA256.new()
    hash.update('message')
    hash.digest()

This code uses the `Crypto.Hash` library to hash the password using SHA-256. The resulting hash can then be compared to the hash of the password stored in the database, and send back the results to the security gate.

