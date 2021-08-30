import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input('\nPlease select a city to explore: chicago, new york city, washington:\n').lower()
        if city in cities:
            break
        else:
            print('\nERROR: The input and/or format you provided is invalid.')

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input('\nPlease select from the following to filter by month: january, february, march, april, may, june, all:\n').lower()
        if month in months:
            break
        else:
            print('\nERROR: The input and/or format you provided is invalid.\n')
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input('\nPlease select from the following to filter by day of the week: monday, tuesday, wednesday, thursday, friday, saturday, sunday, all\n').lower()
        if day in days:
            break
        else:
            print('\nERROR: The input and/or format you provided is invalid.\n')           

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # download relevent city data
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and time from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
       
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # Ask user if they would like to see raw data.
    row = 0
    while True:
        if row == 0:
            response = input('\nWould you like to see 5 lines of raw data? Please select yes or no:\n').lower()
            if response == 'yes':
                print(df.head())
                row = 5
            elif response == 'no':
                break
            else:
                print('\nERROR: The input and/or format you provided is invalid.\n')
        elif row > 0 and row <= len(df.index):
            response = input('\nWould you like to see 5 more lines of raw data? Please select yes or no:\n').lower()
            if response == 'yes':
                row += 5
                print(df.head(row)[-5:])
            elif response == 'no':
                break
            else:
                print('\nERROR: The input and/or format you provided is invalid.\n')                
        elif row > len(df.index):
            break
    print('-'*40)     
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('\nMost common month: ',most_common_month)
    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('\nMost common day of the week: ',most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df['start_hour'].mode()[0]
    print('\nMost common start hour: ',most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('\nMost commonly used start station: ',most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nMost commonnly used end station: ',most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    # Concatenate start and end stations, then check for mode
    df['trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['trip'].mode()[0]
    print('\nMost common trip: ',most_common_trip)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # note travel time in seconds
    total_travel = df['Trip Duration'].sum()
    print('\nTotal travel time (sec): ',total_travel)

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('\nMean travel time (sec): ',mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe types and numbers of users are listed below:\n',user_types)
    
    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of users by gender is listed below:\n',gender_count)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        print('\nThe earliest user birth year is: ',earliest_year)

        recent_year = int(df['Birth Year'].max())
        print('\nThe most recent user birth year is: ',recent_year)

        common_year = int(df['Birth Year'].mode()[0])
        print('\nThe most common user birth year is: ',common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
