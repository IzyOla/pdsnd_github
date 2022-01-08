import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def read_response(usr_input, category):
    """
    Read user input and analyze
        usr_input - user's choice
        category: - category of the user's choice: 1 = City, 2 = Month, 3 = Day
    """
    while True:
        user_input = input(usr_input).title()
        try:
            if user_input in ['Chicago', 'New York City', 'Washington'] and category == 1:
                break
            elif user_input in ['January', 'February', 'March', 'April', 'May', 'June', 'All'] and category == 2:
                break
            elif user_input in ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'] and category == 3:
                break
            else:
                if category == 1:
                    print("Incorrect response - The options are 'Chicago', 'New York', or 'Washington'")
                if category == 2:
                    print("Incorrect response - The options are 'January', 'February', 'March', 'April', 'May', 'June', or 'All'")
                if category == 3:
                    print("Incorrect response - The options are 'Sunday', 'Monday' ... 'Friday', 'Saturday' or 'All'")
        except ValueError:
            print("Incorrect response recorded")
    return user_input

# get_filters function
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = read_response("Would you like to see the data for Chicago, New York City or Washington? ", 1)

    # Get user input for month (all, january, february, ... , june)
    month = read_response("Which Month (January, February, ... June, All)? ", 2)

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = read_response("Which day? (Monday, Tuesday, ... Sunday, All) ", 3)

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

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract hour, day of week, and month to different columns
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month

    # For the option 'month' where user selects 'all'. filter by month
    if month != 'All':
        # Index of months' list to obtain corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # Filter by month and create new dataframe
        df = df[df['month'] == month]

    # For the option 'day' where user selects 'all'. filter by day
    if day != 'All':
        # Filter by day of week and create new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    if (common_month == 1):
        common_month_text = "January"
    if (common_month == 2):
        common_month_text = "February"
    if (common_month == 3):
        common_month_text = "March"
    if (common_month == 4):
        common_month_text = "April"
    if (common_month == 5):
        common_month_text = "May"
    if (common_month == 6):
        common_month_text = "June"

    print('Most common month is:', common_month_text)

    # Display the most common day of week
    common_weekday = df['day_of_week'].mode()[0]
    print('Most common month is:', common_weekday)

    # Display the most common start hour
    common_start_hour = df['hour'].mode()[0]
    print('Most common month is:', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(popular_start_station))

    # Display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    df['freq_combination'] = df['Start Station'] + " " + "to" + " " + df['End Station']
    popular_combination= df['freq_combination'].mode()[0]
    print("The most frequent combination of Start and End Station is {} ".format(popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', total_travel_time)

    # Display the appropraite time unit of the total travel time in hours, minutes, and seconds format
    minute, second = divmod(total_travel_time, 60)
    # Display the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time:', mean_travel_time)

    # Display the appropraite time unit of the average travel time in hours, minutes, and seconds format
    minute, second = divmod(mean_travel_time, 60)
    # Display the duration in hour and minutes format
    hour, minute = divmod(minute, 60)
    print(f"The average trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    usertype_counts = df['User Type'].value_counts()
    print("The user types are:\n", usertype_counts)

    if city != 'Washington':
    # Display counts of gender
        print('Gender Stats:')
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
        print('Birth Year Stats:')

        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)

        most_recent_year = df['Birth Year'].max()
        print('Most Recent Year:',most_recent_year)

        most_popular_year = df['Birth Year'].mode()[0]
        print('Most Common Year:', most_popular_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city.
    Args:
        param1 (df): The chosen data frame.
    """
    while True:
        view_options = ['Yes', 'No']
        option = input("Would you like to view individual trip data (5 entries)? Type 'Yes' or 'No' \n").title()
        if option in view_options:
            if option == 'Yes':
                start_loc = 0
                end_loc = 5
                data = df.iloc[start_loc:end_loc, :9]
                print(data)
            break
        else:
            print("Please enter a valid response")
    if  option == 'Yes':
            while True:
                option_2 = input("Would you like to view more trip data? Type 'Yes' or 'No'\n").title()
                if option_2 in view_options:
                    if option_2 == 'Yes':
                        start_loc += 5
                        end_loc += 5
                        data = df.iloc[start_loc:end_loc, :9]
                        print(data)
                    else:
                        break
                else:
                    print("Please enter a valid response")



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Thank you for using this application")
            break


if __name__ == "__main__":
	main()
