import pandas as pd
import requests

def get_doaj_data(issn):
    """Fetches select journal metadata from DOAJ API via the ISSN-L"""
    if issn is None or issn == "":
        print('No ISSN-L found')
        return '', '', '', '', ''
    
    base_url = 'https://doaj.org/api/search/journals/issn:'
    api_endpoint = base_url + str(issn)
    
    response = requests.get(api_endpoint)
    results = response.json().get('results')

    if results:
        data = results[0]['bibjson']

        oa_start = data.get('oa_start')
        apc_waiver = data.get('waiver').get('has_waiver')

        apc_info = data.get('apc')
        has_apc = apc_info.get('has_apc')
        apc_url = apc_info.get('url')
        
        if apc_info.get('max'):
            for item in apc_info.get('max'):
                if item['currency'] == 'USD':
                    apc_usd = item['price']
                else: apc_usd = f"{item['currency']} {item['price']}"

        else: apc_usd = None
        
        print(issn)
        print(oa_start, has_apc, apc_usd, apc_waiver, apc_url)
        return oa_start, has_apc, apc_usd, apc_waiver, apc_url 
    else:
        return '', '', '', '', '' 

file = 'Step3_Results.xlsx'
df = pd.read_excel(file)

df['DOAJ_oa_startdate'], df['DOAJ_has_apc'], df['DOAJ_apc_usd'], df['DOAJ_apc_waiver'], df['DOAJ_apc_url'] = zip(*df['issn_l'].apply(get_doaj_data))

df.to_excel('Step4_Results.xlsx', index=False)
print(df)