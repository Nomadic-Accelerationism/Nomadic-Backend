from flask import Flask, jsonify, request
import requests 
import json
app = Flask(__name__)



@app.route("/")
def helloworld():
	return 'N/ACC'
	

	
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
	
if __name__ == "__main__":
	app.run()
	
