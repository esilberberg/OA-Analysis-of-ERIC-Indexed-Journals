import pandas as pd
import statsmodels.api as sm
import math

file = 'FULL_DATA_SET.xlsx'
df = pd.read_excel(file)

# 1. Composite Data
# 1.1 Subscription and Open Access
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

# 1.2 Countries
df['composite_country'] = df['openalex_country'].fillna(df['SR_country'])
df['composite_country'] = df['composite_country'].str.lower()

# 1.3 APC Fees
df['composite_apc'] = df['OPENAPC_Avg_APC_USD'].fillna(df['openalex_apc_usd'])
df['composite_apc'] = df['composite_apc'].fillna(df['doaj_apc_usd'])

# 1.4 Publisher
df['composite_publishers'] = df['openalex_publisher'].fillna(df['SR_publisher'])
df['composite_publishers'] = df['composite_publishers'].fillna(df['EZB_publishers'])

# 1.5 Diamond Open Access
def determine_if_published_ver_oa_fee(data):
    if not data:
        return None

    data = str(data).strip()
    data = data.replace('[', '').replace(']', '').replace("'", "")

    if ',' in data:
        answers = data.split(',')
        return 'no' if 'no' in answers else 'yes'

    return data

def determine_if_diamond_oa(row):
    if row['composite_OA_results'] == 'oa' and row['published_version_oa_fee'] == 'no' and (math.isnan(row['composite_apc']) or row['composite_apc'] is None):
        return True
    else:
        return False

df['published_version_oa_fee'] = df['SR_published_version_oa_fees'].apply(determine_if_published_ver_oa_fee)
df['diamond_oa_status'] = df.apply(determine_if_diamond_oa, axis=1)

# 2. Number of journals per ERIC collection area 
journals_per_collection_area = df['ERIC Topic Area'].value_counts()

# 3. Publishing Models
# 3.1 Open Access
open_alex_oa_count = df['openalex_is_oa'].value_counts()
open_alex_oa_percent = df['openalex_is_oa'].value_counts()
ezb_oa_count = df['EZB_price_for_reading_access'].value_counts()
ezb_oa_percent = df['EZB_price_for_reading_access'].value_counts(normalize=True) * 100

composite_oa_count = df['composite_OA_results'].value_counts()
composite_oa_percent = df['composite_OA_results'].value_counts(normalize=True) * 100
composite_oa_df = df[df['composite_OA_results'] == 'oa']

# 3.2 Subscription
subscription_journals_df = df[df['composite_OA_results'] == 'no']

# 3.3 Diamond OA
diamond_journals_df = df[df['diamond_oa_status'] == True]

# 4. Countries
countries_count = df['composite_country'].value_counts()
countries_percent = df['composite_country'].value_counts(normalize=True) * 100

# 5 Impact Factors
# 5.1 Total Impact Factors
total_h_index = df['openalex_h_index'].describe()
total_2_yr_impact = df['openalex_impact_factor'].describe()

# 5.2 Subscription Impact Factors
subscription_h_index = subscription_journals_df['openalex_h_index'].describe()
subscription_2yr_impact = subscription_journals_df['openalex_impact_factor'].describe()

# 5.3 OA Impact Factors
oa_h_index = composite_oa_df['openalex_h_index'].describe()
oa_2yr_impact = composite_oa_df['openalex_impact_factor'].describe()

# 5.4 Diamond Impact Factors
diamon_h_index = diamond_journals_df['openalex_h_index'].describe()
diamond_2_yr_impact = diamond_journals_df['openalex_impact_factor'].describe()

# 6. APC Fees
composite_apc_describe = df['composite_apc'].describe()

apc_idx = df['composite_apc'].idxmax()
highest_apc = df.loc[apc_idx, ['Journal Name', 'issn_l', 'composite_apc']]

# 7. Publishers
# 7.1 Publisher Count
publishers_count = df['composite_publishers'].value_counts()

# 7.2 Highest APC Publishers
threshold = df['composite_apc'].quantile(0.75)
top_25_percent_apc_df = df[df['composite_apc'] >= threshold]
high_apc_publishers = top_25_percent_apc_df['composite_publishers']
high_apc_publishers_count = high_apc_publishers.value_counts()

# 7.3 Types of Publishers
grouped_df = df.groupby(['SR_publisher_type', 'Journal Name'])['composite_apc'].max().reset_index()
sorted_df = grouped_df.sort_values(['SR_publisher_type', 'composite_apc'], ascending=[True, False])

publisher_types = ['Commercial Publisher', 'University Publisher', 'Society Publisher']
for publisher_type in publisher_types:
    selected_publisher_type_df = df[df['SR_publisher_type'] == publisher_type]
    publisher_column = selected_publisher_type_df['composite_publishers']
    publishers_per_type = selected_publisher_type_df['composite_publishers'].nunique()
    journals_per_type = selected_publisher_type_df['Journal Name'].nunique()


# 7.4 Publisher-based OA publishing schemes

def unpack_oa_schemes(data):
    if not data:
        return None

    data = str(data).strip()
    data = data.replace('[', '').replace(']', '').replace("'", "")

    policies_list = []
    if ',' in data:
        policies = data.split(',')
        for policy in policies:
            policies_list.append(policy.strip())
        return policies_list
    else:
        return data

df['oa_schemes'] = df['SR_oa_schemes'].apply(unpack_oa_schemes)
df_expanded = df['oa_schemes'].explode()
df_expanded = df_expanded.dropna()

print(df_expanded.value_counts(normalize=True) * 100)


# 8. Regression: APC and Impact Factor
# 8.1 APC & H-Index
# Include only rows that have APC and H-Index
df['h_index_per_apc'] = df['openalex_h_index'].where(df['composite_apc'].notnull())
df_filtered_h_index = df[df['h_index_per_apc'].notnull()]

# Calculate correlation
correlation = df_filtered_h_index['composite_apc'].corr(df_filtered_h_index['h_index_per_apc'])

# Regression Analysis
X = df_filtered_h_index['h_index_per_apc']
y = df_filtered_h_index[['composite_apc']]
model = sm.OLS(y, X).fit()
analysis_summary_h_index = model.summary()

# 8.2 APC & 2-Year Impact Factor
# Include only rows that have APC and 2-year impact factor
df['impact_factor_per_apc'] = df['openalex_impact_factor'].where(df['composite_apc'].notnull())
df_filtered_impact_factor = df[df['impact_factor_per_apc'].notnull()]

# Calculate correlation
correlation = df_filtered_impact_factor['composite_apc'].corr(df_filtered_impact_factor['impact_factor_per_apc'])

# Regression Analysis
X = df_filtered_impact_factor['impact_factor_per_apc']
y = df_filtered_impact_factor['composite_apc']
model = sm.OLS(y, X).fit()
analysis_summary_2yr_impact = model.summary()