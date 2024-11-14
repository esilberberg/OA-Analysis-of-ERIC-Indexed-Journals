import pandas as pd
import json

def get_openapc_data(issn):
    if issn is None or issn == "":
        print('No ISSN found')
        return '', ''

    filtered_openapc_data = openapc_df[(openapc_df['issn'] == issn)]

    if filtered_openapc_data.empty:
        return None, None 

    avg_apc_euros = filtered_openapc_data['euro'].mean()

    if avg_apc_euros >= 1:
        exchange_rate = 1.09
        avg_apc_dollars = int(filtered_openapc_data['euro'].mean()) * exchange_rate
        avg_apc_dollars = round(avg_apc_dollars, 2)
    else:
        avg_apc_dollars = None

    is_hybrid = int(filtered_openapc_data['is_hybrid'].mode().astype(bool).iloc[0])

    print(issn)
    print(avg_apc_dollars, is_hybrid)
    return avg_apc_dollars, is_hybrid


with open('OpenAPC/openapc_data', 'r') as f:
    data = [json.loads(line) for line in f]

openapc_df = pd.DataFrame(data)
main_df = pd.read_excel('Step6_Results.xlsx')


main_df['OPENAPC_Avg_APC_USD'], main_df['OPENAPC_is_hybrid_(mode)'] = zip(*main_df['issn_l'].apply(get_openapc_data))

main_df.to_excel('Step7_Results.xlsx', index=False)
print(main_df)