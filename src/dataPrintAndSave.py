import numpy as np
import pandas as pd

    
def print_describe(df):
    """    
    Prints overall statistics of the final dataset, specifically for Crime Count, Crime per Capita 1000, Businesses Opened,
    and Median Assessed Value.
    
    Parameters: 
        df (pd.DataFrame): The DataFrame containing the final crime data.

    Returns:
        None: This method prints the statistics directly to the console.
    """
    describe_df = df.replace([np.inf, -np.inf], np.nan)
    
    # print("describe_df columns:", describe_df.columns)
    
    describe_df = describe_df.groupby(['Year', 'Month', 'Community'], as_index=False).agg({
        'Crime Count': 'sum',
        'Crime per Capita 1000': 'first',  # these don't change within community/month
        'Businesses Opened': 'first',
        # 'Community Businesses Opened TD Total': 'first',
    })
    
    describe_df = describe_df.groupby(['Year', 'Month'], as_index=False).agg({
        'Crime Count': 'sum',
        'Crime per Capita 1000': 'mean',
        'Businesses Opened': 'sum',
        # 'Community Businesses Opened TD Total': 'sum',
    })
    
    describe_stats = describe_df[['Crime Count',
                                'Crime per Capita 1000',
                                'Businesses Opened',
                                #  'Community Businesses Opened TD Total',
                                ]].describe()
    
    assessment_stats = df.replace([np.inf, -np.inf], np.nan)
    assessment_stats = assessment_stats.groupby(['Community'], as_index=False).agg({'Median Assessed Value': 'first'})
    median_assess_describe = assessment_stats['Median Assessed Value'].describe()
    
    describe_stats_t = describe_stats.T
    
    # Add median assessment as a new row
    describe_stats_t.loc['Median Assessed Value'] = median_assess_describe
    
    # Transpose back to original format (stats as rows)
    describe_stats_final = describe_stats_t.T

    describe_stats_final['Median Assessed Value'] = describe_stats_final['Median Assessed Value'].apply(
        lambda x: f"{x:,.2f}" if pd.notna(x) else x
    )
    
    # Print final table
    print("================ Overall Stats of the dataset oganized by Months ==================" \
    "\n===================================================================================")
    print(describe_stats_final)
    print("===================================================================================")


def location_year_summary(df, location, year, location_type):
    """
    Generates a summary of crime statistics for the user specified location and year, including total population,
    median assessed value, number of businesses, total crime incidents, crime per 1000 residents, and business density per 1000 residents.
    
    Parameters:
        df (pd.DataFrame): The DataFrame containing the final dataset
        location (str): The name of the location to analyze (e.g., community name, ward number, or sector).
        year (int): The year of the data to analyze. (2018-2024)
        location_type (str): The type of location (e.g., 'Community', 'Ward', or 'Sector').
    """
    # Filter by year and location
    filtered_df = df[(df['Year'] == year) & (df[location_type] == location)]

    if filtered_df.empty:
        print(f"No data found for {location_type}: {location} in {year}.")
        return

    # Total population
    pop_vals = filtered_df['Population Household'].dropna().unique()
    total_population = int(np.mean(pop_vals)) if len(pop_vals) > 0 else 'N/A'

    # Median Assessed Value
    med_vals = filtered_df['Median Assessed Value'].dropna().unique()
    median_assessed = int(np.mean(med_vals)) if len(med_vals) > 0 else 'N/A'

    # Number of Businesses
    bis_vals = filtered_df['Community Businesses Opened TD Total'].dropna().unique()
    num_businesses = int(np.mean(bis_vals)) if len(bis_vals) > 0 else 'N/A'

    # Crime Count Total
    total_crimes = int(filtered_df['Crime Count'].sum())

    # Crime per 1000 people
    crime_per_1000 = round((total_crimes / total_population) * 1000, 2) if isinstance(total_population, int) and total_population > 0 else 'N/A'

    # Business Density
    bis_density = round((num_businesses / total_population) * 1000, 2) if isinstance(num_businesses, int) and isinstance(total_population, int) and total_population > 0 else 'N/A'

    # Output Summary
    print(f"Summary for {location_type}: {location} ({year})")
    print("-----------------------------------------------")
    print(f"Total Population: {total_population:,}" if isinstance(total_population, int) else "Total Population: N/A")
    print(f"Median Assessed Value: ${median_assessed:,}" if isinstance(median_assessed, int) else "Median Assessed Value: N/A")
    print(f"Number of Businesses: {num_businesses}" if isinstance(num_businesses, int) else "Number of Businesses: N/A")
    print(f"Total Crime Incidents: {total_crimes}")
    print(f"Crime per 1,000 residents: {crime_per_1000}")
    print(f"Business Density per 1,000 residents: {bis_density}")
