import pandas as pd
import re
import statsmodels.api as sm
import math


file = 'FULL_DATA_SET.xlsx'
df = pd.read_excel(file)

# # 1 Number of journals per ERIC collection area 
# print(df['ERIC Topic Area'].value_counts())


# # 2. Subscription vs. OA
# print(df['EZB_price_for_reading_access'].count())
# print(df['EZB_price_for_reading_access'].value_counts())
# print(df['EZB_price_for_reading_access'].value_counts(normalize=True) * 100)
# print('---'*10)
# print(df['openalex_is_oa'].count())
# print(df['openalex_is_oa'].value_counts())
# print(df['openalex_is_oa'].value_counts(normalize=True) * 100)

df['composite_OA'] = df['openalex_is_oa'].fillna(df['EZB_price_for_reading_access'])

def is_oa(data):
    yes_oa = [1.0, "{'subject to fee', 'free of charge'}", "{'free of charge'}" ]
    not_oa = [0.0, "{'subject to fee'}"]
    if data in yes_oa:
        return 'oa'
    elif data in not_oa:
        return 'no'
    else: 
        return None

df['composite_OA_results'] = df['composite_OA'].apply(is_oa)
# print(df['composite_OA_results'].count())
# print(df['composite_OA_results'].value_counts())
# print(df['composite_OA_results'].value_counts(normalize=True) * 100)


# 3 Impact Factors
# print(df['openalex_h_index'].describe())
# print(df['openalex_impact_factor'].describe())

# print('Highest H-Index for OA')
# filter_df = df[df['composite_OA_results'] == 'oa']
# h_index_idx = filter_df['openalex_h_index'].idxmax()
# oa_highest_hindex = filter_df.loc[h_index_idx, ['Journal Name', 'issn_l', 'openalex_h_index']]
# print(oa_highest_hindex)

# print('Highest 2yr Impact Factor for OA')
# filter_df = df[df['composite_OA_results'] == 'oa']
# two_yr_idx = filter_df['openalex_impact_factor'].idxmax()
# oa_highest_two_yr = filter_df.loc[two_yr_idx, ['Journal Name', 'issn_l', 'openalex_impact_factor']]
# print(oa_highest_two_yr)

# print('Highest H-Index for Subscription')
# filter_df = df[df['composite_OA_results'] == 'no']
# h_index_idx = filter_df['openalex_h_index'].idxmax()
# subscription_highest_hindex = filter_df.loc[h_index_idx, ['Journal Name', 'issn_l', 'openalex_h_index']]
# print(subscription_highest_hindex)

# print('Highest 2yr Impact Factor for Subscription')
# filter_df = df[df['composite_OA_results'] == 'no']
# two_yr_idx = filter_df['openalex_impact_factor'].idxmax()
# subscription_highest_two_yr = filter_df.loc[two_yr_idx, ['Journal Name', 'issn_l', 'openalex_impact_factor']]
# print(subscription_highest_two_yr)


# 4. APCs
# print('OpenAPC')
# print(df['OPENAPC_Avg_APC_USD'].dropna().describe())
# print('----'*5)
# print('OpenAlex')
# print(df['openalex_apc_usd'].dropna().describe())
# print('----'*5)
# print('DOAJ')
# print(df['doaj_apc_usd'].dropna().describe())

df['composite_apc'] = df['OPENAPC_Avg_APC_USD'].fillna(df['openalex_apc_usd'])
df['composite_apc'] = df['composite_apc'].fillna(df['doaj_apc_usd'])
# print(df['composite_apc'].describe())
# apc_idx = df['composite_apc'].idxmax()
# highest_apc = df.loc[apc_idx, ['Journal Name', 'issn_l', 'composite_apc']]
# print(highest_apc)


# 5. Publishers
df['composite_publishers'] = df['openalex_publisher'].fillna(df['SR_publisher'])
df['composite_publishers'] = df['composite_publishers'].fillna(df['EZB_publishers'])
# print(df['composite_publishers'].value_counts())
# print(df['composite_publishers'].count())

# threshold = df['composite_apc'].quantile(0.75)
# df_filtered = df[df['composite_apc'] >= threshold]
# high_apc_publishers = df_filtered['composite_publishers']
# print(high_apc_publishers.value_counts())
# print(high_apc_publishers.count())


# 6. Types of Publishers
grouped_df = df.groupby(['SR_publisher_type', 'Journal Name'])['composite_apc'].max().reset_index()
sorted_df = grouped_df.sort_values(['SR_publisher_type', 'composite_apc'], ascending=[True, False])


print(df['SR_publisher_type'].count())
publisher_types = ['Commercial Publisher', 'University Publisher', 'Society Publisher']
for publisher_type in publisher_types:
    # filtered_df = df[df['SR_publisher_type'] == publisher_type]
    # publisher_column = filtered_df['composite_publishers']
    # publishers_per_type = filtered_df['composite_publishers'].nunique()
    # print(f"Total publishers for {publisher_type}: {publishers_per_type}")
    # journals_per_type = filtered_df['Journal Name'].nunique()
    # print(f"Total journals for {publisher_type}: {journals_per_type}")
    # print(f"Publishers for {publisher_type}:")
    # print(publisher_column.value_counts())

    top_journal = sorted_df[sorted_df['SR_publisher_type'] == publisher_type].iloc[0]
    print(f"Highest APC for {publisher_type}:")
    print(f"Journal Name: {top_journal['Journal Name']}")
    print(f"Composite APC: {top_journal['composite_apc']}")


# # 7. Regression: APC and Impact Factor
# # Include only rows that have APC and H-Index
# df['h_index_per_apc'] = df['openalex_h_index'].where(df['composite_apc'].notnull())
# df_filtered_h_index = df[df['h_index_per_apc'].notnull()]

# # Calculate correlation
# correlation = df_filtered_h_index['composite_apc'].corr(df_filtered_h_index['h_index_per_apc'])
# print("Correlation coefficient:", correlation)

# # Regression Analysis
# X = df_filtered_h_index['h_index_per_apc']
# y = df_filtered_h_index[['composite_apc']]
# model = sm.OLS(y, X).fit()
# print(model.summary())

# # Include only rows that have APC and 2-year impact factor
# df['impact_factor_per_apc'] = df['openalex_impact_factor'].where(df['composite_apc'].notnull())
# df_filtered_impact_factor = df[df['impact_factor_per_apc'].notnull()]

# # Calculate correlation
# correlation = df_filtered_impact_factor['composite_apc'].corr(df_filtered_impact_factor['impact_factor_per_apc'])
# print("Correlation coefficient:", correlation)

# # Regression Analysis
# X = df_filtered_impact_factor['impact_factor_per_apc']
# y = df_filtered_impact_factor['composite_apc']
# model = sm.OLS(y, X).fit()
# print(model.summary())


