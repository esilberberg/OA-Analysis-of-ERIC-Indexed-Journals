import pandas as pd
import csv

def get_ezb_data(issn):

    issn_search_result = ezb_df[(ezb_df['E-ISSN'] == issn) | (ezb_df['P-ISSN'] == issn)]

    publishers = issn_search_result['Publisher'].to_list()
    flattened_publishers = list(set(p.strip() for p in (item for sublist in (publisher.split('; ') for publisher in publishers) for item in sublist)))

    ezb_id = set(issn_search_result['EZB-Id'].to_list())
    journal_type = set(issn_search_result['Type'].to_list())
    price = set(issn_search_result['Price type'].to_list())
    access_requirements = set(issn_search_result['Access requirements'].to_list())
    first_year = set(issn_search_result['First year'].to_list())
    last_year = set(issn_search_result['Last year'].to_list())
    moving_wall = set(issn_search_result['Moving Wall'].to_list())

    print(issn)
    print(flattened_publishers, ezb_id, journal_type, price, access_requirements, first_year, last_year, moving_wall)
    return flattened_publishers, ezb_id, journal_type, price, access_requirements, first_year, last_year, moving_wall


data = []
with open('EZB_journals_2024_11_05.txt', 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        data.append(row)

columns = data[2]
rows = data[3:]

ezb_df = pd.DataFrame(rows, columns=columns)
main_df = pd.read_excel('Step5_Results.xlsx')

main_df['EZB_publishers'], main_df['EZB_ID'], main_df['EZB_journal_type'], main_df['EZB_price_for_reading_access'], main_df['EZB_access_conditions'], main_df['EZB_first_year'], main_df['EZB_last_year'], main_df['EZB_moving_wall']  = zip(*main_df['issn_l'].apply(get_ezb_data))

main_df.to_excel('Step6_Results.xlsx', index=False)
print(main_df)