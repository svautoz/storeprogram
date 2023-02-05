import price_lib as pl
import pandas as pd
import base64
import requests
import json

file_name = 'getprice.xlsx'


login = "info@svautoz.ru"
password = "461821td"
url = 'https://www.svautoz.ru/webservice/?out=json&in=json&'
max_time_filter = 79


def contruct_params(method, data):
    params = {'login': base64.b64encode(login.encode('utf-8')).decode("utf-8"), 'password': base64.b64encode(password.encode('utf-8')).decode("utf-8")}
    match(method):
        case 'testConnection':
            params['method'] = 'testConnection'
            params['data'] = ''
        case 'getPrice':
            params['method'] = 'getPrice'
            params['data'] = data
    params = json.dumps(params)
    return base64.b64encode(params.encode('utf-8'))


def test_connection():
    params = contruct_params('testConnection')    
    req_string = url + "data=" + params.decode("utf-8")
    response = requests.get(req_string)
    return response.json()


def get_price_from_site(spares_df):
    price_list = list()
    for i in range(len(spares_df.index)):
        art = spares_df.NUMBER[i].strip()
        brand = spares_df.BRAND[i].strip()    
        params = contruct_params('getPrice', {'art': art, 'brand': brand})  
        req_string = url + "data=" + params.decode("utf-8")
        response = requests.get(req_string).json()
        best_price = 0
        if "products" in response['data']:
            products = response['data']['products']        
            product_offers = list()
            for product in products:
                time = product['delivery_time'].split()
                min_time = time[0]
                max_time = time[2] if len(time) > 1 else time[0]
                product_offers.append({'price': product['prices']['delivery_id_1'], 'qty': product['qty'], 'min_time': min_time, 'max_time': max_time})
            best_price = filter_products_min_price(product_offers)        
        price_list.append(best_price)
        print(art, brand, best_price)
    return pd.Series(price_list)


def filter_products_min_price(products):
    max_price = 0
    for product in products:
        if (max_price == 0 and int(product['max_time']) < max_time_filter) or (int(product['max_time']) < max_time_filter and product['price'] < max_price):
            max_price = product['price']
    return max_price


spares_df = pl.get_df_from_file(file_name, 0)
price = get_price_from_site(spares_df)
spares_df['price'] = price
pl.set_result_sheet_from_df(file_name, spares_df)


