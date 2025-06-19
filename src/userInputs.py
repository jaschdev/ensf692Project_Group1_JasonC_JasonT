class UserInputs:
    """
    A class to handle user inputs for analyzing crime statistics in Calgary. This class provides methods to get the type of location (Sector, Ward, or Community),

    Methods:
        get_location(df): Prompts the user to select a location type and returns the corresponding location and type.
        get_community(df): Prompts the user to enter a community name or code and returns the community.
        get_year(df): Prompts the user to enter a year and returns the year.
        get_ward(df): Prompts the user to enter a ward number and returns the ward number.
        get_sector(df): Prompts the user to enter a sector name and returns the sector name.
    """

    def get_location(df):
        """
        Prompts the user to select a location type (Sector, Ward, or Community) and redirects the user to another method to get the Sector, Ward, or Community.
        Parameters:
            df (pd.DataFrame): The DataFrame containing the crime statistics data.
            """
        print("Data can be analyzed in either City Sectors, City Wards, or City Communities.")
        while True:
            location_in = input("Type 'Sector' 'Ward' or 'Community' for the type of location you wish to analyze data on: ")
            location = location_in.strip().upper()
            try:
                if (location == 'SECTOR'):
                    return 'Sector', get_sector(df)
                elif (location == 'WARD'):
                    return 'Ward Number', get_ward(df)
                elif (location == 'COMMUNITY'):
                    return get_community(df)
                else:
                    raise KeyError("\n" + location_in + ' is not a valid location. Please try again.\n')
            except KeyError as e:
                print(e.args[0])

    def get_community(df):
        """
        Prompts the user to enter a community name or code available in the dataset and returns the community.
        Parameters:
            df (pd.DataFrame): The DataFrame containing the crime statistics data.
        """
        while True:
            # formating input to be case insensitive and ignore spaces at beginnig and end
            community = input("Please enter a community by name or 3 character code to analyze data on: ").strip().upper()
            # ensure dataframe of breed column only has upper case names
            df['Community Code'] = df['Community Code'].str.upper()
            df['Community'] = df['Community'].str.upper()
            try:
                if (community not in df['Community Code'].values) and (community not in df['Community'].values):
                    raise KeyError('\nThis community was not found in the data. Please try again.\n')
                if community in df['Community Code'].values:
                    return 'Community', df.loc[df['Community Code'] == community, 'Community'].iloc[0]
                elif  community in df['Community'].values:
                    return 'Community', df.loc[df['Community'] == community, 'Community'].iloc[0]
            except KeyError as e:
                print(e.args[0])

    def get_year(df):
        """
        Prompts the user to enter a year available in the dataset and returns the year.
        Parameters:
            df (pd.DataFrame): The DataFrame containing the crime statistics data.
        """
        while True:
            # formating input to be case insensitive and ignore spaces at beginnig and end
            year = input("Please enter the year of data to analyze: ")
            # ensure dataframe of breed column only has upper case names
            try:
                if (year not in df['Year'].values):
                    raise KeyError('\nThis year was not found in the data. Please try again.\n')
                if year in df['Year'].values:
                    return df.loc[df['Year'] == year, 'Year'].iloc[0]
                elif year == 'Q':
                    return year
            except KeyError as e:
                print(e.args[0])

    def get_ward(df):
        """
        Prompts the user to enter a ward number available in the dataset and returns the ward number.
        Parameters:
            df (pd.DataFrame): The DataFrame containing the crime statistics data.
        """
        while True:
            # formating input to be case insensitive and ignore spaces at beginnig and end
            ward = input("Please enter the city ward to analyze data on (i.e. 1-14): ")
            # ensure dataframe of breed column only has upper case names
            try:
                if (ward not in df['Ward Number'].values):
                    raise KeyError('\nThis city ward was not found in the data. Please try again.\n')
                if ward in df['Ward Number'].values:
                    return df.loc[df['Ward Number'] == ward, 'Ward Number'].iloc[0]
                elif ward == 'Q':
                    return ward
            except KeyError as e:
                print(e.args[0])

    def get_sector(df):
        """
        Prompts the user to enter a sector name available in the dataset and returns the sector name.
        Parameters:
            df (pd.DataFrame): The DataFrame containing the crime statistics data.
        """
        while True:
            # formating input to be case insensitive and ignore spaces at beginnig and end
            sector = input("Please enter the city sector to analyze data on: ").strip().upper().replace(" ", "")
            # ensure dataframe of breed column only has upper case names
            df['Sector'] = df['Sector'].str.upper()
            try:
                if sector in df['Sector'].values:
                    return df.loc[df['Sector'] == sector, 'Sector'].iloc[0]
                elif sector == 'CITYCENTRE':
                    return 'CENTRE'
                elif (sector not in df['Sector'].values):
                    raise KeyError('\nThis city sector was not found in the data. Please try again.\n')
            except KeyError as e:
                print(e.args[0])
