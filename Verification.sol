// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateVerificationSystem {
    address public admin;

    struct Certificate {
        uint256 id;           // Unique ID for the certificate
        string recipientName; // Name of the certificate holder
        string issueDate;     // Date the certificate was issued
        address issuedBy;     // Address of the admin who issued the certificate
        bool isValid;         // Status of the certificate
    }

    // Store certificates by their ID
    mapping(uint256 => Certificate) public certificates;
    uint256 public certificateCount;

    // Constructor to set the admin
    constructor() {
        admin = msg.sender; // The deployer of the contract is the admin
    }

    // Function to issue a new certificate
    function issueCertificate(string memory _recipientName, string memory _issueDate) public {
        require(msg.sender == admin, "Only the admin can issue certificates");

        certificateCount++; // Increment certificate ID
        certificates[certificateCount] = Certificate({
            id: certificateCount,
            recipientName: _recipientName,
            issueDate: _issueDate,
            issuedBy: msg.sender,
            isValid: true
        });
    }

    // Function to verify a certificate by its ID
    function verifyCertificate(uint256 _certificateId) public view returns (bool) {
        require(_certificateId > 0 && _certificateId <= certificateCount, "Certificate does not exist");
        return certificates[_certificateId].isValid;
    }

    // Function to fetch certificate details by ID
    function getCertificateDetails(uint256 _certificateId)
        public
        view
        returns (string memory, string memory, address, bool)
    {
        require(_certificateId > 0 && _certificateId <= certificateCount, "Certificate does not exist");

        Certificate memory cert = certificates[_certificateId];
        return (
            cert.recipientName,
            cert.issueDate,
            cert.issuedBy,
            cert.isValid
        );
    }

    // Function to invalidate a certificate
    function invalidateCertificate(uint256 _certificateId) public {
        require(msg.sender == admin, "Only the admin can invalidate certificates");
        require(_certificateId > 0 && _certificateId <= certificateCount, "Certificate does not exist");
        require(certificates[_certificateId].isValid, "Certificate is already invalid");

        certificates[_certificateId].isValid = false;
    }
}
