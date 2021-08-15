pragma solidity ^0.5.1;

contract Counter
{
    uint256 counter = 0;
    
    function increase() public
    {
        counter++;
    }
    
    function decrease() public
    {
        counter--;
    }
    
    function getCount() public view returns(uint256)
    {
        return counter;
    }
}