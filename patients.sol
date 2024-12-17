// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientManagement {
    struct Patient {
        uint id;
        string name;
        uint age;
        string phoneNumber;
        string disease;
        string appointmentTime;
        string prescription;
    }

    mapping(uint => Patient) private patients; // Map patient ID to Patient details
    uint private patientCounter; // Counter for unique patient IDs

    event PatientRegistered(uint patientId, string name, uint age, string phoneNumber);
    event AppointmentBooked(uint patientId, string disease, string appointmentTime);
    event PrescriptionAdded(uint patientId, string prescription);

    // Register a new patient
    function registerPatient(string memory name, uint age, string memory phoneNumber) public returns (uint) {
        patientCounter++;
        patients[patientCounter] = Patient(patientCounter, name, age, phoneNumber, "", "", "");
        emit PatientRegistered(patientCounter, name, age, phoneNumber);
        return patientCounter; // Return the new patient ID
    }

    // Add disease and appointment time for a patient
    function addAppointmentDetails(uint patientId, string memory disease, string memory appointmentTime) public {
        require(patientId > 0 && patientId <= patientCounter, "Invalid patient ID");
        Patient storage patient = patients[patientId];
        patient.disease = disease;
        patient.appointmentTime = appointmentTime;
        emit AppointmentBooked(patientId, disease, appointmentTime);
    }

    // Add a prescription for a patient
    function addPrescription(uint patientId, string memory prescription) public {
        require(patientId > 0 && patientId <= patientCounter, "Invalid patient ID");
        Patient storage patient = patients[patientId];
        patient.prescription = prescription;
        emit PrescriptionAdded(patientId, prescription);
    }

    // Retrieve patient details
    function getPatientDetails(uint patientId) public view returns (
        uint id,
        string memory name,
        uint age,
        string memory phoneNumber,
        string memory disease,
        string memory appointmentTime,
        string memory prescription
    ) {
        require(patientId > 0 && patientId <= patientCounter, "Invalid patient ID");
        Patient storage patient = patients[patientId];
        return (
            patient.id,
            patient.name,
            patient.age,
            patient.phoneNumber,
            patient.disease,
            patient.appointmentTime,
            patient.prescription
        );
    }
}
