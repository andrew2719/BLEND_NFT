from scripts.helpful_scripts import get_account


def create_nft(recepient_address, account, blendtoken,token_uri):
    txn = blendtoken.createNFT(recepient_address, token_uri, {"from": account})
    txn.wait(1)
    print("NFT created!for the recepient address", recepient_address)