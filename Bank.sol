// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BankingSystem {
    // Mapping to store the balance of each user
    mapping(address => uint256) private balances;

    // Event to log deposit activity
    event Deposit(address indexed user, uint256 amount);

    // Event to log withdrawal activity
    event Withdrawal(address indexed user, uint256 amount);

    // Function to deposit an amount into the user's account
    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        balances[msg.sender] += msg.value;
    }


    // Function to withdraw an amount from the user's account
    function withdraw(uint256 _amount) public {
        require(_amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        balances[msg.sender] -= _amount;

        // Transfer the amount to the user's wallet
        payable(msg.sender).transfer(_amount);

        emit Withdrawal(msg.sender, _amount);
    }

    // Function to check the remaining balance of the user
    function checkBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
