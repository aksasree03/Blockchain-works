pragma solidity ^0.8.0;

contract BSNLEmployeeSystem {
    // Employee structure
    struct Employee {
        string name;
        uint256 id;
    }

    // Customer structure
    struct Customer {
        string name;
        uint256 id;
        string phone;
        string simType; // Prepaid or Postpaid
        bool accessGranted; // Access to SIM card
    }

    // State variables
    Employee public employee;
    Customer[] public customers;

    // Modifier to ensure valid SIM type
    modifier validSimType(string memory simType) {
        require(
            keccak256(abi.encodePacked(simType)) == keccak256(abi.encodePacked("Prepaid")) ||
                keccak256(abi.encodePacked(simType)) == keccak256(abi.encodePacked("Postpaid")),
            "Invalid SIM type! Must be 'Prepaid' or 'Postpaid'."
        );
        _;
    }

    // Register the employee
    function registerEmployee(string memory name, uint256 id) public {
        employee = Employee(name, id);
    }

    // Register a customer
    function registerCustomer(
        string memory name,
        uint256 id,
        string memory phone,
        string memory simType
    ) public validSimType(simType) {
        customers.push(Customer(name, id, phone, simType, true));
    }

    // Get details of a specific customer
    function getCustomer(uint256 index)
        public
        view
        returns (
            string memory name,
            uint256 id,
            string memory phone,
            string memory simType,
            bool accessGranted
        )
    {
        require(index < customers.length, "Customer index out of range.");
        Customer memory customer = customers[index];
        return (customer.name, customer.id, customer.phone, customer.simType, customer.accessGranted);
    }

    // Get the total number of customers
    function getCustomerCount() public view returns (uint256) {
        return customers.length;
    }
}
