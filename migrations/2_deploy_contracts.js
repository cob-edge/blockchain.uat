var IoT = artifacts.require("./IoT.sol");

module.exports = function(deployer) {
  deployer.deploy(IoT);
};
