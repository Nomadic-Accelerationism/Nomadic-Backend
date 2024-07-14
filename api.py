from flask import Flask, jsonify, request
from web3 import Web3

import requests, json
app = Flask(__name__)

#######################################################################################################################

@app.route("/")
def helloworld():
    return 'N/ACC'
    
#######################################################################################################################
    
@app.route('/poaps', methods=['GET'])
def get_poaps():
    WALLET_ADDRESS = request.args.get('wallet')
    WALLET_ADDRESS = WALLET_ADDRESS.lower()
    if not WALLET_ADDRESS:
        return jsonify({'error': 'Wallet address is required'}), 400
    
    GRAPHQL_URL = 'https://gateway-arbitrum.network.thegraph.com/api/6e8591f9d4a459d9b6a2d2214f20d6b5/subgraphs/id/41xbTurY2KEHZdwFYPXAZTgRL8n4Cf3RfV3X4GSuUckp'
    EVENT_IDS = ["175480","174403","173047","171820","169518","167539","166438","160005","157551","155332","148642","146194","140955","128160","124806","111991","107011","99467","95087","85155","80122","70986","63400","57318","53153","47144","42068","36528","30875","25149","15916"]
    EVENT_IDS_STRING = json.dumps(EVENT_IDS)
    query = '''
    {
        tokens(where: {owner: "''' + WALLET_ADDRESS + '''", event_in: ''' + EVENT_IDS_STRING + '''}) {
            id
            owner {
                id
            }
            event {
                id
            }
        }
    }
    '''
    
    response = requests.post(GRAPHQL_URL, json={'query': query})
    if response.status_code == 200:
        data = response.json()['data']
        tokens = data['tokens']
        #total_events = data['tokensConnection']['aggregate']['count']
        tokens_count = len(data['tokens'])
        return jsonify({'tokens': tokens, 'tokensCount': tokens_count})
    else:
        return jsonify({'error': 'Failed to fetch data from The Graph'}), 500


#######################################################################################################################


def is_holder(wallet_address, contract_address):
    url = f"{'https://eth-mainnet.alchemyapi.io/v2/pGYy75CP_bnPTpplzZngCWOJ9C_uDQYz'}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenBalances",
        "params": [wallet_address, [contract_address]],
        "id": 1
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        result = response.json().get('result', {})
        token_balances = result.get('tokenBalances', [])
        for token in token_balances:
            balance = int(token.get('tokenBalance', '0x0'), 16)
            if balance > 0:
                return 1
    return 0

@app.route('/check_ape', methods=['GET'])
def check_holder_endpoint():
    wallet_address = request.args.get('wallet')
    wallet_address = wallet_address.lower()
    if not wallet_address:
        return jsonify({'error': 'Wallet address is required'}), 400
    
    bored_ape_contract = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"
    mutant_ape_contract = "0x60e4d786628fea6478f785a6d7e704777c86a7c6"

    is_bored_ape_holder = is_holder(wallet_address, bored_ape_contract)
    is_mutant_ape_holder = is_holder(wallet_address, mutant_ape_contract)

    return jsonify({
        'wallet': wallet_address,
        'is_ape_holder': is_bored_ape_holder+is_mutant_ape_holder 
    })	

#######################################################################################################################

@app.route('/prove', methods=['GET'])
def prove():
    url = request.args.get('url')
    #url = request.args.get('url', 'https://api.talentprotocol.com/api/v2/passports/0xc2564e41B7F5Cb66d2d99466450CfebcE9e8228f')
    # Aquí puedes agregar la lógica para el filtro de registro
    # await set_logging_filter('info,tlsn_extension_rs=debug')
    
    response = requests.get(url)
    proof = {
        'status_code': response.status_code,
        'headers': dict(response.headers),
        'content': response.content.decode('utf-8')
    }
    
    return jsonify(proof)

@app.route('/verify', methods=['POST'])
def verify():
    proof = request.json
    # Aquí puedes agregar la lógica para verificar la prueba
    # Por simplicidad, este ejemplo solo regresa la prueba sin cambios
    
    result = {
        'verification': 'success',  # Placeholder para el resultado de la verificación
        'proof': proof
    }
    
    return jsonify(result)

#######################################################################################################################

@app.route('/hold_nouns', methods=['GET'])
def get_token_balance():
    wallet_address = request.args.get('wallet')
    wallet_address = wallet_address.lower()
    if not wallet_address:
        return jsonify({'error': 'Wallet address is required'}), 400
    
    nouns_contract = "0x5c1760c98be951A4067DF234695c8014D8e7619C"
    
    is_nouns_holder = is_holder(wallet_address, nouns_contract)
    
    return jsonify({
        'wallet': wallet_address,
        'is_nouns_holder': is_nouns_holder
    })	

#######################################################################################################################

@app.route('/getAge', methods=['GET'])
def get_age():
    wallet_address = request.args.get('wallet')
    wallet_address = wallet_address.lower()
    if not wallet_address:
        return jsonify({'error': 'Wallet address is required'}), 400
    
    
    abi = str('[ {  "inputs": [   {    "internalType": "address",    "name": "_owner",    "type": "address"   },   {    "internalType": "uint32",    "name": "_age",    "type": "uint32"   },   {    "internalType": "bytes32",    "name": "_poap",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_nouns",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_ape",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_talent",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_financial",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_identity",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_farcaster",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "_ens",    "type": "bytes32"   }  ],  "name": "createHacker",  "outputs": [],  "stateMutability": "nonpayable",  "type": "function" }, {  "inputs": [   {    "internalType": "address",    "name": "_owner",    "type": "address"   }  ],  "name": "getHacker",  "outputs": [   {    "components": [     {      "internalType": "eaddress",      "name": "owner",      "type": "uint256"     },     {      "internalType": "euint32",      "name": "age",      "type": "uint256"     },     {      "internalType": "bytes32",      "name": "poap",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "nouns",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "ape",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "talent",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "financial",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "identity",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "farcaster",      "type": "bytes32"     },     {      "internalType": "bytes32",      "name": "ens",      "type": "bytes32"     }    ],    "internalType": "struct Users.NewHacker",    "name": "",    "type": "tuple"   }  ],  "stateMutability": "view",  "type": "function" }, {  "inputs": [   {    "internalType": "eaddress",    "name": "",    "type": "uint256"   }  ],  "name": "hackers",  "outputs": [   {    "internalType": "eaddress",    "name": "owner",    "type": "uint256"   },   {    "internalType": "euint32",    "name": "age",    "type": "uint256"   },   {    "internalType": "bytes32",    "name": "poap",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "nouns",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "ape",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "talent",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "financial",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "identity",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "farcaster",    "type": "bytes32"   },   {    "internalType": "bytes32",    "name": "ens",    "type": "bytes32"   }  ],  "stateMutability": "view",  "type": "function" }]')

    web3 = Web3(Web3.HTTPProvider(' https://api.helium.fhenix.zone'))

    account_from = {
        'private_key': '76e4b8a2744ed6d43c96e08b8bec53860f71367',
        'address': '0x86300E0a857aAB39A601E89b0e7F15e1488d9F0C',
    }
    
    contract_address = '0x4fb57d05994f6D41792E42FB147D4F40426cDad2'
    ejecutador = web3.eth.contract(address=contract_address, abi=abi)

    la_transaccion = ejecutador.functions.createHacker().build_transaction(
    {
	    'gasPrice': 1,
	    'from': account_from['address'],
	    'nonce': web3.eth.get_transaction_count(account_from['address']),
    }
    )


    tx_create = web3.eth.account.sign_transaction(la_transaccion, account_from['private_key'])


    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)


    return jsonify({
        'wallet': wallet_address,
        'tx_hash': tx_hash
    })	


#######################################################################################################################
if __name__ == "__main__":
    app.run()
    
