from scripts.helpful_scripts import get_account
from brownie import BLENDToken, accounts, config, network,web3
import os


sample_token_uri = "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/sepolia/{}/{}"

# def main():
#     account = get_account()
#     simple_collectible = SimpleCollectible.deploy({"from": account})
#     print(simple_collectible)
#     tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
#     tx.wait(1)
#     print("Collectible created!")
#     # to_lower_case_address = simple_collectible.address.lower()
#     print(OPENSEA_URL.format(simple_collectible.address.lower(), simple_collectible.tokenCounter() - 1))

def simple_trx(account, blendtoken):

    intital_balance = account.balance()
    print("Initial balance of the account", intital_balance)
    recepient_address = "0x279cD178c18a1cBc4618dDDddf59c1109Cdf5c5e"

    txn = blendtoken.createNFT(recepient_address, sample_token_uri, {"from": account})
    txn.wait(1)
    print("NFT created! 1")


    print("Balance of the account", account.balance())

    #pint the balance of the account
    


def deploy_simple_storage():

    minting_account = get_account()
    # account = accounts[0]
    # print(account)

    blendtoken = BLENDToken.deploy({"from": minting_account})
    print(blendtoken)

    simple_trx(minting_account, blendtoken)

    
    

def main():
    # deploy_simple_storage()
    # get the nfts that are linked to the recepient address
    account = get_account()
    blendsmartcontract_address = "0x0A4a0f85C4451617D841Cc4f1305116416dAA8Fc"
    blendtoken = BLENDToken.at(blendsmartcontract_address) # at is used to get the contract instance
    print(type(blendtoken))
    recepient_address = "0x279cD178c18a1cBc4618dDDddf59c1109Cdf5c5e"
    token_ids = blendtoken.getTokenIdsByOwner(recepient_address)
    print(type(token_ids))

    for token_id in token_ids:
        token_uri = blendtoken.tokenURI(token_id)
        print(token_uri)

    print(type(BLENDToken))