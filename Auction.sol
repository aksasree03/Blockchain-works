// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuctionPlatform {
    address public auctionOwner;
    uint256 public auctionEndTime;
    bool public auctionEnded;

    struct Auction {
        string itemName;        // Name of the item
        uint256 startingPrice;  // Initial price of the item
        uint256 highestBid;     // Highest bid so far
        address highestBidder;  // Address of the highest bidder
    }

    Auction public auction;

    mapping(address => uint256) public pendingReturns;

    // Events
    event AuctionStarted(string itemName, uint256 startingPrice, uint256 endTime);
    event NewHighestBid(address indexed bidder, uint256 bidAmount);
    event AuctionEnded(address winner, uint256 amount);

    // Modifier to check if the auction is ongoing
    modifier onlyDuringAuction() {
        require(block.timestamp < auctionEndTime, "Auction has ended");
        _;
    }

    // Modifier to check if the auction is over
    modifier onlyAfterAuction() {
        require(block.timestamp >= auctionEndTime, "Auction is still ongoing");
        _;
    }

    // Modifier to check if only the owner can call certain functions
    modifier onlyOwner() {
        require(msg.sender == auctionOwner, "Only the auction owner can call this");
        _;
    }

    // Start an auction
    function startAuction(string memory _itemName, uint256 _startingPrice, uint256 _durationInMinutes) public {
        require(auctionEndTime == 0 || auctionEnded, "An auction is already ongoing");

        auctionOwner = msg.sender;
        auction = Auction({
            itemName: _itemName,
            startingPrice: _startingPrice,
            highestBid: 0,
            highestBidder: address(0)
        });

        auctionEndTime = block.timestamp + (_durationInMinutes * 1 minutes);
        auctionEnded = false;

        emit AuctionStarted(_itemName, _startingPrice, auctionEndTime);
    }

    // Place a bid
    function placeBid() public payable onlyDuringAuction {
        require(msg.value > auction.highestBid, "Your bid must be higher than the current highest bid");
        require(msg.value >= auction.startingPrice, "Your bid must be at least the starting price");

        // Refund the previous highest bidder
        if (auction.highestBidder != address(0)) {
            pendingReturns[auction.highestBidder] += auction.highestBid;
        }

        // Update the highest bid and bidder
        auction.highestBid = msg.value;
        auction.highestBidder = msg.sender;

        emit NewHighestBid(msg.sender, msg.value);
    }

    // Withdraw funds (for bidders who were outbid)
    function withdraw() public {
        uint256 amount = pendingReturns[msg.sender];
        require(amount > 0, "No funds to withdraw");

        pendingReturns[msg.sender] = 0;

        payable(msg.sender).transfer(amount);
    }

    // End the auction and declare the winner
    function endAuction() public onlyOwner onlyAfterAuction {
        require(!auctionEnded, "Auction has already been ended");

        auctionEnded = true;

        emit AuctionEnded(auction.highestBidder, auction.highestBid);

        // Transfer the highest bid amount to the auction owner
        if (auction.highestBid > 0) {
            payable(auctionOwner).transfer(auction.highestBid);
        }
    }

    // Get auction details
    function getAuctionDetails() public view returns (string memory, uint256, uint256, address, uint256) {
        return (
            auction.itemName,
            auction.startingPrice,
            auction.highestBid,
            auction.highestBidder,
            auctionEndTime
        );
    }
}
