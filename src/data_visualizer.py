import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def show_maps():
    """Display two PNG images side by side using matplotlib."""
    print("\nLoading images. This may take a few seconds...\n")
    file1 = "data/Calgary_Wards_and_Community_Codes_Map_2025.png"
    file2 = "data/Creb_Calgary_Community_and_Sector_Map_2025.png"
    img1 = mpimg.imread(file1)
    img2 = mpimg.imread(file2)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

    axes[0].imshow(img1)
    axes[0].set_title(f"Calgary Wards and Community Codes Map")
    axes[0].axis('off')

    axes[1].imshow(img2)
    axes[1].set_title(f"Calgary Community and Sectors Map")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show(block = False)

def plot_crime_category(final_df, location, year, location_type):
    # Create 2 subplots for Figure 1
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 9))

    # ----- PLOT 1.1: TOTAL CRIME COUNT PER CATEGORY FOR SPECIFIED COMMUNITY AND YEAR -----
    subset = final_df[(final_df[location_type] == location) & (final_df['Year'] == year)]
    crime_by_category = subset.groupby('Category')['Crime Count'].sum().reset_index()
    crime_by_category = crime_by_category.sort_values(by='Crime Count', ascending=False)

    axes[0].bar(crime_by_category['Category'], crime_by_category['Crime Count'])
    axes[0].set_title(f'Total Crime by Category in {location} ({year})')
    axes[0].set_xlabel('Crime Category')
    axes[0].set_ylabel('Total Crime Count')
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis='y')

     # ----- PLOT 1.2: LINE PLOT TOTAL CRIME COUNT PER YEAR ALL CATEGORIES -----
    total_crime_category = final_df.groupby(['Category', 'Year'])['Crime Count'].sum().reset_index()
    pivot_table_year = total_crime_category.pivot(index='Year', columns='Category', values='Crime Count')

    pivot_table_year.plot(ax=axes[1], marker='o')
    axes[1].set_title('Total Crime Count Per Year (For all of Calgary)')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Total Crime Count')
    axes[1].grid(True)
    axes[1].legend(title='Crime Category', bbox_to_anchor=(1, 1), loc='upper left')

    # Layout fix
    plt.tight_layout()
    plt.show()

    # crime_category_month = final_df.groupby(['Category', 'Year', 'Month'])['Crime Count'].sum().reset_index()
    # pivot_table_month = total_crime_category.pivot(index='Month', columns='Category', values='Crime Count')
    # print(pivot_table_month)

def plot_crime_count(final_df, location, year, location_type):
    # ----- PLOT 2.1: TOTAL CRIME COUNT PER MONTH -----

    # Create 2 subplots for Figure 2
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 9))  

    # Filter data frame
    subset = final_df[(final_df[location_type] == location) & (final_df['Year'] == year)]

    # Group by Month and sum Crime Count
    monthly_crime = subset.groupby('Month')['Crime Count'].sum().reset_index()
    monthly_crime = monthly_crime.sort_values(by='Month')

    # Plot on first subplot
    axes[0].bar(monthly_crime['Month'], monthly_crime['Crime Count'])
    axes[0].set_title(f'Total Crime Count per Month in {location} ({year})')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Total Crime Count')
    axes[0].set_xticks(range(1, 13))
    axes[0].grid(axis='y')

    # ----- PLOT 2.2: CRIME TREND BY MONTH ACROSS YEARS -----

    # Group by Year and Month, then sum Crime Count
    crime_month = final_df.groupby(['Year', 'Month'])['Crime Count'].sum().reset_index()

    # Pivot table so rows = Month, columns = Year
    pivot_table = crime_month.pivot(index='Month', columns='Year', values='Crime Count')
    pivot_table = pivot_table.replace(0, np.nan).dropna(axis=1, how='all')

    # Plot on second subplot
    pivot_table.plot(kind='line', marker='o', ax=axes[1])

    axes[1].set_title('Total Crime Per Month by Year')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Total Crime Count')
    axes[1].set_xticks(range(1, 13))
    axes[1].grid(True)
    axes[1].legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Plot
    plt.tight_layout()
    plt.show()

def plot_cc_vs_mdv(final_df, location, year, location_type):
    # ----- PLOT 3: MEDIAN ASSESSED VALUES VERSUS CRIME PER CAPITA -----

    # Filter data for the selected year
    filtered_df = final_df[final_df['Year'] == year]

    # Group by Community
    agg_dict = {
        'Community Code': 'first',
        'Median Assessed Value': 'first',
        'Crime per Capita 1000': 'first',
    }

    if location_type not in ['Community']:
        agg_dict[location_type] = 'first'

    scatter_df = filtered_df.groupby(['Community']).agg(agg_dict).reset_index()

    # Scatter plot, plotting all communities
    plt.figure(figsize=(10, 6))
    plt.scatter(scatter_df['Median Assessed Value'],
                scatter_df['Crime per Capita 1000'],
                alpha=0.5, label='Other Communities')

    # Highlight the specified community
    highlight = scatter_df[scatter_df[location_type] == location]
    if not highlight.empty:
        plt.scatter(highlight['Median Assessed Value'], 
                    highlight['Crime per Capita 1000'],
                    color='red', s=100, label=f"{location_type}: {location}",
                    edgecolor='black')
        for _, row in highlight.iterrows():
            plt.text(row['Median Assessed Value'],
                     row['Crime per Capita 1000'] + 0.2,
                     row['Community Code'],
                     fontsize=10, ha='center', color='red')

    # --- Plot labels ---
    plt.title(f'Median Assessed Value vs. Crime per Capita by Community ({year})')
    plt.xlabel('Community Median Assessed Value ($)')
    plt.ylabel('Crime per Capita 1000')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_cc_vs_bc(final_df, location, year, location_type):
    # ----- PLOT 4: TOTAL CRIME COUNT VERSUS TOTAL BUSINESS COUNT ----- 

    # filter to a specific year
    filtered_df = final_df[final_df['Year'] == year]

    # Group by Community
    agg_dict = {
        'Community Code': 'first',
        'Community Businesses Opened TD Total': 'first',
        'Crime Count': 'sum'
    }

    # Only add location_type if it is not the groupby column to avoid conflict
    if location_type not in ['Community']:
        agg_dict[location_type] = 'first'

    scatter_df = filtered_df.groupby(['Community']).agg(agg_dict).reset_index()

    # Create the scatter plot
    plt.figure(figsize=(10, 6))

    # Plot all communities
    plt.scatter(scatter_df['Community Businesses Opened TD Total'],
                scatter_df['Crime Count'],
                alpha=0.5, label='Other Communities')
    # Highlight the selected community
    highlight = scatter_df[scatter_df[location_type] == location]
    if not highlight.empty:
        plt.scatter(highlight['Community Businesses Opened TD Total'],
                    highlight['Crime Count'],
                    color='red', s=100, edgecolor='black', label=f"{location_type}: {location}")

        # Add labels (community codes)
        for _, row in highlight.iterrows():
            plt.text(row['Community Businesses Opened TD Total'],
                     row['Crime Count'] + 100,
                     row['Community Code'],
                     fontsize=9, ha='center', color='red')

    # Add plot details
    plt.title(f'Total Crime Count vs. Business Count by Communities ({year})')
    plt.xlabel(f'Community Businesses Opened TD Total')
    plt.ylabel('Total Crime Count')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# def get_plots(final_df, community_code, year):
    # """
    # Generates and displays various plots based on the final DataFrame.

    # Args:
    #     final_df (DataFrame): The final DataFrame containing the cleaned and merged data.
    # """
    # # Create 2 subplots for Figure 1
    # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 9))

    # # ----- PLOT 1.1: TOTAL CRIME COUNT PER CATEGORY FOR SPECIFIED COMMUNITY AND YEAR -----
    # subset = final_df[(final_df['Community Code'] == community_code) & (final_df['Year'] == year)]
    # crime_by_category = subset.groupby('Category')['Crime Count'].sum().reset_index()
    # crime_by_category = crime_by_category.sort_values(by='Crime Count', ascending=False)

    # axes[0].bar(crime_by_category['Category'], crime_by_category['Crime Count'])
    # axes[0].set_title(f'Total Crime by Category in {community_code} ({year})')
    # axes[0].set_xlabel('Crime Category')
    # axes[0].set_ylabel('Total Crime Count')
    # axes[0].tick_params(axis='x', rotation=45)
    # axes[0].grid(axis='y')

    # # ----- PLOT 1.2: LINE PLOT TOTAL CRIME COUNT PER YEAR ALL CATEGORIES -----
    # total_crime_category = final_df.groupby(['Category', 'Year'])['Crime Count'].sum().reset_index()
    # pivot_table = total_crime_category.pivot(index='Year', columns='Category', values='Crime Count')

    # pivot_table.plot(ax=axes[1], marker='o')
    # axes[1].set_title('Total Crime Count Per Year (All Communities)')
    # axes[1].set_xlabel('Year')
    # axes[1].set_ylabel('Total Crime Count')
    # axes[1].grid(True)
    # axes[1].legend(title='Crime Category', bbox_to_anchor=(1, 1), loc='upper left')

    # # Layout fix
    # plt.tight_layout()
    # plt.show()


    # # ----- PLOT 2.1: TOTAL CRIME COUNT PER MONTH -----

    # # Create 2 subplots for Figure 2
    # fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 9))  

    # # Filter data frame
    # subset = final_df[(final_df['Community Code'] == community_code) & (final_df['Year'] == year)]

    # # Group by Month and sum Crime Count
    # monthly_crime = subset.groupby('Month')['Crime Count'].sum().reset_index()
    # monthly_crime = monthly_crime.sort_values(by='Month')

    # # Plot on first subplot
    # axes[0].bar(monthly_crime['Month'], monthly_crime['Crime Count'])
    # axes[0].set_title(f'Total Crime Count per Month in {community_code} ({year})')
    # axes[0].set_xlabel('Month')
    # axes[0].set_ylabel('Total Crime Count')
    # axes[0].set_xticks(range(1, 13))
    # axes[0].grid(axis='y')

    # # ----- PLOT 2.2: CRIME TREND BY MONTH ACROSS YEARS -----

    # # Group by Year and Month, then sum Crime Count
    # crime_month = final_df.groupby(['Year', 'Month'])['Crime Count'].sum().reset_index()

    # # Pivot table so rows = Month, columns = Year
    # pivot_table = crime_month.pivot(index='Month', columns='Year', values='Crime Count')
    # pivot_table = pivot_table.replace(0, np.nan).dropna(axis=1, how='all')

    # # Plot on second subplot
    # pivot_table.plot(kind='line', marker='o', ax=axes[1])

    # axes[1].set_title('Total Crime Per Month by Year')
    # axes[1].set_xlabel('Month')
    # axes[1].set_ylabel('Total Crime Count')
    # axes[1].set_xticks(range(1, 13))
    # axes[1].grid(True)
    # axes[1].legend(title='Year', bbox_to_anchor=(1.05, 1), loc='upper left')

    # # Plot
    # plt.tight_layout()
    # plt.show()

    # # ----- PLOT 3: MEDIAN ASSESSED VALUES VERSUS CRIME PER CAPITA -----

    # # Filter data for the selected year
    # filtered_df = final_df[final_df['Year'] == year]

    # # Group by Community: take average values
    # scatter_df = filtered_df.groupby('Community Code').agg({
    #     'Median Assessed Value': 'mean',
    #     'Crime per Capita 1000': 'mean'
    # }).reset_index()

    # # Scatter plot
    # plt.figure(figsize=(10, 6))

    # # Plot all communities
    # plt.scatter(scatter_df['Median Assessed Value'], scatter_df['Crime per Capita 1000'], alpha=0.6, label='Other Communities')

    # # Highlight the specified community
    # highlight = scatter_df[scatter_df['Community Code'] == community_code]
    # if not highlight.empty:
    #     plt.scatter(highlight['Median Assessed Value'], highlight['Crime per Capita 1000'],
    #                 color='red', s=100, label=community_code, edgecolor='black')
    #     plt.text(highlight['Median Assessed Value'].values[0],
    #             highlight['Crime per Capita 1000'].values[0] + 1,
    #             community_code,
    #             fontsize=10, ha='center', color='red')

    # # --- Plot labels ---
    # plt.title(f'Median Assessed Value vs. Crime per Capita by Community ({year})')
    # plt.xlabel('Median Assessed Value ($)')
    # plt.ylabel('Crime per Capita 1000')
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    
    # # ----- PLOT 4: TOTAL CRIME COUNT VERSUS TOTAL BUSINESS COUNT ----- 

    # # Optional: filter to a specific year
    # # year = 2022
    # # filtered_df = final_df[final_df['Year'] == year]
    # # Otherwise, use full dataset
    # filtered_df = final_df

    # # Group by community
    # scatter_df = filtered_df.groupby('Community Code').agg({
    #     'Community Businesses Opened TD Total': 'mean', 
    #     'Crime Count': 'sum'
    # }).reset_index()

    # # Create the scatter plot
    # plt.figure(figsize=(10, 6))

    # # Plot all communities
    # plt.scatter(scatter_df['Community Businesses Opened TD Total'], scatter_df['Crime Count'], alpha=0.6, label='Other Communities')

    # # Highlight the selected community
    # highlight = scatter_df[scatter_df['Community Code'] == community_code]
    # if not highlight.empty:
    #     plt.scatter(highlight['Community Businesses Opened TD Total'], highlight['Crime Count'],
    #                 color='red', s=100, edgecolor='black', label=community_code)
    #     plt.text(highlight['Community Businesses Opened TD Total'].values[0],
    #             highlight['Crime Count'].values[0] + 200,  # adjust offset as needed
    #             community_code,
    #             fontsize=10, ha='center', color='red')

    # # Add plot details
    # plt.title('Total Crime Count vs. Community Businesses Opened TD Total')
    # plt.xlabel('Community Businesses Opened TD Total')
    # plt.ylabel('Total Crime Count')
    # plt.grid(True)
    # plt.legend()
    # plt.tight_layout()
    # plt.show()
    

    # # Create a single figure with 3 subplots (3 rows, 1 column)
    # fig, axes = plt.subplots(3, 1, figsize=(10, 18))  # Adjust height for spacing

    # # ---------------- Plot 1: Total Crime Count Per Year by Crime Category ----------------
    # # Group by Category and Year, then sum Crime Count
    # plot1_df = final_df.groupby(['Category', 'Year'])['Crime Count'].sum().reset_index()
    # # Create a pivot table where rows = Year, columns = Category, values = total crime count
    # plot1_pt = plot1_df.pivot(index='Year', columns='Category', values='Crime Count')
    # # Plot each category's crime trend across years
    # plot1_pt.plot(kind='line', marker='o', ax=axes[0])
    # axes[0].set_title('Total Crime Count Per Year')
    # axes[0].set_xlabel('Year')
    # axes[0].set_ylabel('Total Crime Count')
    # axes[0].grid(True)
    # axes[0].legend(title='Crime Category', fontsize='small', loc='upper left')

    # # ---------------- Plot 2: Total Crime Per Month by Year ----------------
    # # Group by Year and Month, then sum Crime Count
    # plot2_df = final_df.groupby(['Year', 'Month'])['Crime Count'].sum().reset_index()
    # # Create a pivot table where rows = Month, columns = Year, values = total crime count
    # plot2_pt = plot2_df.pivot(index='Month', columns='Year', values='Crime Count')
    # # Replace all 0s with NaN and drop years (columns) where all values are NaN
    # plot2_pt = plot2_pt.replace(0, np.nan).dropna(axis=1, how='all')
    # # Plot total crime per month for each year
    # plot2_pt.plot(kind='line', marker='o', ax=axes[1])
    # axes[1].set_title('Total Crime Per Month by Year')
    # axes[1].set_xlabel('Month')
    # axes[1].set_ylabel('Total Crime Count')
    # axes[1].set_xticks(range(1, 13))
    # axes[1].grid(True)
    # axes[1].legend(title='Year', fontsize='small', loc='upper left')

    # # ---------------- Plot 3: Year-over-Year % Change in Total Crime ----------------
    # # Group by Year and get Total of Crime Count
    # plot3_df = final_df.groupby('Year')['Crime Count'].sum().sort_index()
    # # Remove years with 0 or NaN crime count
    # plot3_df = plot3_df[plot3_df > 0]
    # # Compute percent change
    # plot3_pct_change = plot3_df.pct_change() * 100
    # plot3_pct_change.dropna().plot(kind='bar', ax=axes[2], color='coral')
    # axes[2].set_title('YoY % Change in Total Crime')
    # axes[2].set_xlabel('Year')
    # axes[2].set_ylabel('Percent Change (%)')
    # axes[2].axhline(0, color='gray', linestyle='--')
    # axes[2].grid(axis='y')

    # # ---------------- Layout adjustment ----------------
    # plt.tight_layout()
    # plt.show()