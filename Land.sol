pragma solidity ^0.8.0;

contract LandRegistry {
    struct Land {
        uint256 id;
        string location;
        uint256 price;
        address owner;
    }

    mapping(uint256 => Land) public lands;
    uint256 public landCount;

    event LandRegistered(uint256 id, string location, uint256 price, address owner);
    event OwnershipTransferred(uint256 id, address previousOwner, address newOwner);

    // Function to register land with dynamic users
    function registerLand(
        uint256 id,
        string memory location,
        uint256 price
    ) public {
        require(lands[id].id == 0, "Land ID already exists"); // Ensure ID is unique
        landCount++;
        lands[id] = Land(id, location, price, msg.sender); // msg.sender is the owner
        emit LandRegistered(id, location, price, msg.sender);
    }

    // Function to claim ownership of a registered land
    function claimOwnership(uint256 id) public {
    // Check if the land exists
    require(lands[id].id != 0, "Land does not exist");

    // Check if the caller is not already the owner
    require(lands[id].owner != msg.sender, "You already own this land");

    // Ensure the land has a valid owner
    address previousOwner = lands[id].owner;
    require(previousOwner != address(0), "Land has no current owner");

    // Transfer ownership to the caller
    lands[id].owner = msg.sender;

    // Emit an event for the ownership transfer
    emit OwnershipTransferred(id, previousOwner, msg.sender);
    }



    // Function to retrieve details of a specific land
    function getLand(uint256 id)
        public
        view
        returns (uint256, string memory, uint256, address)
    {
        require(lands[id].id != 0, "Land does not exist"); // Ensure land exists
        Land memory land = lands[id];
        return (land.id, land.location, land.price, land.owner);
    }
}
