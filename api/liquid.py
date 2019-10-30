import requests
import time
import jwt

class LiquidAPI:
    
    BASE_URL = "https://api.liquid.com"

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret
        self.currency_pairs = self.get_currency_pairs()

    def get_products(self, product_id=None, pair_code=None):
        '''
        Get a list a products (trading pairs) available. If no product_id is specified, the complete list will be returned.
        '''
        path = "%s/products" % self.BASE_URL
        if product_id:
            path += "/" + product_id
        elif pair_code:
            path += "/" + self.currency_pairs[pair_code]
        return self._get(path)

    def get_order_book(self, product_id=None, pair_code=None, full=None):
        '''
        Get order book for a product.
        '''
        path = "%s/products" % self.BASE_URL
        if product_id:
            path += "/" + product_id
        elif pair_code:
            path += "/" + self.currency_pairs[pair_code]
        path += "/price_levels"
        path += "?full=" + str(full) if full else ""
        return api._get(path)

    def get_currency_pairs(self):
        '''
        Return a dictionary of indexes assigned to their currency pair code
        '''
        products = self.get_products()
        currency_pairs = {}
        for product in products:
            currency_pairs[product["currency_pair_code"]] = product["id"]
        return currency_pairs

    def _get(self, path, params={}):
        '''
        Return result of a GET call to the API.
        '''
        params.update({"recvWindow": 120000})
        url = "%s" % path
        header = self.generate_header(path)
        return requests.get(url, headers=header, \
            timeout=30, verify=True).json()

    def generate_header(self, path):
        '''
        Generate the header for call to API.
        '''
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
    # print(api.get_products(pair_code="BTCJPY"))
    result = api.get_order_book(pair_code="BTCJPY")

    # for pair, index in api.currency_pairs.items():
    #     print(pair, index)

    print(result)
    
