import requests
import time
import jwt

class LiquidAPI:
    
    BASE_URL = "https://api.liquid.com"

    def __init__(self, token_id, secret):
        self.token_id = token_id
        self.secret = secret
        self.pairs_id = self.get_currency_pairs()

    def info(self, pair):
        '''
        Return infos on currency pair.
        TODO: process json response into dictionary.
        '''
        return self.get_products(self.pairs_id[pair])

    def history(self, pair):
        '''
        Return history of orders of currency pair.
        TODO: process json response into dictionary.
        '''
        return self.get_order_book(self.pairs_id[pair])

    def get_products(self, product_id=None):
        '''
        Get a list a products (trading pairs) available. If no product_id is specified, the complete list will be returned.
        https://developers.liquid.com/#get-a-product
        '''
        path = "/products"
        if product_id:
            path += "/" + product_id
        return self._get(path)

    def get_order_book(self, product_id, full=False):
        '''
        Get order book for a product.
        full to True, then all history will be returned.
        https://developers.liquid.com/#get-order-book
        '''
        path = "/products"
        path += "/" + product_id + "/price_levels"
        path += "?full=1" if full else ""
        return self._get(path)

    def get_executions(self, product_id, limit=None, page=None, timestamp=None):
        '''
        Get list of recent executions
        limit and page are for selecting the range of executions to be returned.
        For example limit=20 and page=2 will return executions 21 to 40.
        https://developers.liquid.com/#executions
        '''
        path = "/executions"
        path += "?product_id=%s" % product_id
        if limit:
            path += "&limit=%s" % limit
        if page:
            path += "&page=%s" % page
        if timestamp:
            path += "&timestamp=%s" % timestamp
        return self._get(path)

    def get_interest_rates(self, currency):
        '''
        Get interest rates for currency. Example currency="USD"
        '''
        path = "ir_ladders/" + currency
        return self._get(path)

    def get_fees(self, product_id, fee_type):
        '''
        /!\ API documentation is not clear
        Get fees
        fee_type={0: trade_fee,
                  1: additional_liquidation_trade_fee,
                  2: trade_fee_discount}
        '''
        raise NotImplementedError

        path = "/fees" + "&product_id=" + product_id
        if fee_type == 1:
            path += "&fee_type=trade_fee"
        elif fee_type == 2:
            path += "&fee_type=additional_liquidation_trade_fee"
        elif fee_type == 3:
            path += "&fee_type=trade_fee_discount"
        return self._get(path)

    def get_order(self,  order_id):
        '''
        Get an order
        https://developers.liquid.com/#get-an-order
        '''
        path = "/orders/%s" % order_id
        return self._get(path)

    def get_orders(self, funding_currency=None, product_id=None,
                   status=None, trading_type=None, with_details=False):
        '''
        Get orders
        https://developers.liquid.com/#get-orders
        '''
        path = "/orders"
        if funding_currency:
            path += "&funding_currency=" % funding_currency
        if product_id:
            path += "&product_id=" % product_id
        if status:
            path += "&status=" % status
        if with_details:
            path += "&with_details=1"
        return self._get(path)

    def cancel_order(self, order_id):
        '''
        https://developers.liquid.com/#cancel-an-order
        '''
        path = "/orders/%s" % order_id + "/cancel"
        return self._get(path)

    def get_trade(self, order_id):
        '''
        Get order_id order's trade
        https://developers.liquid.com/#get-an-order's-trades
        '''
        path = "/orders/%s/trades" % order_id
        return self._get(path)
    def get_currency_pairs(self):
        '''
        Return a dictionary of indexes assigned to their currency pair code
        '''
        products = self.get_products()
        pairs_id = {}
        for product in products:
            pairs_id[product["currency_pair_code"]] = product["id"]
        return pairs_id

    def _get(self, path, params={}):
        '''
        Return result of a GET call to the API.
        '''
        params.update({"recvWindow": 120000})
        url = self.BASE_URL + path
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
    # BTCJPY's id is 5
    result = api.history("BTCJPY")



    print(result)
    
