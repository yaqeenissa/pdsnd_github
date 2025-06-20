import pandas as pd
import numpy as np
import time

# Load data files
chicago_df = pd.read_csv('chicago.csv')
new_york_df = pd.read_csv('new_york_city.csv')
washington_df = pd.read_csv('washington.csv')


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('Enter city name (chicago, new york city, washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city name. Please try again.')

    while True:
        month = input('Enter month (all, january, february, ..., june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month name. Please try again.')

    while True:
        day = input('Enter day of week (all, monday, tuesday, ..., sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day. Please try again.')

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
    # Solution 1: Load data and filter by month and day using basic pandas operations
    df = pd.read_csv(CITY_DATA[city])
    df = df.drop(columns=['Unnamed: 0'], errors='ignore')


    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower() == day.lower()]

    return df

# df = load_data(city, month, day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Solution 1: Using mode for most common month, day, and hour
    most_common_month = df['month'].mode()[0]
    most_common_day_of_week = df['day_of_week'].mode()[0]
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]

    print('Most Common Month:', most_common_month)
    print('Most Common Day of Week:', most_common_day_of_week)
    print('Most Common Start Hour:', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# time_stats(df)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Solution 1: Using mode for most commonly used start and end station
    most_common_start_station = df['Start Station'].mode()[0]
    most_common_end_station = df['End Station'].mode()[0]

    print('Most Commonly Used Start Station:', most_common_start_station)
    print('Most Commonly Used End Station:', most_common_end_station)

    # Display most frequent combination of start station and end station trip
    # Solution 1: Using mode for the combination of start and end stations
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    most_common_trip = df['Trip'].mode()[0]

    print('Most Common Trip:', most_common_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# station_stats(df)


def trip_duration_stats(df: pd.DataFrame) -> None:
    """Displays statistics on the total and average trip duration.

    Args:
        df (pd.DataFrame): DataFrame containing bikeshare data with 'Trip Duration' column.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Use pandas built-in methods for sum and mean
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()

    print(f'Total Travel Time: {total_duration}')
    print(f'Mean Travel Time: {mean_duration:.2f}')

    print(f"\nThis took {time.time() - start_time:.4f} seconds.")
    print('-'*40)

# trip_duration_stats(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Solution 1: Using value_counts for user types
    user_types = df['User Type'].value_counts()
    print('User Types:\n', user_types)

    # For Gender and Birth Year statistics (if available)
    if 'Gender' in df.columns:
        # Solution 1: Using value_counts for genders
        genders = df['Gender'].value_counts()
        print('Genders:\n', genders)


    if 'Birth Year' in df.columns:
        # Solution 1: Using basic pandas methods for birth year stats
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]

        print('Earliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def display_raw_data(df):
    """Displays 5 lines of raw data at a time upon user request."""
    row_index = 0
    while True:
        show_data = input("\nWould you like to view 5 lines of raw data? (yes/no): ").strip().lower()
        if show_data == 'yes':
            if row_index >= len(df):
                print("No more raw data to display.")
                break
            print(df.iloc[row_index:row_index + 5])
            row_index += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please type 'yes' or 'no'.")

def main():
    """Main program loop with full analysis and optional raw data display."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart the analysis? (yes/no): ").strip().lower()
        if restart != 'yes':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    main()
