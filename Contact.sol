// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LandRegistry {
    struct Land {
        string location;
        uint256 price;
        address owner;
    }

    mapping(uint256 => Land) public lands;
    uint256 public landCount;

    // Events
    event LandRegistered(uint256 indexed landId, string location, uint256 price, address owner);
    event OwnershipTransferred(uint256 indexed landId, address indexed previousOwner, address indexed newOwner);
    event PriceUpdated(uint256 indexed landId, uint256 oldPrice, uint256 newPrice);
    event LandDeleted(uint256 indexed landId);

    // Register a new land
    function registerLand(string memory location, uint256 price) public {
        require(bytes(location).length > 0, "Location cannot be empty.");
        require(price > 0, "Price must be greater than zero.");

        landCount++;
        lands[landCount] = Land(location, price, msg.sender);

        emit LandRegistered(landCount, location, price, msg.sender);
    }

    // Transfer ownership of a land
    function transferOwnership(uint256 id, address newOwner) public {
        require(id > 0 && id <= landCount, "Invalid land ID.");
        require(newOwner != address(0), "New owner address cannot be zero.");
        require(msg.sender == lands[id].owner, "Only the owner can transfer ownership.");

        address previousOwner = lands[id].owner;
        lands[id].owner = newOwner;

        emit OwnershipTransferred(id, previousOwner, newOwner);
    }

    // Get details of a land
    function getLand(uint256 id) public view returns (string memory, uint256, address) {
        require(id > 0 && id <= landCount, "Invalid land ID.");
        Land memory land = lands[id];
        return (land.location, land.price, land.owner);
    }

    // Check if an address owns a specific land
    function isOwner(uint256 id, address account) public view returns (bool) {
        require(id > 0 && id <= landCount, "Invalid land ID.");
        return lands[id].owner == account;
    }

    // Update the price of a land
    function updatePrice(uint256 id, uint256 newPrice) public {
        require(id > 0 && id <= landCount, "Invalid land ID.");
        require(newPrice > 0, "Price must be greater than zero.");
        require(msg.sender == lands[id].owner, "Only the owner can update the price.");

        uint256 oldPrice = lands[id].price;
        lands[id].price = newPrice;

        emit PriceUpdated(id, oldPrice, newPrice);
    }

    // Delete a land record
    function deleteLand(uint256 id) public {
        require(id > 0 && id <= landCount, "Invalid land ID.");
        require(msg.sender == lands[id].owner, "Only the owner can delete the land.");

        delete lands[id];

        emit LandDeleted(id);
    }
    // Structure to hold contact details
        struct Contact {
        string name;
        string phoneNumber;
        string email;
        uint256 timestamp; // Timestamp to track submission time
    }

    // Mapping to store contacts by unique IDs
    mapping(uint256 => Contact) public contacts;
    uint256 public contactCount = 0; // Counter for assigning unique IDs to contacts

    // Events
    event ContactAdded(uint256 indexed contactId, string name, string phoneNumber, string email, uint256 timestamp);

    /**
     * @dev Adds a new contact to the guestbook and assigns it a unique ID.
     * @param _name Name of the person submitting the contact details.
     * @param _phoneNumber Phone number of the person.
     * @param _email Email of the person.
     */
    function addContact(string memory _name, string memory _phoneNumber, string memory _email) public {
        // Validations
        require(bytes(_name).length > 0, "Name cannot be empty");
        require(bytes(_phoneNumber).length > 0, "Phone number cannot be empty");
        require(bytes(_email).length > 0, "Email cannot be empty");

        // Store the contact into the mapping
        contacts[contactCount] = Contact({
            name: _name,
            phoneNumber: _phoneNumber,
            email: _email,
            timestamp: block.timestamp
        });

        // Emit an event to notify external DApps about the new contact submission
        emit ContactAdded(contactCount, _name, _phoneNumber, _email, block.timestamp);

        // Increment the unique ID counter
        contactCount++;
    }

    /**
     * @dev Retrieves the contact details by unique ID.
     * @param id The unique contact ID.
     * @return name The name of the contact.
     * @return phoneNumber The phone number of the contact.
     * @return email The email address of the contact.
     * @return timestamp The timestamp when the contact was added.
     */
    function getContactById(uint256 id) public view returns (string memory name, string memory phoneNumber, string memory email, uint256 timestamp) {
        require(id < contactCount, "Invalid contact ID");
        Contact memory contact = contacts[id];
        return (contact.name, contact.phoneNumber, contact.email, contact.timestamp);
    }

    /**
     * @dev Retrieves all the contact IDs added so far.
     * @return A list of all contact IDs.
     */
    function getAllContactIds() public view returns (uint256[] memory) {
        uint256[] memory ids = new uint256[](contactCount);
        for (uint256 i = 1; i < contactCount; i++) {
            ids[i] = i;
        }
        return ids;
    }
}