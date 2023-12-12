#!/usr/bin/env python
# coding: utf-8

# In[121]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


# In[122]:


df = pd.read_csv('airbnb_cleaning-15.csv', header=0, skiprows=1)
df.head()

for value in df['id']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")
       
# Here we can see that the 'id' column has mixed types (some are <class 'str'> and some 
# are <class 'int'>)


# In[123]:


df.shape


# In[124]:


df['id'] = pd.to_numeric(df['id'], errors='coerce')


# In[125]:


has_nan_values = df['id'].isna().any()

if has_nan_values:
    print("The 'id' column contains NaN values.")
else:
    print("The 'id' column does not contain NaN values.")
    
#Now we know that there are NaN values that we have to deal with.


# In[126]:


nan_rows = df[df['id'].isna()]
print(nan_rows)
print(f"Number of rows with NaN in 'id': {len(nan_rows)}")

type_of_id = type(df.at[1673, 'id'])
print(type_of_id)


# In[127]:


has_duplicates = df['id'].duplicated().any()

if has_duplicates:
    print("The 'id' column contains duplicate values.")
else:
    print("The 'id' column does not contain duplicate values.")


# In[128]:


duplicates = df[df['id'].duplicated(keep=False)]
print(duplicates)


# In[129]:


df['id'].fillna(0, inplace=True)
df['id'] = df['id'].astype(int)

for value in df['id']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[130]:


df.shape


# In[131]:


# Now the id column is fully cleaned. We filled the rows with 'id' = NaN with 0.
# Let's look at the name column to see if there are any NaN or non-String values.
nan_rows = df[df['name'].isna()]
print(f"Number of rows with NaN in 'id': {len(nan_rows)}")


# In[132]:


# Because a description of the airbnb isn't necessary to the dataset, as long as it has a unique id, we will not 
# drop the rows that have NaN values.
# Let's see if there are duplicates.
has_duplicates2 = df['name'].duplicated().any()

if has_duplicates2:
    print("The 'name' column contains duplicate values.")
else:
    print("The 'name' column does not contain duplicate values.")


# In[133]:


duplicates2 = df[df['name'].duplicated(keep=False)]
print(duplicates2)


# In[134]:


df2= df.dropna(subset=['name'])


# In[135]:


nan_rows2 = df2[df2['name'].isna()]
print(f"Number of rows with NaN in 'id': {len(nan_rows2)}")


# In[136]:


has_duplicates3 = df2['name'].duplicated().any()

if has_duplicates3:
    print("The 'name' column contains duplicate values.")
else:
    print("The 'name' column does not contain duplicate values.")


# In[137]:


duplicates3 = df2[df2['name'].duplicated(keep=False)]
print(duplicates3)


# In[138]:


df['name'].fillna('', inplace=True)


# In[139]:


# None of the names are duplicated. We will leave the 'name' unchanged
for value in df['name']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[140]:


subset_with_nan = df.loc[df['name'].isna()]
print(subset_with_nan)


# In[141]:


# Replaced NaN values in the 'name' column with empty strings so that everything is a string type/
#In the 'host   id' column, there are a mix of strings and integers. Let us convert all the entries to integers.
df = df.rename(columns={'host   id': 'host_id'})
df.head()


# In[142]:


# All the values in the name column are strings, except for the NaN values.
# Let's move onto the next column

for value in df['host_id']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[143]:


# Let's make everything in the host_id column the same type. Right now, it is a mix of strings and ints.
df['host_id'] = pd.to_numeric(df['host_id'], errors='coerce')


# In[144]:


has_nan_values2 = df['host_id'].isna().any()

if has_nan_values2:
    print("The 'host_id' column contains NaN values.")
else:
    print("The 'host_id' column does not contain NaN values.")


# In[145]:


nan_rows2 = df[df['host_id'].isna()]
print(nan_rows2)
print(f"Number of rows with NaN in 'host_id': {len(nan_rows2)}")


# In[146]:


# The host_id contains NaN values, so let us make all the entities type int. Filled NaN values with 0, so that everything is type integer
df['host_id'].fillna(0, inplace=True)
df['host_id'] = df['host_id'].astype(int)

for value in df['host_id']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[147]:


# Let's move onto 'host_name' column. I want to see if the duplicate 'host_id' rows correspond to the same host_names
has_duplicates4 = df['host_id'].duplicated().any()

if has_duplicates4:
    print("The 'host_id' column contains duplicate values.")
else:
    print("The 'host_id' column does not contain duplicate values.")


# In[148]:


duplicates4 = df['host_id'].duplicated()
numdupes = duplicates4.sum()
duplicate_rows = df[duplicates4]
print(duplicate_rows)
print(numdupes)


# In[149]:


desired_host_id = 30283594
rows_with_host_id = df[df['host_id'] == desired_host_id]
print(rows_with_host_id)


# In[150]:


# Moving onto host_name column
for value in df['[host_name]']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[151]:


df = df.rename(columns={'[host_name]': 'host_name'})
df.head()


# In[152]:


df['host_name'].fillna('', inplace=True)


# In[153]:


# Moving onto neighbourhood group
grouped = df.groupby('neighbourhood group')
for group_name, group_data in grouped:
    print(f"Group Name: {group_name}")
    print("\n")


# In[154]:


# Fix the neighborhood group categories
category_mapping = {
    '  bronx_borugh': 'Bronx',
    'B-r-0-n-x': 'Bronx',
    'Brooklyn - **Borough**': 'Brooklyn',
    'Brooklyn Borough': 'Brooklyn',
    'brklyn': 'Brooklyn',
    'broxn   ': 'Bronx'
}

# Replace incorrect categories with correct ones
df['neighbourhood group'] = df['neighbourhood group'].replace(category_mapping)

# Verify the updated categories
unique_categories = df['neighbourhood group'].unique()
print("Updated Unique Categories:")
print(unique_categories)


# In[155]:


nan_rows3 = df[df['neighbourhood group'].isna()]
print(nan_rows3)
print(f"Number of rows with NaN in 'id': {len(nan_rows3)}")


# In[156]:


# Let's move onto the 'neighbourhood' column.
grouped = df.groupby('neighbourhood')
for group_name, group_data in grouped:
    print(f"Group Name: {group_name}")
    print("\n")


# In[157]:


category_mapping = {
    'AllertonBronx-Bronx': 'Allerton',
    'AstoriaQueens-Queens': 'Astoria',
    'Bay Terrace, Staten Island': 'Bay Terrace',
    'Bedford-StuyvesantBrooklyn - **Borough**-Brooklyn - **Borough**': 'Bedford-Stuyvesant',
    'Bedford-StuyvesantBrooklyn Borough-Brooklyn Borough': 'Bedford-Stuyvesant',
    'Bedford-StuyvesantBrooklyn-Brooklyn': 'Bedford-Stuyvesant',
    'Bedford-Stuyvesantbrklyn-brklyn': 'Bedford-Stuyvesant',
    'Borough ParkBrooklyn-Brooklyn': 'Borough Park',
    'BriarwoodQueens-Queens': 'Briarwood',
    'Brooklyn HeightsBrooklyn-Brooklyn': 'Brooklyn Heights',
    'BushwickBrooklyn - **Borough**-Brooklyn - **Borough**': 'Bushwick',
    'BushwickBrooklyn Borough-Brooklyn Borough': 'Bushwick',
    'BushwickBrooklyn-Brooklyn': 'Bushwick',
    'Carroll GardensBrooklyn-Brooklyn': 'Carroll Gardens',
    'ChelseaManhattan-Manhattan': 'Chelsea',
    'ChinatownManhattan-Manhattan': 'Chinatown',
    'Civic CenterManhattan-Manhattan': 'Civic Center',
    'Clinton HillBrooklyn-Brooklyn': 'Clinton Hill',
    'Cobble HillBrooklyn Borough-Brooklyn Borough': 'Cobble Hill',
    'Concourse Village': 'Concourse',
    'Crown HeightsBrooklyn-Brooklyn': 'Crown Heights',
    'Cypress HillsBrooklyn-Brooklyn': 'Cypress Hills',
    'Ditmars SteinwayQueens-Queens': 'Ditmars Steinway',
    'Downtown BrooklynBrooklyn-Brooklyn': 'Downtown Brooklyn',
    'East ElmhurstQueens-Queens': 'East Elmhurst',
    'East FlatbushBrooklyn-Brooklyn': 'East Flatbush',
    'East HarlemManhattan-Manhattan': 'East Harlem',
    'East New YorkBrooklyn-Brooklyn': 'East New York',
    'East VillageManhattan-Manhattan': 'East Village',
    'ElmhurstQueens-Queens': 'Elmhurst',
    'Far RockawayQueens-Queens': 'Far Rockaway'
}

df['neighbourhood'] = df['neighbourhood'].replace(category_mapping)

# Verify the updated categories
grouped = df.groupby('neighbourhood')
for group_name, group_data in grouped:
    print(f"Group Name: {group_name}")
    print("\n")


# In[158]:


category_mapping2 = {
    'Financial DistrictManhattan-Manhattan': 'Financial District',
    'FlatbushBrooklyn-Brooklyn': 'Flatbush',
    'FlatlandsBrooklyn-Brooklyn': 'Flatlands',
    'FlushingQueens-Queens': 'Flushing',
    'Forest HillsQueens-Queens': 'Forest Hills',
    'Fort GreeneBrooklyn - **Borough**-Brooklyn - **Borough**': 'Fort Greene',
    'Fort GreeneBrooklyn-Brooklyn': 'Fort Greene',
    'GowanusBrooklyn-Brooklyn': 'Gowanus',
    'GreenpointBrooklyn-Brooklyn': 'Greenpoint',
    'Greenwich VillageManhattan-Manhattan': 'Greenwich Village',
    'HarlemManhattan-Manhattan': 'Harlem',
    'Hell\'s KitchenManhattan-Manhattan': 'Hell\'s Kitchen',
    'HighbridgeBronx-Bronx': 'Highbridge',
    'HolliswoodQueens-Queens': 'Holliswood',
    'InwoodManhattan-Manhattan': 'Inwood',
    'Jackson HeightsQueens-Queens': 'Jackson Heights',
    'JamaicaQueens-Queens': 'Jamaica',
    'KensingtonBrooklyn - **Borough**-Brooklyn - **Borough**': 'Kensington',
    'KensingtonBrooklyn-Brooklyn': 'Kensington',
    'KingsbridgeBronx-Bronx': 'Kingsbridge',
    'Kingsbridgebroxn   -broxn   ': 'Kingsbridge',
    'Kips BayManhattan-Manhattan': 'Kips Bay',
    'LaureltonQueens-Queens': 'Laurelton',
    'Little ItalyManhattan-Manhattan': 'Little Italy',
    'Long Island CityQueens-Queens': 'Long Island City',
    'LongwoodBronx-Bronx': 'Longwood',
    'Lower East SideManhattan-Manhattan': 'Lower East Side',
    'MidtownManhattan-Manhattan': 'Midtown'
}

df['neighbourhood'] = df['neighbourhood'].replace(category_mapping2)

# Verify the updated categories
grouped = df.groupby('neighbourhood')
for group_name, group_data in grouped:
    print(f"Group Name: {group_name}")
    print("\n")


# In[159]:


category_mapping3 = {
    'MidwoodBrooklyn-Brooklyn': 'Midwood',
    'Morningside HeightsManhattan-Manhattan': 'Morningside Heights',
    'Mott HavenBronx-Bronx': 'Mott Haven',
    'Murray HillManhattan-Manhattan': 'Murray Hill',
    'NolitaManhattan-Manhattan': 'Nolita',
    'Ozone ParkQueens-Queens': 'Ozone Park',
    'Park SlopeBrooklyn-Brooklyn': 'Park Slope',
    'Prospect HeightsBrooklyn-Brooklyn': 'Prospect Heights',
    'Prospect-Lefferts GardensBrooklyn-Brooklyn': 'Prospect-Lefferts Gardens',
    'Richmond HillQueens-Queens': 'Richmond Hill',
    'RidgewoodQueens-Queens': 'Ridgewood',
    'Roosevelt IslandManhattan-Manhattan': 'Roosevelt Island',
    'RosedaleQueens-Queens': 'Rosedale',
    'SoHoManhattan-Manhattan': 'SoHo',
    'South SlopeBrooklyn-Brooklyn': 'South Slope',
    'Springfield GardensQueens-Queens': 'Springfield Gardens',
    'St. AlbansQueens-Queens': 'St. Albans',
    'St. GeorgeStaten Island-Staten Island': 'St. George',
    'StapletonStaten Island-Staten Island': 'Stapleton',
    'Stuyvesant TownManhattan-Manhattan': 'Stuyvesant Town',
    'SunnysideQueens-Queens': 'Sunnyside',
    'Theater DistrictManhattan-Manhattan': 'Theater District',
    'Upper East SideManhattan-Manhattan': 'Upper East Side',
    'Upper West SideManhattan-Manhattan': 'Upper West Side',
    'Washington HeightsManhattan-Manhattan': 'Washington Heights',
    'West VillageManhattan-Manhattan': 'West Village',
    'WilliamsburgBrooklyn - **Borough**-Brooklyn - **Borough**': 'Williamsburg',
    'WilliamsburgBrooklyn Borough-Brooklyn Borough': 'Williamsburg',
    'WilliamsburgBrooklyn-Brooklyn': 'Williamsburg',
    'Windsor TerraceBrooklyn-Brooklyn': 'Windsor Terrace'
}

df['neighbourhood'] = df['neighbourhood'].replace(category_mapping3)

# Verify the updated categories
grouped = df.groupby('neighbourhood')
for group_name, group_data in grouped:
    print(f"Group Name: {group_name}")
    print("\n")


# In[160]:


nan_rows5 = df[df['neighbourhood'].isna()]
print(nan_rows5)
print(f"Number of rows with NaN in 'id': {len(nan_rows5)}")


# In[161]:


# There are 30 rows with NaN values for the 'neighbourhood'


# In[162]:


df['neighbourhood'].fillna('Unknown', inplace=True)


# In[163]:


nan_rows5 = df[df['neighbourhood'].isna()]
print(nan_rows5)
print(f"Number of rows with NaN in 'id': {len(nan_rows5)}")


# In[164]:


unknown_rows = df[df['neighbourhood']=='Unknown']
print(unknown_rows)
print(unknown_rows.shape)


# In[165]:


# Let's move onto Latitude and Longitude
for value in df['latitude']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[166]:


df['latitude'] = df['latitude'].str.replace('N', '')  # Remove 'N' characters
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')  # Convert to numeric

for value in df['latitude']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[167]:


for value in df['latitude']:
    print(f"latitude: {value}")


# In[168]:


for value in df['longitude']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[169]:


df['longitude'] = df['longitude'].str.replace('° W', '')
df['longitude'] = df['longitude'].str.replace('W', '')


# In[170]:


for value in df['longitude']:
    print(f"longitude: {value}")


# In[171]:


df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')  # Convert to numeric

for value in df['longitude']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[172]:


nan_rows6 = df[df['latitude'].isna()]
print(nan_rows6)
print(f"Number of rows with NaN in 'latitude': {len(nan_rows6)}")


# In[173]:


nan_rows7 = df[df['longitude'].isna()]
print(nan_rows7)
print(f"Number of rows with NaN in 'longitude': {len(nan_rows7)}")


# In[174]:


df.head(50)


# In[175]:


# Now let us clean up 'room and type' column
unique_categories = df['room and type'].unique()
num_categories = len(unique_categories)
print(unique_categories)


# In[176]:


# There are some duplicate categories to clean up.
rooms_mapping = {
    'Room Type Private': 'Private room',
    'Entire home/apt ': 'Entire home/apt',
    'Privatè-Room': 'Private room',
    'Shared room ': 'Shared room'
}

df['room and type'] = df['room and type'].replace(rooms_mapping)

unique_categories = df['room and type'].unique()
print("Updated Unique Categories:")
print(unique_categories)


# In[177]:


nan_row8 = df[df['room and type'].isna()]
print(nan_row8)
print(f"Number of rows with NaN in 'room and type': {len(nan_row8)}")


# In[178]:


# Next column to clean up is 'minimum nights'
for value in df['minimum nights']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[179]:


unique_categories = df['minimum nights'].unique()
print(unique_categories)


# In[180]:


df['minimum nights'] = df['minimum nights'].str.replace(' nights', '')
unique_categories = df['minimum nights'].unique()
print(unique_categories)


# In[181]:


category_counts = df.groupby('minimum nights').size().reset_index(name='count')
print(category_counts)


# In[182]:


nan_row9 = df[df['minimum nights'].isna()]
print(nan_row9)
print(f"Number of rows with NaN in 'minimum nights': {len(nan_row9)}")


# In[183]:


df['minimum nights'] = pd.to_numeric(df['minimum nights'], errors='coerce')
df['minimum nights'] = df['minimum nights'].astype(int)

for value in df['minimum nights']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[184]:


df.head(50)


# In[185]:


# Next column to cleab up is number of reviews (total)
for value in df['number of reviews (total)']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[186]:


unique_categories = df['number of reviews (total)'].unique()
print(unique_categories)


# In[187]:


nan_row9 = df[df['number of reviews (total)'].isna()]
print(nan_row9)
print(f"Number of rows with NaN in 'number of reviews (total)': {len(nan_row9)}")


# In[188]:


is_int_column = df['number of reviews (total)'].apply(lambda x: isinstance(x, int)).all()

if is_int_column:
    print(f"All values in 'number of reviews' are of type int.")
else:
    print(f"Not all values in 'number of reviews' are of type int.")


# In[189]:


# Nothing to clean up in 'number of reviews (total)' column. Next is 'last review (date)'
for value in df['last review (date)']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[190]:


nan_row10 = df[df['last review (date)'].isna()]
print(nan_row10)
print(f"Number of rows with NaN in 'last review (date)': {len(nan_row10)}")


# In[191]:


# Lots of rows have NaN for 'last review (date)'
column_name = 'last review (date)'
df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d', errors='coerce')
df[column_name].fillna(pd.NaT, inplace=True)
print(df.head())


# In[192]:


is_datetime_column = df['last review (date)'].apply(lambda x: isinstance(x, datetime)).all()

if is_datetime_column:
    print(f"All values in 'last review' are of type datetime.")
else:
    print(f"Not all values in 'last review' are of type datetime.")


# In[193]:


# Next column to clean up is 'reviews per month'. The entries should all be floats.
are_all_floats = (df['reviews per month'].dtype == 'float64') or (df[column_name].dtype == 'float32')

if are_all_floats:
    print(f"All entries in 'reviews per month' are floats.")
else:
    print(f"Not all entries in 'reviews per month' are floats.")


# In[194]:


# Nothing to clean up in reviews per month. Next column is 'floor' column
unique_categories = df['floor'].unique()
print(unique_categories)


# In[195]:


floor_mapping = {
    'First Floor': '1',
    'Fifth Floor': '5',
    'Second Floor': '2',
    '1st-floor': '1',
    '5th Floor': '5',
    'Third Floor': '3',
    'Eighth Floor': '8',
    'Sixth Floor': '6',
    'Fourth Floor': '4',
    'Tenth Floor': '10',
    'Seventeenth Floor': '17',
    'Thirteenth Floor': '13',
    'Eleventh Floor': '11',
    'Seventh Floor': '7',
    'Ninth Floor': '9',
    'Twentieth Floor': '20',
    'Hundreth Floor': '100',
    'Lower Level': '0',
    'Sixteenth Floor': '16'
}

df['floor'] = df['floor'].replace(floor_mapping)

unique_categories = df['floor'].unique()
print("Updated Unique Categories:")
print(unique_categories)


# In[196]:


df['floor'] = pd.to_numeric(df['floor'], errors='coerce')
df['floor'] = df['floor'].astype(int)

for value in df['floor']:
    value_type = type(value)
    print(f"Data type of entity: {value_type}")


# In[197]:


nan_row11 = df[df['floor'].isna()]
print(nan_row11)
print(f"Number of rows with NaN in 'floor': {len(nan_row11)}")


# In[198]:


# Next column to clean up is 'noise.dB.'
df = df.rename(columns={'noise.dB.': 'noise (dB)'})
df.head()


# In[199]:


df['noise (dB)'] = df['noise (dB)'].str.replace('dB', '')
df['noise (dB)'] = pd.to_numeric(df['noise (dB)'], errors='coerce')


# In[200]:


df.head(50)


# In[201]:


are_all_floats = (df['noise (dB)'].dtype == 'float64') or (df[column_name].dtype == 'float32')

if are_all_floats:
    print(f"All entries in 'noise' are floats.")
else:
    print(f"Not all entries in 'noise' are floats.")


# In[202]:


# Next column to clean up is 'Unnamed: 15'
num_rows = df.shape[0]
print(f"Number of Rows in the DataFrame: {num_rows}")


# In[203]:


column_name = 'Unnamed: 15'

# Count the number of NaN values in the specified column
num_nan_values = df[column_name].isna().sum()

# Print the number of NaN values
print(f"Number of NaN Values in '{column_name}': {num_nan_values}")


# In[204]:


non_null_mask = df['Unnamed: 15'].notna()
non_null_values = df.loc[non_null_mask]
print(non_null_values)


# In[205]:


# There is nothing in this column, so we are going to discard of it.
df.drop('Unnamed: 15', axis=1, inplace=True)


# In[209]:


df.head()


# In[210]:


print("Column Names:")
for column in df.columns:
    print(column)


# In[211]:


# Last column to clean up is price
df = df.rename(columns={'price': 'price ($)'})
df['price ($)'] = df['price ($)'].str.replace('approx', '')
df['price ($)'] = df['price ($)'].str.replace('open to negotiate', '')
df['price ($)'] = df['price ($)'].str.replace('\$', '', regex=False)
df['price ($)'] = df['price ($)'].str.replace(r'^\$', '', regex=True)
df.head(50)


# In[212]:


df['price ($)'] = pd.to_numeric(df['price ($)'], errors='coerce')


# In[213]:


df.head(50)


# In[218]:


df_0 = df[df['price ($)']== 0]
df_NaN = df[df['price ($)'].isna()]
print(df_0)
print(df_0.shape)
print(df_NaN)
print(df_NaN.shape)


# In[214]:


csv_filename = 'airbnb_final_cleaned.csv'
df.to_csv(csv_filename, index=False)


# In[215]:


print(df.shape)

