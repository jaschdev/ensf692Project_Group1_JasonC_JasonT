"""
data_loader.py

Handles reading and merging of raw datasets into a clean, combined Pandas DataFrame.

Responsibilities:
- Load at least 3 Excel files into DataFrames
- Merge datasets using at least 2 merge/join operations
- Remove duplicate rows/columns after merge
- Create and return a hierarchically indexed DataFrame (row or column)
- Sort data based on the index
- Handle null values and data mismatches

Note:
No hardcoded data should be used—only column names may be specified explicitly.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def data_loader():

    ## ----------- Importing Data Files ------------
    census_init = pd.read_csv('data/2021_Federal_Census_Population_and_Dwellings_by_Community_20250611.csv')
    assessment_init = pd.read_csv('data/Assessments_by_Community_20250609.csv')
    business_init = pd.read_csv('data/Calgary_Business_Licences_20250611.csv')
    wards_init = pd.read_csv('data/Communities_by_Ward_20250609.csv')
    crime_init = pd.read_csv('data/Community_Crime_Statistics_20250611.csv')

    # Print crime_init dataframe for verification
    # print(crime_init.head())

    # Find relevant categories and years in the crime dataset
    # print(crime_init['Category'].unique())
    # Print(crime_init['Year'].unique())

    ###  --------- Clean Data Files ----------

    # Keep only total and gender total columns
    census = census_init.drop(census_init.columns[3:53], axis=1)
    census.drop(census_init.columns[54:97], axis=1, inplace = True)
    census.drop(census_init.columns[98:], axis=1, inplace = True)

    # Drop all percentage columns, keep specific demographics
    # census = census_init.drop(census_init.columns[7:11], axis=1)
    # census.drop(census_init.columns[32:53], axis=1, inplace = True)
    # census.drop(census_init.columns[75:97], axis=1, inplace = True)
    # census.drop(census_init.columns[118:], axis=1, inplace = True)

    # print(census.isnull().any())
    # print(census.shape)
    census.dropna(inplace = True)
    # print(census.shape)

    ## Cleaning Assessment data 
    assessment = assessment_init
    # assessment['Community name'] = assessment['Community name'].str.capitalize()
    assessment['Estimated Community Property Base In Millions ($)'] = assessment['Number of taxable accounts'] * assessment['Median assessed value'] / 1000000
    # Instead of taking data by year, take the average of the two years, when giving data will include a disclaimer
    assessment = assessment.groupby('COMM_CODE', as_index=False)[[
        'Number of taxable accounts',
        'Median assessed value',
        'Estimated Community Property Base In Millions ($)'
    ]].mean()
    # print(assessment.isnull().any())

    ## Cleaning Business data 
    business = business_init.drop(['GETBUSID', 'TRADENAME', 'HOMEOCCIND', 'ADDRESS', 'LICENCETYPES', 'EXP_DT', 'JOBSTATUSDESC', 'POINT', 'GLOBALID'], axis=1)
    business['BUSINESS_COUNT'] = 1
    business.dropna(inplace = True)
    # converting date format into year and month columns
    business['Year'] = business['FIRST_ISS_DT'].astype(str).str[:4].astype(int)
    business['Month'] = business['FIRST_ISS_DT'].astype(str).str[5:7].astype(int)
    business.drop(['FIRST_ISS_DT'], axis=1, inplace = True)
    # print(business.isnull().any())
    # print(business.shape)
    business = business.groupby(['COMDISTNM', 'COMDISTCD', 'Year', 'Month']).sum(numeric_only=True).reset_index()
    # print(business.shape)
    # TBD, make business count = # of business opened in this time, or = # of business existing at this time
    # process before or after decision

    ## Cleaning Wards data 
    wards = wards_init.drop(['SRG', 'COMM_STRUCTURE'], axis=1)
    # print(wards.isnull().any())

    ## Cleaning Crime data 
    crime = crime_init
    # print(crime.isnull().any())

    ### -------------------- MERGING OF DATA --------------------

    ## Merge 1 wards plus business --------------------
    print("wards size:", wards.shape)
    print("business size:", business.shape)
    merge1_df = pd.merge(wards, business, how='outer', left_on='COMM_CODE', right_on='COMDISTCD')
    merge1_df['Community'] = merge1_df['NAME']
    merge1_df = merge1_df.drop(['COMDISTNM', 'COMDISTCD', 'NAME'], axis=1)
    print("merge1 size:", merge1_df.shape)
    # print(merge1_df.head())
    print("merge1 columns:", merge1_df.columns)
    # print(merge1_df.isnull().any())
    merge1_df.to_csv('check1.csv', index=False)


    ## Merge 1.5 wards plus crime --------------------
    print("crime size:", crime.shape)
    merge1_5_df = pd.merge(wards, crime, how='outer', left_on='NAME', right_on='Community').drop(['NAME'], axis=1)
    print("merge1.5 size:", merge1_5_df.shape)
    merge1_5_df.to_csv('check1_5.csv', index=False)
    # print(merge1_5_df.head())
    print("merge1.5 columns:", merge1_5_df.columns)
    # print(merge1_5_df.isnull().any())

    ## Merge 2 - merge1 and merge1.5 --------------------
    merge2_df = pd.merge(merge1_df, merge1_5_df, how="outer",
                        left_on = ['COMM_CODE', 'CLASS', 'CLASS_CODE', 'SECTOR', 'WARD_NUM', 'Community', 'Year', 'Month', ],
                        right_on = ['COMM_CODE', 'CLASS', 'CLASS_CODE', 'SECTOR', 'WARD_NUM', 'Community', 'Year', 'Month'])
    print("merge2 size:", merge2_df.shape)
    # print(merge2_df.head())
    # print(merge2_df.isnull().any())
    merge2_df.to_csv('check2.csv', index=False)

    ## Merge 3 plus assessment --------------------
    print("assessment size:", assessment.shape)
    merge3_df = pd.merge(merge2_df, assessment, how='outer', left_on='COMM_CODE', right_on='COMM_CODE')
    print("merge3 size:", merge3_df.shape)
    # print(merge3_df.head())
    merge3_df.to_csv('check3.csv', index=False)

    ## Merge 4 plus census --------------------
    print("census size:", census.shape)
    census['COMM_CODE'] = census['COMMUNITY_CODE']
    census = census.drop(['COMMUNITY_CODE', 'COMMUNITY_NAME'], axis=1)
    merge4_df = pd.merge(merge3_df, census, how='outer', left_on='COMM_CODE', right_on='COMM_CODE')

    print("merge4 size:", merge4_df.shape)
    # print(merge4_df.head())
    merge4_df.to_csv('check4.csv', index=False)

if __name__ == "__main__":
    data_loader()