// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CrowdfundingPlatform {
    
    struct Campaign {
        string name;
        uint256 goal;           // Funding goal
        uint256 deadline;      // End of campaign (timestamp)
        address creator;       // Creator of the campaign
        uint256 totalContributions; // Total amount contributed
        bool withdrawn;        // Whether funds have been withdrawn
    }
    
    mapping(uint256 => Campaign) public campaigns; // Map campaign IDs to Campaigns
    uint256 public campaignCount; // Unique campaign counter

    // Create a new campaign
    function startCampaign(string memory _name, uint256 _goal, uint256 _durationInDays) public returns (uint256) {
        require(_goal > 0, "Funding goal must be greater than 0");
        require(_durationInDays > 0, "Duration must be at least 1 day");

        campaignCount++;
        uint256 deadline = block.timestamp + (_durationInDays * 1 days);
        
        campaigns[campaignCount] = Campaign({
            name: _name,
            goal: _goal,
            deadline: deadline,
            creator: msg.sender,
            totalContributions: 0,
            withdrawn: false
        });

        return campaignCount; // Return the new campaign ID
    }

    // Contribute funds to a specific campaign
    function contribute(uint256 _campaignId) public payable {
        require(msg.value > 0, "Contribution amount must be greater than 0");
        require(block.timestamp < campaigns[_campaignId].deadline, "The campaign deadline has passed");

        campaigns[_campaignId].totalContributions += msg.value;
    }

    // Allow the campaign creator to withdraw funds if goal is met and deadline has passed
    function withdrawFunds(uint256 _campaignId) public {
        Campaign storage campaign = campaigns[_campaignId];

        require(msg.sender == campaign.creator, "Only the campaign creator can withdraw funds");
        require(block.timestamp >= campaign.deadline, "Cannot withdraw before the deadline");
        require(campaign.totalContributions >= campaign.goal, "Funding goal has not been met");
        require(!campaign.withdrawn, "Funds have already been withdrawn");

        campaign.withdrawn = true;
        payable(campaign.creator).transfer(campaign.totalContributions);
    }

    // Fetch details about a specific campaign
    function getCampaignDetails(uint256 _campaignId) public view returns (
        string memory,
        uint256,
        uint256,
        address,
        uint256,
        bool
    ) {
        Campaign memory campaign = campaigns[_campaignId];
        return (
            campaign.name,
            campaign.goal,
            campaign.deadline,
            campaign.creator,
            campaign.totalContributions,
            campaign.withdrawn
        );
    }
}
