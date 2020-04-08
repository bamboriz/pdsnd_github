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
    print('Hello! Let\'s explore some US bikeshare data !')

    month = 'all'
    day = 'all'

    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    while True:
        try:
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            city = input('Would you like to see data for Chicago, New York, or Washington? : ')

            filt = input('Would you like to filter the data by month, day, or not at all? Type "none" for no filter : ')
            filt = filt.lower()

            if filt == 'both':
                # get user input for month (all, january, february, ... , june)
                month = input('What month would you like to see ? January, February, ... , June : ')
                # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input('What day would you like to see ? :')

            if filt == 'month':
                # get user input for month (all, january, february, ... , june)
                month = input('What month would you like to see ? January, February, ... , June : ')
            
            if filt == 'day':
               # get user input for day of week (all, monday, tuesday, ... sunday)
                day = input('What day would you like to see ? : ')

        finally:
            city = city.strip().lower()
            month = month.strip().lower()
            day = day.strip().lower()

        if city in cities:
            print('-'*40)
            break
        else:
            print('Invalid input, please let\'s start again !\n')
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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']

    # display the most common month
    print('Most common month: ', months[df['month'].mode()[0] - 1].title())

    # display the most common day of week
    print('Most common day of week: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most common start hour: {}:00'.format(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most used Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most used End Station: ', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    st_end = df['Start Station'] + '|' + df['End Station']
    most_popular_combination = st_end.mode()[0]
    start_station = most_popular_combination.split('|')[0]
    end_station = most_popular_combination.split('|')[1]
    print('Most used frequent combination of start station and end station: {} -> {}'.format(start_station, end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean travel time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts() 
    print('Subscribers: ', user_types['Subscriber'])
    print('Customers: ', user_types['Customer'])

    if city != 'washington':
        # Display counts of gender
        gender_types = df['Gender'].value_counts() 
        print('Male: ', gender_types['Male'])
        print('Female: ', gender_types['Female'])

        # Display earliest, most recent, and most common year of birth
        print('Most common year of birth : ', df['Birth Year'].mode()[0])
        print('Earliest year of birth : ', df['Birth Year'].min())
        print('Most recent year of birth : ', df['Birth Year'].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def continue_prompt():
    raw = input('\nWould you like to see raw data? Enter yes or no.\n')
    return raw.title()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw = continue_prompt()
        if raw != 'yes':
            break
        else:
            count = 5
            while raw == 'yes':
                print(df.head(count).tail())
                count += 5
                raw = continue_prompt()
               
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
