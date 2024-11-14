import pandas as pd
import requests

def get_openalex_data(id):
    """Fetches select journal metadata from OpenAlex API via the OpenAlex ID."""
    if id is None or id == "":
        print('No ID found.')
        # Returns None values to avoid error when assigning later to Dataframe
        return (None,) * 10 
    
    base_url = 'https://api.openalex.org/sources/'
    api_endpoint = base_url + str(id)
    response = requests.get(api_endpoint)

    if response.status_code != 200:
        print(f"Error retrieving data! (ID: {id}) (Status Code: {response.status_code})")
        return (None,) * 10  # Returns None values to avoid error when assigning later to Dataframe

    data = response.json()

    publisher = data.get('host_organization_name')
    homepage = data.get('homepage_url')
    is_oa = data.get('is_oa')
    is_in_doaj = data.get('is_in_doaj')
    apc_usd = data.get('apc_usd')
    country = data.get('country_code')

    if 'societies' not in data or not data['societies']:
        organization = None
    else:
        organization = data['societies'][0]['organization']

    try:
        h_index = data['summary_stats']['h_index']
    except (KeyError, IndexError):
        h_index = None
    
    try:
        impact_factor = data['summary_stats']['2yr_mean_citedness']
    except (KeyError, IndexError):
        impact_factor = None

    try:
        wikidata_id = data['ids']['wikidata']
        if wikidata_id:
            wikidata_id = wikidata_id.replace('https://www.wikidata.org/entity/', '')
            wikidata_id = wikidata_id.replace('http://www.wikidata.org/entity/', '')
    except (KeyError, IndexError):
        wikidata_id = None

    print(id)
    print(publisher, homepage, organization, country, h_index, impact_factor, is_oa, is_in_doaj, apc_usd, wikidata_id)
    return publisher, homepage, organization, country, h_index, impact_factor, is_oa, is_in_doaj, apc_usd, wikidata_id

file = 'Step2_Results.xlsx'
df = pd.read_excel(file)

df['publisher'], df['homepage'], df['organization'], df['country'], df['h_index'], df['impact_factor'], df['is_oa'], df['is_in_doaj'], df['apc_usd'], df['wikidata_id'] = zip(*df['openalex_id'].apply(get_openalex_data))

df.to_excel('Step3_Results.xlsx', index=False)
print(df)