import pandas as pd

file = 'Step3_Results.xlsx'
df = pd.read_excel(file)

# Find journals in more than one topic area

# Number of journals index per ERIC topic area

print(df.count())
