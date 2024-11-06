import pandas as pd
import requests

with open('sr-key.txt') as f:
	sr_api_key = f.read()

def get_sherparomeo_data(issn):
    """Fetches select journal metadata from SherpaRomeo API via the ISSN-L"""
    
    error_data = None, None, None, None, None,
    
    if issn is None or issn == "":
        print('No ISSN-L found')
        return error_data
    
    base_url = 'https://v2.sherpa.ac.uk/cgi/retrieve_by_id'
    api_endpoint = f'{base_url}?item-type=publication&api-key={sr_api_key}&format=Json&identifier={issn}'
   
    response = requests.get(api_endpoint)
    response_json = response.json()
    
    try:
        data = response_json['items'][0]
    except(IndexError):
         print(f'No record: {issn}')
         return error_data

    try:
        publisher = data['publishers'][0]['publisher']['name'][0]['name']
    except: 
         publisher = None

    try:
        publisher_type = data['publishers'][0]['relationship_type_phrases'][0]['phrase']
    except:
        publisher_type = None
   
    try:
        country = data['publishers'][0]['publisher']['country']
    except:
         country = None
    
    try:
        publisher_oa_policies = data['publisher_policy']
    except:
         oa_fees, oa_schemes = None, None
    
    oa_fees = []
    oa_schemes = []
    for policy in publisher_oa_policies:
        oa_schemes.append(policy.get('internal_moniker'))
        pathways = policy['permitted_oa']
        for path in pathways:
            try:
                version = path['article_version'][0]
            except(KeyError):
                pass
            if version == 'published':
                oa_fee = path.get('additional_oa_fee')
                oa_fees.append((oa_fee))

    print(issn)
    print(publisher, publisher_type, country, oa_fees, oa_schemes)       
    return publisher, publisher_type, country, oa_fees, oa_schemes

file = 'Step4_Results.xlsx'
df = pd.read_excel(file)

df['SR_publisher'], df['SR_publisher_type'], df['SR_country'], df['SR_published_version_oa_fees'], df['SR_oa_schemes'], = zip(*df['issn_l'].apply(get_sherparomeo_data))

df.to_excel('Step5_Results.xlsx', index=False)
print(df)