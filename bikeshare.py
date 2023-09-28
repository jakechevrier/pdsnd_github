import time
import calendar
import sys
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
    print('\n\n*********************************************')
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    
    
    
    
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None    
    while city not in CITY_DATA:
        city = input("Enter a city to explore (Chicago, New York City, Washington) or exit to end:  ").strip()
        if city == 'exit':
            print('Ending Program...\n')
            sys.exit()
        
        try:
            if city in CITY_DATA:
                print(city.title()+' will be used to filter data.\n')
            if city not in CITY_DATA:
                print("Unsupported input. Please only enter a city name from the list given.\n")
        except ValueError:
            print("Unsupported input. Please only enter a city name from the list given.\n")

            

            
            
            

    # TO DO: get user input for month (all, january, february, ... , june)
    months = [i for i in range(1, 13)]
    month_int = None
    
    while month_int not in months:
        month_int = input('Enter an integer for the month to filter by (0: no filtering, 1: Jan, 2: Feb, etc.), or exit to end:  ')

        if month_int == 'exit':
            print('Ending Program...\n')
            sys.exit()
        
        try:
            month_int = int(month_int)

            if month_int == 0:
                month = 'all'
                print('No month filteriing will be used.\n')
                break    
            if month_int not in months:
                print("Unsupported input. Please only enter the integer of the chosen month (1-12) or 0 for no filtering.\n")
            if month_int in months:
                month = month_int
                print(calendar.month_name[month_int]+' will be used to filter data.\n')

                
        except ValueError:
            print("Unsupported input. Please only enter the integer of the chosen month (1-12) or 0 for no filtering.\n")
    
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = list(calendar.day_name)
    days.insert(0, days.pop())
    
    day_indices = [i for i in range(1, 8)]
    
    day_int = None
    while day_int not in day_indices:
        day_int = input('Enter an integer for the day of the week to filter by (0: no filtering, 1: Sun, 2: Mon, etc.), or exit to end:  ')

        if day_int == 'exit':
            print('Ending Program...\n')
            sys.exit()

        try:
            day_int = int(day_int)

            if day_int == 0:
                day = 'all'
                print('No day filteriing will be used.\n')
                break
            if day_int not in day_indices:
                print("Unsupported input. Please only enter the integer of the chosen day (1-7) or 0 for no filtering.\n")
            if day_int in day_indices:
                day = day_int-1
                print(days[day_int-1]+' will be used to filter data.\n')

    
        except ValueError:
            print("Unsupported input. Please only enter the integer of the chosen day (1-7) or 0 for no filtering.\n")
    

    #print('-'*40)
    #return city, month, day
    #day = 1
    return(city,month,day)


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
    print('Loading '+city.title()+' data...')
    
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['DayOfWeek'] = (df['Start Time'].dt.weekday  + 1) % 7
    
    if month != 'all':
        df = df[df['Start Time'].dt.month == month]
    if day != 'all':
        df = df[df['DayOfWeek'] == day]

    print('\nFound ', len(df), 'data points...')
    print(df.head())


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_month = df['Start Time'].dt.month.value_counts().idxmax()
    most_month_name = calendar.month_name[most_month]
    print('- The most common month is: ',most_month_name)
          
    
    # TO DO: display the most common day of week
    most_day = df['Start Time'].dt.weekday.value_counts().idxmax()
    print('- The most common day is: ',calendar.day_name[most_day])

    # TO DO: display the most common start hour
    most_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('- The most common hour is: ',most_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start_station = df['Start Station'].value_counts().idxmax()
    print('- The most common start station is: ',most_start_station)

    # TO DO: display most commonly used end station
    most_end_station = df['End Station'].value_counts().idxmax()
    print('- The most common end station is: ',most_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['combined_station'] = df['Start Station'] + ' - ' + df['End Station']
    most_combined_station = df['combined_station'].value_counts().idxmax()
    print('- The most common station combination is: ',most_combined_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    hours,remainder = divmod(sum(df['Trip Duration']),3600)
    minutes,seconds = divmod(remainder,60)
    print('- The total trip duration is: ',"{:,.0f}".format(hours),'hours ',"{:,.0f}".format(minutes),'minutes ',"{:,.0f}".format(seconds),'seconds')

    # TO DO: display mean travel time
    mean_travel = df['Trip Duration'].mean()
    hours,remainder = divmod(mean_travel,3600)
    minutes,seconds = divmod(remainder,60)    
    
    print('- The mean trip duration is: ',"{:,.0f}".format(hours),'hours ',"{:,.0f}".format(minutes),'minutes ',"{:,.0f}".format(seconds),'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    for user_type, count in user_types.items():
        print('-',user_type,': ',count)

    # TO DO: Display counts of gender
    try:
        print('\n')
        genders = df['Gender'].value_counts()
        for gender, count in genders.items():
            print('-',gender,': ',count)
    except:
        pass

        
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        print('\n')
        bday_min = int(min(df['Birth Year']))
        bday_max = int(max(df['Birth Year']))
        bday_mostcommon = int(df['Birth Year'].value_counts().idxmax())
        print('- The earliest year of birth is: ',bday_min)
        print('- The most recent year of birth is: ',bday_max)
        print('- The most common year of birth is: ',bday_mostcommon)
    except:
        pass


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    df = df.drop('combined_station', axis=1)
    show_raw_data = input("Do you want to show 5 rows of raw data? (yes/no)").lower()
    i = 0
    pd.set_option('display.max_columns', 200)
    
    while True:   
        if show_raw_data == "no":
            break
        if show_raw_data == "yes":
            
            print(df[i:i+5])
            i += 5
            if i <= len(df):
                show_raw_data = input("\nDo you want to show 5 more rows of raw data? (yes/no)").lower()
            else:
                print("End of data.")
                show_raw_data = 'no'
        else:
            show_raw_data = input("Your input was invalid... Do you want to show 5 rows of raw data? (yes/no)").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        try:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data(df)
        except ValueError:
            print('\nThere is no data within that filtering. Please try again with a different filtering criteria.')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()