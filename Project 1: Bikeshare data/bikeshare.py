import time
import pandas as pd
import numpy as np

pd.set_option('max_columns',None)
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter the name of the city:\n').lower()
        city_list = ['chicago','new york city','washington']
        if city in city_list:
            break
        else:
            print('The city name you have entered is not vaild, please try again.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month_list = ['January','February','March','April','May','June',
                      'July','August','September','October','November',
                      'December','All']
        month = input('Please enter the month or all for all months):\n').capitalize()
        if month in month_list:
            break
        else:
            print('Error. Please try again.')
            
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the day:\n').capitalize()
        day_list = ['Saturday','Sunday','Monday','Tuesday','Wednesday',
                    'Thursday','Friday','All']
        if day in day_list:
            break
        else:
            print('Error. Please try again.')


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
    df = pd.read_csv(CITY_DATA[city])
    # delete the ID column since it is not needed
    df.pop('Unnamed: 0')
    # convert both start time and end time to date data type
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # add day column for Start Day, then add month column
    df.insert(loc = 1, column = 'Start Day',
              value = df['Start Time'].dt.day_name())
    df.insert(loc = 2, column = 'Start Month',
              value = df['Start Time'].dt.month_name())
    #add start hour column
    df.insert(loc = 3, column = 'Start Hour',
              value = df['Start Time'].dt.hour)
    # filter by month if a filter exists
    if month != 'All':
        df = df[df['Start Month'] == month]
    #filter by day if a filter exists
    if day != 'All':
        df = df[df['Start Day'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # calculate the most common month
    most_common_month = list(df['Start Month'].mode())[0]
    print('The most common month is {}.'.format(most_common_month))
    # calculate the most common day of week
    most_common_day = list(df['Start Day'].mode())[0]
    print('The most common day is {}.'.format(most_common_day))

    # calculate the most common start hour
    most_common_hour = list(df['Start Hour'].mode())[0]
    print('The most common starting hour is {}.'.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = list(df['Start Station'].mode())[0]
    print('The most commonly used start station is {}.'\
          .format(most_common_start))

    # display most commonly used end station
    most_common_end = list(df['End Station'].mode())[0]
    print('The mosty commonly used end station is {}.'\
          .format(most_common_end))
    # display most frequent combination of start station and end station trip
    # create column for most frequest combination, print the mode, then remove it
    df['Start + End'] = df['Start Station'] + ' -> ' + df['End Station']
    most_common_combination = list(df['Start + End'].mode())[0]
    print('The most frequest combination of start station and'
          'end stations is {}.'.format(most_common_combination))
    df.pop('Start + End')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time for selected data is {} seconds.'\
          .format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time for selected data is {} seconds.'\
          .format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The number of user types is {}.'.format(df['User Type'].nunique()))

    # Display counts of gender or notify user if there is no data for gender
    if 'Gender' in df:
        print('The number of genders is {}.'.format(df['Gender'].nunique()))
    else:
        print('No data found for genders.')
    # Display earliest, most recent, and most common year of birth
    # or notify user if there is no data for year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is {}.'\
              .format(int(df['Birth Year'].min())))
        print('The most recent year of birth is {}.'\
              .format(int(df['Birth Year'].max())))
        print('The most common year of birth is {}.'\
              .format(int((df['Birth Year'].mode())[0])))
    else:
        print('No data found for birth years.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # skip processing data if there is no data to avoid errors
        if df.size == 0:
            print('There is no data for the filters you have selected.')
        else:    
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            all_data_read = False
            while True:
                #break loop if all data has been read or user doesn't want to read more
                if all_data_read == True:
                    break
                # get a correct response from user whether to display 5 rows or not
                while True:
                    if all_data_read == True:
                        break
                    try:
                        answer = input(str('\nWould you like to see the first 5'
                                           ' rows of data? y/n\n'))
                        #user wants to read data
                        if answer == 'y':
                            break
                        # user doesn't want to read any data
                        elif answer == 'n':
                            all_data_read == True
                            break
                                
                    except:
                        print("Error. Please try again.")
                
                if answer == 'y':
                    start = 0
                    end = 5
                    while True:
                        print(df.iloc[start:end])
                        answer2 = input('\nPress enter if you would like to see the'
                                        ' next 5 rows. Type anything then press'
                                        ' enter to stop showing data.\n')
                        #display 5 rows if answer is yes or break out of loop otherwise
                        if answer2 == '':
                            start += 5
                            end += 5
                        else:
                            all_data_read = True
                            break
                        # don't show data if there is no more data or less than 5 rows remain
                        if end > len(df.index):
                            print("No more data to display OR less than 5 rows remaining.")
                            #show user last 5 rows if user wants to see them
                            answer3 = input('Enter y if you would like to see the last 5 rows')
                            if answer3 == 'y':
                                print(df.tail())
                            all_data_read = True
                            break
                        elif answer == 'n':
                            break
                # user doesn't want to read data
                elif answer == 'n':
                    break
                # user did not enter yes or no, restart to get a correct response
                else:
                    print('Error. Please try again.')
            
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                break
            elif restart.lower() == 'no':
                break
            else:
                print('Error. Please try again.')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
