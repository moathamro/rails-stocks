import requests

# Sandbox API - FOR TESTING
BASE_URL = 'https://sandbox.iexapis.com'
PUBLIC_TOKEN = 'Tpk_c818732500c24764801eb121fa658bb6'


# Real API - FOR PRODUCTION
# YOU NEED TO CREATE AN ACCOUNT TO RECEIVE YOUR OWN API KEYS (its free)
# BASE_URL = '<MAKE_AN_ACCOUNT>'
# PUBLIC_TOKEN = '<MAKE_AN_ACCOUNT>'

# For general info for all symbols
# https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a


# For all symbols with prices (*free weight*)
# https://cloud.iexapis.com/stable/tops/last?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a
def _request_data(url, filter='', additional_parameters={}):
    final_url = BASE_URL + url

    query_strings = {
        'token': PUBLIC_TOKEN
    }
    query_strings.update(additional_parameters)

    if filter:
        query_strings['filter'] = filter

    response = requests.get(final_url, params=query_strings)

    if not response.ok:
        raise Exception('Unexpected response: ', response.__dict__)
    return response.json()


def _get_top_stocks():
    data = _request_data('/stable/stock/market/list/mostactive',
                         filter='symbol,companyName,latestVolume,change,changePercent,primaryExchange,marketCap,latestPrice,calculationPrice,recommendationTrends',
                         additional_parameters={'displayPercent': 'true', 'listLimit': '20'})
    return data
"""
NOTE=============================
difference between change and change over time

"""


def get_stock_info(symbol):
    # 'symbol,companyName,marketcap,totalCash,primaryExchange,latestPrice,latestSource,change,changePercent'
    data = _request_data('/stable/stock/{symbol}/quote'.format(symbol=symbol),
                         additional_parameters={'displayPercent': 'true'})
    # to get the currency
    data2 = _request_data('/stable/stock/{symbol}/financials'.format(symbol=symbol),
                          additional_parameters={'displayPercent': 'true'})

    finan_list = data2["financials"]
    data['currency'] = finan_list[0]['currency']
    try:
        data['revenueLoss'] = finan_list[0]['totalRevenue'] - \
            finan_list[0]['costOfRevenue']
    except:
        data['revenueLoss'] = "No data"

    data3 = _request_data('/stable/stock/{symbol}/company'.format(symbol=symbol),
                          additional_parameters={'displayPercent': 'true'})

    data['issue'] = data3['issueType']

    return data


def get_stock_historic_prices(symbol, time_range='1m'):
    return _request_data('/stable/stock/{symbol}/chart/{time_range}'.format(symbol=symbol, time_range=time_range))


def _get_all_stocks():
    return _request_data('/stable/stock/market/list/mostactive',
                         filter='symbol,companyName,latestVolume,change,changePercent,primaryExchange,marketCap,latestPrice,calculationPrice',
                         additional_parameters={'displayPercent': 'true', 'listLimit': '300'})

def _get_all_stocks():
    return _request_data('/stable/stock/market/list/mostactive',
                         filter='symbol,companyName,latestVolume,change,changePercent,primaryExchange,marketCap,latestPrice,calculationPrice,recommendationTrends',
                         additional_parameters={'displayPercent': 'true', 'listLimit': '100'})


def get_stock_Recommendations(symbol):
    data = _request_data('/stable/stock/{symbol}/recommendation-trends'.format(symbol=symbol), filter='ratingScaleMark')
    if data:
        dict = data[0]
        num = dict['ratingScaleMark']
        return num
    else:
        return 4