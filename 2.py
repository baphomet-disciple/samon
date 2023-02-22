import os
import requests
import time
import urllib.parse
path = os.getcwd()
def get_access_token():
    cookies = {
        '__Host-MSAAUTHP': '-CaxtlNJQ8pPHigvhWCZ4DPY6vZZuoTSXHSCPxTh6CzDuiSdx61OxfT9jajvoeIUsqhcUJJ3FsOl!NVtvp8KeAk3uxRcn1eMI3nnCBYRBXN5Tptitb5fnlYSw702kuA1J01eM1t65gEtAwXez0sUwL*k*EKDB!KMbZtPqt0!z4odIMMI!GdV1Ts69R8Mwsxs8ONM*QY4BO8uVQsvn01Xe8JfNJYOGtjR*wwXtZFuu2l48RSktCzfGy0S6zWHBHbCptkXxqwItnFL9SuRnXdN0W7m2KhEzZnHewxLToVCTGX6r9yH!UGjS0geMa5tC8sxKoDdxni1leX7JrMgHKKlDN97QriYFMt4f!s9olCQXcsME9TLHkEu71NL1m*KquYcb0FHu1KG!*bXjfwIEJvIp0iJjbbobXYTxQUHknymSK78v3YGNeEC5gz0P*PZhFrtfgAiw5ocTYBgwmHfXpes*sodlpJlDbxbCkFDyPu3h94q2',
        'MSPAuth': 'Disabled',
    }

    headers = {
        'Host': 'login.live.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}

    params = {
        'response_type': 'token',
        'prompt': 'none',
        'redirect_uri': 'https://outlook.live.com/owa/auth/dt.aspx',
        'scope': 'liveprofilecard.access',
        'client_id': '292841',
    }

    response = requests.get(
        'https://login.live.com/oauth20_authorize.srf',
        params=params,
        cookies=cookies,
        headers=headers,
        allow_redirects=False
    )

    if response.status_code == 302:
        redirected_url = response.headers['Location'].split('&')
        redirected_url = str(redirected_url).split("=")[1]
        new_string = redirected_url.replace(", 'token_type", "").replace("'", "")
        access_token = urllib.parse.unquote(new_string)
    else:
        print('No redirect. Response Content:')

    with open(f'{path}/token.txt', 'w') as f:
        f.write(access_token)

    expiry_time_str = response.headers['Expires']
    expiry_time = time.mktime(time.strptime(expiry_time_str, '%a, %d %b %Y %H:%M:%S %Z'))

    return access_token, expiry_time

access_token, expiry_time = get_access_token()

while True:
    if time.time() >= expiry_time - 3600:
        access_token, expiry_time = get_access_token()
        print(access_token)
        print("Access token updated.")
    
    time.sleep(3600)
