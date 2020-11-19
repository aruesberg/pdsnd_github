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
    print('Hello! Let\'s explore some US bikeshare data!')
    available_cities=CITY_DATA.keys()
    city=''
    while city=='':
        user_input = input('Which city would you like to select? ').lower()
        if(user_input in available_cities):
            city=user_input
        else:
            print('City ' + user_input + ' not available in data set')
                      
    available_months=['all', 'january', 'february',  'march', 'april', 'may', 'june']
    month=''
    while month=='':
        user_input = input('Which month would you like to select? ').lower()
        if(user_input in available_months):
            month=user_input
        else:
            print('Month ' + user_input + ' not available in data set')

    available_days=['all', 'monday', 'tuesday',  'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day=''
    while day=='':
        user_input = input('Which day would you like to select? ').lower()
        if(user_input in available_days):
            day=user_input
        else:
            print('Day ' + user_input + ' not available in data set')


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
    
    df = pd.read_csv(CITY_DATA.get(city))
                  
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.dayofweek


    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        df = df.loc[df['month']==month+1]

    if day != 'all':
        days = ['Monday', 'Tuesday', 'Wednesday', ' Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day.title())
        df = df.loc[df['day of week']== day]
    
    return df
    

def display_data(df):
    """Display data for selected city, month and day of week"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', -1)
    while (view_data.lower()=='yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to see the next 5 rows?: ').lower()

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Travel Time']=pd.to_datetime(df['Start Time'])
        
    print('the most common month')
    print(df['Travel Time'].dt.month.mode()[0])

    days = ['Monday', 'Tuesday', 'Wednesday', ' Thursday', 'Friday', 'Saturday', 'Sunday']
    print('the most common day of week')
    print(days[df['Travel Time'].dt.weekday.mode()[0]])


    print('the most common start hour')
    print(df['Travel Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('most commonly used start station\n')
    print(df['Start Station'].mode().iloc[0])

    print('most commonly used end station\n')
    print(df['End Station'].mode().iloc[0])


    print('most frequent combination of start station and end station trip\n')
    print(df.groupby(['Start Station','End Station']).size().sort_values(ascending=False).iloc[:1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['travel time']=pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    print('total travel time\n')
    print(df['travel time'].sum())

    print('mean travel time\n')
    print(df['travel time'].mean())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('Counts of User Type')
    print(df['User Type'].value_counts())

    print('Counts of gender')
    if 'Gender' not in df.columns:
        print('The data does not contain gender values\n')
    else: 
        print(df['Gender'].value_counts())
    
    if 'Birth Year' not in df.columns:
        print('The data does not contain birth year values\n')
    else: 
        print('earliest birth year')
        print(int(df['Birth Year'].min()))
        print('most recent birth year')
        print(int(df['Birth Year'].max()))
        print('most common year of birth')
        print(int(df['Birth Year'].mode().iloc[:1]))




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)         
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
