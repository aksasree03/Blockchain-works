pragma solidity ^0.8.0;
contract Calculator {
 function add(uint256 a, uint256 b) public pure returns (uint256) {
 return a + b;
 }
 function subtract(uint256 a, uint256 b) public pure returns (uint256) {
 require(a >= b, "Subtraction overflow");
 return a - b;
 }
 function multiply(uint256 a, uint256 b) public pure returns (uint256) {
 return a * b;
 }
 function divide(uint256 a, uint256 b) public pure returns (uint256) {
 require(b != 0, "Division by zero");
 return a / b;
 }
 function modulo(uint256 a, uint256 b) public pure returns (uint256) {
 require(b != 0, "Modulo by zero");
 return a % b;
 }
 function square(uint256 a) public pure returns (uint256) {
 return a * a;
 }
}