import price_lib as pl
import requests
import pandas as pd
import json
from xml.etree import ElementTree
import time
from random import randint

api_key = "MBmE7rdJlQjqwr7B1t4CZLfRPlcE1Egu1jkFz3VaqpRFrOhF9GyCALWK43p"
login = "info@svautoz.ru"
password = "svautoz"
code_region = 1
partnumber = '8521148200'
class_man = 'VARTA'
file_name = './febi.xlsx'

def get_min_zzap_price(api_key, login, password, code_region, partnumber, class_man):
    params={'login': login, 'password': password, 'partnumber': partnumber, 'class_man': class_man, 
                    'code_cur': 1, 'code_region': code_region, 'type_request': 1, 'api_key': api_key}
    response = requests.get('https://www.zzap.ru/webservice/datasharing.asmx/GetSearchResultInfoV3', params)
    response_xml_body = ElementTree.fromstring(response.content).text
    response_dict = json.loads(response_xml_body)

    return response_dict['price_min_instock']


def get_price_from_zzap(df):
    i = 0
    freq_array = list()
    for part in df.MPN[30:45]:
        freq_array.append(get_min_zzap_price(api_key, login, password, code_region, part, class_man))
        i += 1
        susp_time = randint(60,120)
        print(i, susp_time)
        time.sleep(susp_time)
    return pd.Series(freq_array)


df = pl.get_df_from_file(file_name, 0)
df['zzap_min_price'] = get_price_from_zzap(df)
pl.set_result_sheet_from_df(file_name, df)

