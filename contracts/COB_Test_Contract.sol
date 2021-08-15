pragma solidity ^0.5.1;

contract ERC20Token
{
    mapping(address => uint256) public balance;
    
    function mint() public
    {
        balance[tx.origin] ++;
    }
}

contract COB_Test_Contract 
{
    uint256 private uCount;
    
    mapping(uint => User) public users;
    mapping(address => uint256) public balance;
    
    address payable wallet;
    address public token;
    
    constructor(address payable _wallet, address _token) public
    {
        wallet = _wallet;
        token = _token;
    }
    
    function() external payable
    {
        purchaseToken();
    }
    
    function purchaseToken() public payable
    {
        balance[msg.sender] += 1;
        
        wallet.transfer(msg.value);
    }
    
    struct User
    {
        uint id;
        string firstName;
        string surname;
    }
    
    function addUser(string memory firstName, string memory surname) public
    {  
        users[uCount] = User(uCount, firstName, surname);
        incUserCount();
    }
    
    function getUserCount() public view returns(uint)
    {
        return uCount;
    }
    
    function incUserCount() internal
    {
        uCount++;
    }
}