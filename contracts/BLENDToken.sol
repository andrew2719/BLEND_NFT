// SPDX-License-Identifier: MIT
pragma solidity >=0.4.0 <0.9.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";

contract BLENDToken is ERC721URIStorage {

    uint256 public tokenCounter;
    constructor () public ERC721("BLENDToken", "BLEND") {
        tokenCounter = 0;
    }

    function createNFT(address to,string memory tokenURI) public returns (uint256){
        uint256 newItemId = tokenCounter;
        _safeMint(to, newItemId);   
        _setTokenURI(newItemId, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newItemId;

    }

    function getTokenIdsByOwner(address owner) public view returns (uint256[] memory) {
        uint256 balance = balanceOf(owner);
        uint256[] memory tokenIds = new uint256[](balance);
        uint256 index = 0;

        for (uint256 i = 0; i < tokenCounter; i++) {
            if (IERC721(address(this)).ownerOf(i) == owner) {
                tokenIds[index] = i;
                index++;
            }
        }

        return tokenIds;
    }
}