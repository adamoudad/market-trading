import requests
import time
import jwt

class LiquidAPI:
    
    BASE_URL = "https://api.liquid.com"

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret

    def get_products(self, product_id=None):
        path = "%s/products" % self.BASE_URL
        path += "/" + product_id if product_id else ""
        return self._get(path)
        
    def _get(self, path, params={}):
        params.update({"recvWindow": 120000})
        url = "%s" % path
        header = self.generate_header(path)
        return requests.get(url, headers=header, \
            timeout=30, verify=True).json()

    def generate_header(self, path):
        auth_payload = {
            'path': path,
            'nonce': time.time() * 100,
            'token_id': self.token_id
        }
        signature = jwt.encode(auth_payload, self.secret, 'HS256')
        return {
            "X-Quoine-API-Version": "2",
            "X-Quoine-Auth": signature,
            "Content-Type": "application/json"
        }

if __name__ == "__main__":
    try:
        from creds import LIQUID_TOKEN_ID, LIQUID_SECRET
    except:
        LIQUID_TOKEN_ID = input("Enter your token ID:")
        LIQUID_SECRET = input("Enter your secret:")
    
    api = LiquidAPI(LIQUID_TOKEN_ID, LIQUID_SECRET)
    print(api.get_products("35"))
    
