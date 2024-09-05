import pandas as pd

df = pd.read_csv('NYPD_Shooting_Incident_Data__Historic_.csv')
print(df.info())
print(df.isnull().sum())

# Perpetrator Information
# Perpetrator Information
perp_race_counts = df['PERP_RACE'].value_counts()
perp_race_counts = perp_race_counts[perp_race_counts.index != '(null)'] 
perp_race_counts.to_csv('perp_race_counts.csv', header=True)
boro_counts = df['BORO'].value_counts()
precinct_counts = df['PRECINCT'].value_counts()
perp_age_group_counts = df['PERP_AGE_GROUP'].value_counts()
perp_race_counts.to_csv('perp_race_counts.csv', header=True)
boro_counts.to_csv('boro_counts.csv', header=True)
precinct_counts.to_csv('precinct_counts.csv', header=True)
perp_age_group_counts.to_csv('perp_age_group_counts.csv', header=True)

# Victim Information
vic_age_group_counts = df['VIC_AGE_GROUP'].value_counts()
vic_race_counts = df['VIC_RACE'].value_counts()
vic_sex_counts = df['VIC_SEX'].value_counts()
vic_age_group_counts.to_csv('vic_age_group_counts.csv', header=True)
vic_race_counts.to_csv('vic_race_counts.csv', header=True)
vic_sex_counts.to_csv('vic_sex_counts.csv', header=True)

# Statistical Murder Flag Information
statistical_murder_flag_counts = df['STATISTICAL_MURDER_FLAG'].value_counts()
statistical_murder_flag_counts.to_csv('statistical_murder_flag_counts.csv', header=True)

# Grouped Information
grouped_df = df.groupby(['PERP_RACE', 'PERP_SEX', 'PERP_AGE_GROUP'])
murder_percentages = grouped_df['STATISTICAL_MURDER_FLAG'].mean() * 100
murder_percentages.to_csv('murder_percentages.csv', header=True)

# Time Information
df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S')
df['OCCUR_HOUR'] = df['OCCUR_TIME'].dt.hour
bins = list(range(25))
labels = [f'{i}-{i+1}' for i in range(24)]
df['OCCUR_HOUR_INTERVAL'] = pd.cut(df['OCCUR_HOUR'], bins=bins, labels=labels, right=False)
occur_hour_interval_counts = df['OCCUR_HOUR_INTERVAL'].value_counts().sort_index()
occur_hour_interval_counts.to_csv('occur_hour_interval_counts.csv', header=True)

# Date Information
df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE'])
df['OCCUR_MONTH'] = df['OCCUR_DATE'].dt.month
occur_month_counts = df['OCCUR_MONTH'].value_counts().sort_index()
occur_month_counts.to_csv('occur_month_counts.csv', header=True)
df['OCCUR_YEAR'] = df['OCCUR_DATE'].dt.year
occur_year_counts = df['OCCUR_YEAR'].value_counts().sort_index()
occur_year_counts.to_csv('occur_year_counts.csv', header=True)

# Cross-tabulation Information
sex_comparison = pd.crosstab(df['PERP_SEX'], df['VIC_SEX'])
sex_comparison.to_csv('sex_comparison.csv')
race_comparison = pd.crosstab(df['PERP_RACE'], df['VIC_RACE'])
race_comparison.to_csv('race_comparison.csv')

# Age Group Information
valid_age_groups = ['<18', '18-24', '25-44', '45-64', '65+', 'UNKNOWN']
df['PERP_AGE_GROUP'] = pd.Categorical(df['PERP_AGE_GROUP'], categories=valid_age_groups, ordered=True)
df['VIC_AGE_GROUP'] = pd.Categorical(df['VIC_AGE_GROUP'], categories=valid_age_groups, ordered=True)
df = df[df['PERP_AGE_GROUP'].isin(valid_age_groups) & df['VIC_AGE_GROUP'].isin(valid_age_groups)].copy()
age_comparison = pd.crosstab(df['PERP_AGE_GROUP'], df['VIC_AGE_GROUP'])
age_comparison.to_csv('age_comparison.csv')

# Filter out 'UNKNOWN' from 'PERP_AGE_GROUP'
df = df[df['PERP_AGE_GROUP'] != 'UNKNOWN']

# Group the data by perpetrator sex and age group, then count the number of incidents in each group
perp_sex_age_group_counts = df.groupby(['PERP_SEX', 'PERP_AGE_GROUP'], observed=True).size()

# Convert the Series to a DataFrame and rename the 0 column to 'COUNT'
perp_sex_age_group_counts = perp_sex_age_group_counts.reset_index(name='COUNT')

# Separate the data into two DataFrames, one for males and one for females
male_counts = perp_sex_age_group_counts[perp_sex_age_group_counts['PERP_SEX'] == 'M']
female_counts = perp_sex_age_group_counts[perp_sex_age_group_counts['PERP_SEX'] == 'F']

# Save the DataFrames to CSV files
male_counts.to_csv('male_counts.csv', index=False)
female_counts.to_csv('female_counts.csv', index=False)

# Extract unique races
perp_races = pd.DataFrame(df['PERP_RACE'].unique(), columns=['PERP_RACE'])
vic_races = pd.DataFrame(df['VIC_RACE'].unique(), columns=['VIC_RACE'])

# Extract unique age groups
perp_age_groups = pd.DataFrame(df['PERP_AGE_GROUP'].unique(), columns=['PERP_AGE_GROUP'])
vic_age_groups = pd.DataFrame(df['VIC_AGE_GROUP'].unique(), columns=['VIC_AGE_GROUP'])

# Save to CSV
perp_races.to_csv('perp_races.csv', index=False)
vic_races.to_csv('vic_races.csv', index=False)
perp_age_groups.to_csv('perp_age_groups.csv', index=False)
vic_age_groups.to_csv('vic_age_groups.csv', index=False)