import os
from flask import Flask, jsonify
import requests
path = os.getcwd()
contact = "RgAAAABfHbmw4MfSRZMUycYK1tfrBwDuUbVZIV8yTrx5fTjtJ2VHAAIRAP2yAADuUbVZIV8yTrx5fTjtJ2VHAAIea2gsAAAA0"
app = Flask(__name__)
VALID_API_KEYS = ["api_key_1", "api_key_2", "api_key_3"]
def validate_api_key(api_key):
    if api_key in VALID_API_KEYS:
        return True
    else:
        return False
@app.route('/linkedin/<api_key>/email=<email>')
def get_linkedin_profile(api_key, email):
    if not validate_api_key(api_key):   
        return "Please provide a valid API key.", 401
    with open(f'{path}/token.txt') as file:
        token = file.read().replace('\n', '')
        headers = {
            'Host': 'apc-alt.loki.delve.office.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': 'text/plain, application/json, text/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json-patch+json',
            'X-Clienttype': 'OwaPeopleHub',
            'Authorization': f'Bearer {token}',
        }

        data = '{"id":"RgAAAABfHbmw4MfSRZMUycYK1tfrBwDuUbVZIV8yTrx5fTjtJ2VHAAIRAP2yAADuUbVZIV8yTrx5fTjtJ2VHAAIea2gsAAAA0","names":[],"emails":[{"id":"2","action":"PATCH","body":{"address":"old_email"}}],"phones":[],"addresses":[],"tags":[],"positions":[],"notes":[],"anniversaries":[],"relationships":[],"websites":[],"webAccounts":[],"putPhotos":[]}'
        data = data.replace("old_email", email)
        response = requests.patch('https://apc-alt.loki.delve.office.com/api/v1/peoplegraph/contact',headers=headers,data=data)
        headers = {
            'Host': 'apc-alt.loki.delve.office.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'text/plain;charset=UTF-8',
        }

        params = {
            'PersonaDisplayName': 'target',
            'ExternalPageInstance': '',
            'ContactId': f'{contact}',
            'ConvertGetPost': 'true',
        }

        data = '{"Accept":"text/plain, application/json, text/json","X-ClientType":"OwaMail","X-ClientFeature":"LivePersonaCard","X-ClientArchitectureVersion":"v1","X-ClientScenario":"PeopleHubEmbeddedEV","X-HostAppPlatform":"Web","X-LPCVersion":"1.20230129.2.1","authorization":"Bearer something","X-HostAppCapabilities":"{\\"isLokiContactDataDisabled\\":false}"}'
        data = data.replace("something", token)
        response = requests.post('https://apc-alt.loki.delve.office.com/api/v2/linkedin/profiles',params=params,headers=headers,data=data)
        match = response.json()['resultTemplate']
        if match == "ExactMatch":
            person = response.json()['persons'][0]
            keys = ["id", "displayName", "emails", "firstName", "lastName", "photoUrl", "linkedInUrl", "headline", "location"]
            response_data = {key: person.get(key, "NA") for key in keys}
            return jsonify(response_data), 200
        else:
            return f"{email} is not registered with LinkedIn.", 404
if __name__ == '__main__':
    app.run(debug=True)
