import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_list = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'agust', 'september', 'october', 'november', 'december', 'all']

day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    month = ''
    day = ''
    while city not in CITY_DATA:
        city = input('Please enter the name of the city to analyze: Chicago, New York City or Washington').lower()

    while month not in month_list:
    # get user input for month (all, january, february, ... , june)
        month = input('Select a month: all or a specific month.').lower()

    while day not in day_list:
    # get user input for day of week (all, monday, tuesday, ... sunday)
        day = input('Select a day of week: all, or a specific day of the week').lower()

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
        df - pandas DataFrame containing city data filtered by month and day
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
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create a month, hour, and day of week column
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month is {}'.format(popular_month))

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of week is {}'.format(popular_day_of_week))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is {}'.format(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().argmax()
    print('The most commonly used start station is {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().argmax()
    print('The most commonly used end station is {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start-End Combo'] = df.apply(lambda x: x['Start Station'] + ' - ' + x['End Station'], axis = 1)
    popular_start_end_combo = df['Start-End Combo'].value_counts().argmax()
    print('The most frequent combination of start station and end station trip is {}'.format(popular_start_end_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('The total travel time is {} minutes.'.format(total_travel/60))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time is {} minutes.'.format(mean_travel/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are the following:')
    print(df['User Type'].value_counts())


    # Display counts of gender
    print('The counts of users by gender are the following:')
    print(df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth
    print('The earliest year of birth of any user is {}'.format(df['Birth Year'].min()))
    print('The most recent year of birth of any user is {}'.format(df['Birth Year'].max()))
    print('The most common year of birth of any user is {}'.format(df['Birth Year'].mode()[0]))

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
