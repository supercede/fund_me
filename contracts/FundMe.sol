// SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;

    AggregatorV3Interface internal priceFeed;
    address public owner;
    address[] public funders;

    constructor(address _priceFeed) public {
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    mapping(address => uint256) public fundersMap;

    function fund () public payable {
        // Require a minimum of 10 dollars
        uint256 minimumUSD = 10 * 10 ** 18; // Multiplier for ETH to Wei
        require(getConversionRate(msg.value) >= minimumUSD, "More ETH is required for this transaction");
        fundersMap[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion () public view returns (uint) {
        return priceFeed.version();
    }

    function decimals () public view returns (uint256) {
        return uint256(priceFeed.decimals());
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer,,,) = priceFeed.latestRoundData();
        uint256 decimalPlaces = decimals(); 

        // 1 ETH = 10**18 Wei, convert
        return uint256(answer) * (uint256(10)**(18 - decimalPlaces));
    }
 
    function getConversionRate(uint256 ethInWei) public view returns (uint256) {
        uint256 ethPrice = getPrice();

        uint256 ethInUSD = (ethPrice * ethInWei)/(10**(18));

        // returned value is divided by 10^18 to get actual value in ETH/USD
        // 1000000000 Wei(1 Gwei) =  3100190000000
        // divided by 10^18 = 0.00000310019 USD (* 10^ 9 = 3,100.19 USD for 1 ETH/1000000000 Gwei)
        return ethInUSD;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public onlyOwner payable {
        msg.sender.transfer(address(this).balance); // send contract balance
        for(uint i = 0; i < funders.length; i++) {
            address funderAddress = funders[i];
            fundersMap[funderAddress] = 0;
        }

        funders = new address[](0);
    }
}