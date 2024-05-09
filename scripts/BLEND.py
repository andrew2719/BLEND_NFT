from brownie import BLENDToken, accounts, config, network, web3
from flask import Flask, request, jsonify
from scripts.helpful_scripts import get_account
import aioipfs
import asyncio
import requests, json

app = Flask(__name__)

class BLEND:
    def __init__(self):
        self.blendtoken = BLENDToken.at("0x0A4a0f85C4451617D841Cc4f1305116416dAA8Fc")
        self.minter_account = get_account()

    def mint_token(self, recepient_address,token_uri):
        try:
            txn = self.blendtoken.createNFT(recepient_address, token_uri, {"from": self.minter_account})
            txn.wait(1)
            return True
        except:
            return False
            
class IPFSHandler:
    def get_ipfs_data(self, ipfs_uri):
        try:
            response = requests.get(ipfs_uri)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()  # Directly parse the JSON data from the response
        except requests.RequestException as e:
            print(f"HTTP Request failed: {e}")
            return None

class QueryBLEND(BLEND):
    def __init__(self, recipient_address):
        super().__init__()
        self.recipient_address = recipient_address
        self.ipfs_handler = IPFSHandler()
        print(self.blendtoken)

    def get_token_ids(self):
        return self.blendtoken.getTokenIdsByOwner(self.recipient_address)

    def get_token_uri(self, token_id):
        return self.blendtoken.tokenURI(token_id)
    
    def get_token_ids_and_uris(self):
        token_ids = self.blendtoken.getTokenIdsByOwner(self.recipient_address)
        token_uris = [self.blendtoken.tokenURI(token_id) for token_id in token_ids]
        return list(zip(token_ids, token_uris))
    
    def get_token_ids_and_uris_with_details(self):
        token_ids = self.blendtoken.getTokenIdsByOwner(self.recipient_address)
        tokens_with_details = []
        for token_id in token_ids:
            uri = self.blendtoken.tokenURI(token_id)
            details = self.ipfs_handler.get_ipfs_data(uri)
            tokens_with_details.append((token_id, uri, details))
        return tokens_with_details

@app.before_request
def create_event_loop():
    if not hasattr(asyncio, '_current_loop'):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

@app.teardown_request
def close_event_loop(exception=None):
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.close()
    asyncio.set_event_loop(None)

@app.route("/minttoken/<token_uri>", methods=['POST'])
def mint_token(token_uri):
    print(token_uri)
    data = request.get_json()
    recipient_address = data['recipient_address']
    print(recipient_address)
    blend = BLEND()
    # add https://ipfs.io/ipfs/ to the token_uri
    token_uri = "https://ipfs.io/ipfs/" + token_uri
    return jsonify({"status": blend.mint_token(recipient_address, token_uri)})



@app.route('/getTokenIds/<recipient_address>', methods=['GET'])
def get_token_ids(recipient_address):
    print(recipient_address)
    query = QueryBLEND(recipient_address)
    # print(query.get_token_ids())
    return jsonify(query.get_token_ids())

# @app.route('/getTokenDetails/<recipient_address>', methods=['GET'])
# def get_token_details(recipient_address):
#     query = QueryBLEND(recipient_address)
#     details = query.get_token_ids_and_uris()
#     return jsonify(details)

@app.route('/getTokenDetails/<recipient_address>', methods=['GET'])
def get_token_details(recipient_address):
    query = QueryBLEND(recipient_address)
    details = query.get_token_ids_and_uris_with_details()
    return jsonify(details)

def main():
    app.run(debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)