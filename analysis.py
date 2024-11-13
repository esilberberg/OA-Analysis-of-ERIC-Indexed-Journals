import pandas as pd
import re
import statsmodels.api as sm
import math


file = 'FULL_DATA_SET.xlsx'
df = pd.read_excel(file)
print(df.columns)

# 1. General description of ERIC indexed journals:
# 1.1 Countries
# print(f'OpenAlex Total: {df['openalex_country'].count()} || JISC Total:{df['SR_country'].count()}')
# df['combined_country'] = df['openalex_country'].fillna(df['SR_country'])
# df['combined_country'] = df['combined_country'].str.lower()
# print(df['combined_country'].count())
# print(df['combined_country'].value_counts())
# print(df['combined_country'].value_counts(normalize=True) * 100)

# 1.2 Number of journals per ERIC collection area 
# print(df['ERIC Topic Area'].value_counts())

# 1.3 Publishers
# print(f'OpenAlex: {df['openalex_publisher'].count()} || JISC: {df['SR_publisher'].count()} || EZB: {df['EZB_publishers'].count()}')
# df['combined_publishers'] = df['openalex_publisher'].fillna(df['SR_publisher'])
# df['combined_publishers'] = df['combined_publishers'].fillna(df['EZB_publishers'])
# print(df['combined_publishers'].count())
# print(df['combined_publishers'].value_counts().head(20))
# print(df['openalex_organization'].value_counts().head(20))
# print(df['SR_publisher_type'].value_counts())

# publisher_types = ['Commercial Publisher', 'University Publisher', 'Society Publisher']
# for publisher_type in publisher_types:
#     filtered_df = df[df['SR_publisher_type'] == publisher_type]
#     publisher_column = filtered_df['combined_publishers']
#     print(f"Publishers for {publisher_type}:")
#     print(publisher_column.value_counts())

# 1.4 Year OA Started
# print(f'EZB: {df['EZB_first_year'].count()} || DOAJ: {df['doaj_oa_startdate'].count()}')

# def extact_first_oa_year(year):
#     if year is None or year == "" or year == 'nan':
#         return None
#     year = re.sub(r'\{|\}', '', year)
#     year = re.sub(r"'", "", year)
#     if ',' in year:
#         years = year.split(',')
#         years = [int(y.strip()) for y in years if y.strip()]
#         if years:
#             return min(years)
#         else:
#             return None
#     else:
#         return int(year)

# df['EZB_first_year'] = df['EZB_first_year'].astype(str).apply(extact_first_oa_year)
# print(df['EZB_first_year'].value_counts().head(30))

# 1.5 APCs
# print(f'OPENAPC: {df['OPENAPC_Avg_APC_USD'].count()} || OpenAlex: {df['openalex_apc_usd'].count()} || DOAJ: {df['doaj_apc_usd'].count()}')

# print('OpenAPC')
# print(df['OPENAPC_Avg_APC_USD'].dropna().describe())
# print('OpenAlex')
# print(df['openalex_apc_usd'].dropna().describe())
# print('DOAJ')
# print(df['doaj_apc_usd'].dropna().describe())

# df['combined_apc'] = df['OPENAPC_Avg_APC_USD'].fillna(df['openalex_apc_usd'])
# df['combined_apc'] = df['combined_apc'].fillna(df['doaj_apc_usd'])
# print('Combined')
# print(df['combined_apc'].describe())

# df['combined_publishers'] = df['openalex_publisher'].fillna(df['SR_publisher'])
# df['combined_publishers'] = df['combined_publishers'].fillna(df['EZB_publishers'])

# avg_apc_per_publisher = df.groupby('combined_publishers')['combined_apc'].mean().dropna().sort_values(ascending=False)
# avg_apc_per_publisher_type = df.groupby('SR_publisher_type')['combined_apc'].mean().dropna().sort_values(ascending=False)

# avg_apc_per_publisher_by_type = df.groupby(['SR_publisher_type', 'combined_publishers'])['combined_apc'].mean().dropna().reset_index()

# print(avg_apc_per_publisher)

# 1.6 Impact Factors
# print('H-Index')
# top_20_journals = df.nlargest(20, 'openalex_h_index')
# print(top_20_journals['Journal Name'])
# print(df['openalex_h_index'].describe())
# print(df['openalex_h_index'].describe())

# # print('2yr Impact Factor')
# top_20_journals = df.nlargest(20, 'openalex_impact_factor')
# print(top_20_journals['Journal Name'])
# print(df['openalex_impact_factor'].describe())

# 1.7 H-Index v. APC Regression

# df['combined_apc'] = df['OPENAPC_Avg_APC_USD'].fillna(df['openalex_apc_usd'])
# df['combined_apc'] = df['combined_apc'].fillna(df['doaj_apc_usd'])

# # Include only rows that have APC and H-Index
# df['h_index_per_apc'] = df['openalex_h_index'].where(df['combined_apc'].notnull())
# df_filtered_h_index = df[df['h_index_per_apc'].notnull()]

# # Calculate correlation
# correlation = df_filtered_h_index['combined_apc'].corr(df_filtered_h_index['h_index_per_apc'])
# print("Correlation coefficient:", correlation)

# # Regression Analysis
# X = df_filtered_h_index['h_index_per_apc']
# y = df_filtered_h_index[['combined_apc']]
# model = sm.OLS(y, X).fit()
# print(model.summary())

# df['impact_factor_per_apc'] = df['openalex_impact_factor'].where(df['combined_apc'].notnull())
# df_filtered_impact_factor = df[df['impact_factor_per_apc'].notnull()]

# # Calculate correlation
# correlation = df_filtered_impact_factor['combined_apc'].corr(df_filtered_impact_factor['impact_factor_per_apc'])
# print("Correlation coefficient:", correlation)

# # Regression Analysis
# X = df_filtered_impact_factor['impact_factor_per_apc']
# y = df_filtered_impact_factor['combined_apc']
# model = sm.OLS(y, X).fit()
# print(model.summary())


# # 2. Access for Readers 
# print(df[['EZB_price_for_reading_access', 'EZB_access_conditions']])
# print(df['EZB_price_for_reading_access'].count())
# print(df['EZB_price_for_reading_access'].value_counts())
# print(df['EZB_price_for_reading_access'].value_counts(normalize=True) * 100)
# print('---'*10)
# print(df['openalex_is_oa'].count())
# print(df['openalex_is_oa'].value_counts())
# print(df['openalex_is_oa'].value_counts(normalize=True) * 100)

# df['combined_OA'] = df['openalex_is_oa'].fillna(df['EZB_price_for_reading_access'])
# print(df['combined_OA'].count())

# def is_oa(data):
#     options = [1.0, "{'subject to fee', 'free of charge'}", "{'free of charge'}" ]
#     not_options = [0.0, "{'subject to fee'}"]
#     if data in options:
#         return 'oa'
#     elif data in not_options:
#         return 'no'
#     else: 
#         return None

# df['combined_OA_results'] = df['combined_OA'].apply(is_oa)
# print(df['combined_OA_results'].count())
# print(df['combined_OA_results'].value_counts())
# print(df['combined_OA_results'].value_counts(normalize=True) * 100)

# =1 {'subject to fee', 'free of charge'}{'free of charge'}

# 3. Is it Diamond Open Access? 
# def determine_if_published_ver_oa_fee(data):
#     if not data:
#         return None

#     data = str(data).strip()
#     data = data.replace('[', '').replace(']', '').replace("'", "")

#     if ',' in data:
#         answers = data.split(',')
#         return 'no' if 'no' in answers else 'yes'

#     return data

# def determine_if_oa(row):
#     if row['EZB_price_for_reading_access'] == "{'free of charge'}":
#         return "yes"
#     elif row['EZB_price_for_reading_access'] == "{'subject to fee'}":
#         return "no"
#     elif row['EZB_price_for_reading_access'] is None or row['EZB_price_for_reading_access'] == "{'subject to fee', 'free of charge'}":
#         return "yes" if row['openalex_is_oa'] == 1 else None
#     else:
#         return None

# def determine_if_diamond_oa(row):
#     if row['is_oa'] == 'yes' and row['published_version_oa_fee'] == 'no' and (math.isnan(row['combined_apc']) or row['combined_apc'] is None):
#         return True
#     else:
#         return False

# df['combined_apc'] = df['OPENAPC_Avg_APC_USD'].fillna(df['openalex_apc_usd'])
# df['combined_apc'] = df['combined_apc'].fillna(df['doaj_apc_usd'])

# df['published_version_oa_fee'] = df['SR_published_version_oa_fees'].apply(determine_if_published_ver_oa_fee)
# df['is_oa'] = df.apply(determine_if_oa, axis=1)
# df['diamond_oa_status'] = df.apply(determine_if_diamond_oa, axis=1)

# print(df['is_oa'].value_counts())
# print(df['diamond_oa_status'].value_counts())

# 4. Classes of Hybrid OA publishing schemes

# def unpack_oa_schemes(data):
#     if not data:
#         return None

#     data = str(data).strip()
#     data = data.replace('[', '').replace(']', '').replace("'", "")

#     policies_list = []
#     if ',' in data:
#         policies = data.split(',')
#         for policy in policies:
#             policies_list.append(policy.strip())
#         return policies_list
#     else:
#         return data

# df['oa_schemes'] = df['SR_oa_schemes'].apply(unpack_oa_schemes)
# df_expanded = df['oa_schemes'].explode()
# df_expanded = df_expanded.dropna()

# print(df_expanded.value_counts().head(30))
