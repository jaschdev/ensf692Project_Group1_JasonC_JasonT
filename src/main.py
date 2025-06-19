"""
main.py

Authors: Jason Chiu and Jason Tieh

Entry point of the ENSF 692 Spring 2025 final project.

This script coordinates the overall program execution, including loading data,
getting user input, performing analysis, and exporting results.

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from dataLoader import create_dataframe
from userInputs import get_location, get_year
from dataPrintAndSave import print_describe, location_year_summary
from dataVisualizer import show_maps, plot_crime_category, plot_crime_count, plot_cc_vs_mdv, plot_cc_vs_bc

def main():     

    # Load data from CSV files and perform initial cleaning    
    df = create_dataframe()       
    # print(df.head())

    print(" --------- Start Crime Statistics Visualizer ---------")
    print("\nWelcome to Calgary Crime Statistic Visualizer!\n" \
    "\nIn this program, you will be able to view Calgary's basic crime statistics from the years 2018 to 2024" \
    "\nSelect a year and location/region within Calgary, and you will see data related to the input, including: " \
    "\ntype and quantity of crime, crime per month, crime per capita 1000 vs median assessed value of the region," \
    "\nand crime count vs the number of existing businesses of the region.")

    print("Based On current entire existing dataset, the following values have also been observed:")

    print_describe(df)

    print("\n\nTo begin the visualizer, first select the region type.")

    while True:
        map = input("If you would like a map to see what sectors, wards, and communities you may see the map png files " \
        "\nfound in the /data folder or if you wish to see the images from here, enter 'Y' (Note: this process is slow)" \
        "\nor hit 'ENTER' to skip: ")
        if (map == 'Y'):
            show_maps()

        location_type, location = get_location(df)
        year = get_year(df)

        print("\nYou have chosen the following region and year | ", location_type, ": ", location, " for the year ", year)

        print("\nBased on these chosen fields, the following statistics can be seen:\n")
        
        location_year_summary(df, location, year, location_type)

        print("\nHere is a plot showing the crime category and their total count for the chosen year and location:\n")
        plot_crime_category(df, location, year, location_type)

        print("Here is a plot comparing the amount of crime per month for the chosen year and location:\n")
        plot_crime_count(df, location, year, location_type)

        print("Here is a plot comparing Crime per capita 1000 vs a locations communities, median assessed value:\n")
        plot_cc_vs_mdv(df, location, year, location_type)

        print("Here is a plot comparing Crime Count vs a locations communities business count to date total:\n")
        plot_cc_vs_bc(df, location, year, location_type)

        final = input("Would you like to visualize data for another location and/or time? If not, enter 'Q' to quit: ")
        if(final == 'Q' or final == 'q'):
            # print("Final data frame will now be saved in the /data folder.")
            # base_dir = os.path.dirname(os.path.dirname(__file__))
            # data_dir = os.path.join(base_dir, "data")
            # export_path = os.path.join(data_dir, "final_exported_dataset.xlsx")

            # # df = df.set_index(['Community Code', 'Year', 'Month'])
            # df.to_excel(export_path, index=False)
            # print(f"Final dataset exported to {export_path}")
            break

    print("Thank you for Using the Calgary Crime Statistics Visualizer.")
    print("-----------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()