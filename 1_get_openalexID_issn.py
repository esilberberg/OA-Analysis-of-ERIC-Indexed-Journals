import pandas as pd
import requests

def get_openalexID_issn(journal_name):
    """Fetches the OpenAlex ID and ISSN-L for a given journal name from the OpenAlex API."""
    base_url = 'https://api.openalex.org/sources?search='
    api_endpoint = base_url + journal_name

    response = requests.get(api_endpoint)
    response_json = response.json()
    data = response_json.get('results')

    try: 
        data = data[0]
        openalex_id = data.get('id')
        if openalex_id:
            openalex_id = openalex_id.replace('https://openalex.org/', '')
        issn_l = data.get('issn_l')
    except (KeyError, IndexError, TypeError):
        openalex_id, issn_l = None, None

    print(f'{journal_name}: {openalex_id}, {issn_l}')
    return openalex_id, issn_l


file = 'ERIC Indexed Journals Dataset.xlsx'
df = pd.read_excel(file)

df['openalex_id'], df['issn_l'] = zip(*df['Journal Name'].apply(get_openalexID_issn))

df.to_excel('data_openalexid_issn.xlsx', index=False)
print(df)