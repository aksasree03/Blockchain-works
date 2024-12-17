// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RentalAgreementManagement {
    struct RentalAgreement {
        uint256 id;
        address landlord;
        address tenant;
        uint256 rentAmount;
        bool isActive;
    }

    uint256 public agreementCounter;
    mapping(uint256 => RentalAgreement) public agreements;
    mapping(uint256 => uint256) public rentPayments; // Tracks total rent paid for each agreement

    event AgreementCreated(uint256 id, address landlord, address tenant, uint256 rentAmount);
    event RentPaid(uint256 id, address tenant, uint256 amount);
    event AgreementTerminated(uint256 id, address landlord);

    // Modifier to ensure only the landlord of an agreement can perform certain actions
    modifier onlyLandlord(uint256 _id) {
        require(agreements[_id].landlord == msg.sender, "Only landlord can perform this action");
        _;
    }

    // Modifier to ensure only the tenant of an agreement can pay rent
    modifier onlyTenant(uint256 _id) {
        require(agreements[_id].tenant == msg.sender, "Only tenant can perform this action");
        _;
    }

    // Function to create a rental agreement
    function createAgreement(address _tenant, uint256 _rentAmount) public {
        require(_tenant != address(0), "Invalid tenant address");
        require(_rentAmount > 0, "Rent amount must be greater than 0");

        agreementCounter++;
        agreements[agreementCounter] = RentalAgreement(agreementCounter, msg.sender, _tenant, _rentAmount, true);

        emit AgreementCreated(agreementCounter, msg.sender, _tenant, _rentAmount);
    }

    // Function for tenants to pay rent
    function payRent(uint256 _id) public payable onlyTenant(_id) {
        RentalAgreement memory agreement = agreements[_id];
        require(agreement.isActive, "Agreement is not active");
        require(msg.value >= agreement.rentAmount, "Insufficient rent amount");

        rentPayments[_id] += msg.value;

        emit RentPaid(_id, msg.sender, msg.value);
    }

    // Function to terminate the agreement by the landlord
    function terminateAgreement(uint256 _id) public onlyLandlord(_id) {
        RentalAgreement storage agreement = agreements[_id];
        require(agreement.isActive, "Agreement is already terminated");

        agreement.isActive = false;

        emit AgreementTerminated(_id, msg.sender);
    }

    // Function to get rental agreement details
    function getAgreementDetails(uint256 _id)
        public
        view
        returns (
            uint256,
            address,
            address,
            uint256,
            bool
        )
    {
        RentalAgreement memory agreement = agreements[_id];
        return (agreement.id, agreement.landlord, agreement.tenant, agreement.rentAmount, agreement.isActive);
    }
}
