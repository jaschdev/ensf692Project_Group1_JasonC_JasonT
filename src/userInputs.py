


def get_location(df):
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
