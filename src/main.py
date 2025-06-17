"""
main.py

Entry point of the ENSF 692 Spring 2025 final project.

This script coordinates the overall program execution, including loading data,
getting user input, performing analysis, and exporting results.

Responsibilities:
- Call all main functions in proper ordercl
- Ensure no global variables are used
- Document structure clearly with inline comments

Note:
This file must be executable from the terminal and should orchestrate the full program.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():     

    # Load data from CSV files and perform initial cleaning    
    df = load_data()       
    print(df.head())

    # Generate and display plots based on the final DataFrame
    get_plots(df)



def load_data():

        """ ----------- Importing Data Files ------------
        """
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

        """ ----------- Clean Data Files ------------
        """

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

        """ ----------- Merge Data Files ------------
        """

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

        """ ----------- Final DataFrame ------------"""
        final_df = merge4_df.sort_values(['COMM_CODE', 'Year', 'Month'])
        # final_df = final_df.set_index(['COMM_CODE', 'Community', 'Year', 'Month'])
        final_df = final_df.set_index(['COMM_CODE', 'Community', 'Year', 'Month']).reset_index()
        final_df.to_csv('check5.csv', index=False)

        print("final_df columns:", final_df.columns)
        # Rename columns and make title case
        final_df = final_df.rename(columns={
            'COMM_CODE': 'Community Code',
            'CLASS': 'Class',
            'CLASS_CODE': 'Class Code',
            'SECTOR': 'Sector',
            'WARD_NUM': 'Ward Number',
            'BUSINESS_COUNT': 'Business Count',
            'Number of taxable accounts': 'Taxable Accounts',
            'Median assessed value': 'Median Assessed Value',
            'Estimated Community Property Base In Millions ($)': 'Estimated Property Base ($M)',
            'TOTAL_POP_HOUSEHOLD': 'Population Household',
            'TOTAL_POP_MEN': 'Population Men',
            'TOTAL_POP_WOMEN': 'Population Women'
        })
        # print first five rows
        final_df.head()

        # final_df.to_excel("final_dataframe.xlsx", index=True, header=True)

        return final_df

def get_plots(final_df):
    """
    Generates and displays various plots based on the final DataFrame.

    Args:
        final_df (DataFrame): The final DataFrame containing the cleaned and merged data.
    """
   
    # ----- Plot #1 Total Crime Per Year By Crime Category -----
    

    # Group by Category and Year, then sum Crime Count
    plot1_df = final_df.groupby(['Category', 'Year'])['Crime Count'].sum().reset_index()

    # Create a pivot table where rows = Year, columns = Category, values = total crime count
    plot1_pt = plot1_df.pivot(index='Year', columns='Category', values='Crime Count')

    # Plot each category's crime trend across years
    plot1_pt.plot(kind='line', marker='o', figsize=(12, 8))
    plt.title('Total Crime Count Per Year')
    plt.xlabel('Year')
    plt.ylabel('Total Crime Count')
    plt.grid(True)
    plt.legend(title='Crime Category', bbox_to_anchor=(1, 1), loc='upper right')
    plt.tight_layout()
    plt.show()

    # -----Plot #2 Total Crime Per Month Per Year -----
   
    # Group by Year and Month, then sum Crime Count
    plot2_df = final_df.groupby(['Year', 'Month'])['Crime Count'].sum().reset_index()

    # Pivot so rows = Month, columns = Year
    plot2_pt = plot2_df.pivot(index='Month', columns='Year', values='Crime Count')

    # Replace all 0s with NaN and drop years (columns) where all values are NaN
    plot2_pt = plot2_pt.replace(0, np.nan).dropna(axis=1, how='all')

    # Plot total crime per month for each year
    plot2_pt.plot(kind='line', marker='o', figsize=(12, 6))

    plt.title('Total Crime Per Month by Year')
    plt.xlabel('Month')
    plt.ylabel('Total Crime Count')
    plt.xticks(range(1, 13))
    plt.grid(True)
    plt.legend(title='Year', bbox_to_anchor=(1, 1), loc='upper right')
    plt.tight_layout()
    plt.show()

    
    # ----- Plot #3: Percent change of crime compared to previous year -----
   

    # Group by Year and get Total of Crime Count
    plot3_df = final_df.groupby('Year')['Crime Count'].sum().sort_index()

    # Remove years with 0 or NaN crime count
    plot3_df = plot3_df[plot3_df > 0]  # removes 0 and NaN

    # Compute percent change
    plot3_df = plot3_df.pct_change() * 100  # convert to percent

    # Plot
    plt.figure(figsize=(10, 5))
    plot3_df.dropna().plot(kind='bar', color='coral')

    plt.title('Year-over-Year % Change in Total Crime (Excludes Zero-Crime Years)')
    plt.xlabel('Year')
    plt.ylabel('Percent Change (%)')
    plt.axhline(0, color='gray', linestyle='--')  # Reference line at 0%
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

   

def get_user_input():
    """
    Placeholder for user input functionality.
    This function can be expanded to gather parameters or options from the user.
    """
    pass  # Implement user input logic here if needed


if __name__ == "__main__":
    main()