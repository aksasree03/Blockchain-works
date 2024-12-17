// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskManagementSystem {
    struct Task {
        uint256 id;
        string description;
        address assignee;
        bool isCompleted;
    }

    address public admin;
    uint256 public taskCounter;

    mapping(uint256 => Task) public tasks; // Map task ID to Task struct

    // Events
    event TaskCreated(uint256 taskId, string description, address assignee);
    event TaskCompleted(uint256 taskId, address assignee);

    // Modifier to ensure only admin can call certain functions
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }

    // Modifier to ensure only the assignee can complete the task
    modifier onlyAssignee(uint256 taskId) {
        require(tasks[taskId].assignee == msg.sender, "Only the assigned user can complete this task");
        _;
    }

    // Constructor to set the admin as the contract deployer
    constructor() {
        admin = msg.sender;
    }

    // Function to create a new task
    function createTask(string memory _description, address _assignee) public onlyAdmin {
        taskCounter++;
        tasks[taskCounter] = Task(taskCounter, _description, _assignee, false);
        emit TaskCreated(taskCounter, _description, _assignee);
    }

    // Function to mark a task as completed
    function markTaskCompleted(uint256 _taskId) public onlyAssignee(_taskId) {
        Task storage task = tasks[_taskId];
        require(!task.isCompleted, "Task is already completed");

        task.isCompleted = true;
        emit TaskCompleted(_taskId, msg.sender);
    }

    // Function to retrieve task details by ID
    function getTaskDetails(uint256 _taskId) public view returns (uint256, string memory, address, bool) {
        Task memory task = tasks[_taskId];
        return (task.id, task.description, task.assignee, task.isCompleted);
    }
}
