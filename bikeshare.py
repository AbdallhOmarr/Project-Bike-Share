#This is a program to interact with user and calculating specfiic data for them 

#importing pd
from os import replace
import time
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

from numpy.lib.npyio import load
from pandas.io.pytables import incompatibility_doc 
import calendar
#I will first make a class named data and then create objects for each city 
#then i will create a method for calculating the required data and for filitering data

class data():
    """ represent the data of each city """ 
    #initiating city instance variable for class 
    def __init__(self,city,month_value=None,day_value=None):
        self.city = city
        self.month_value = month_value
        self.day_value = day_value

    
    #method to load dataframe from csv
    def load_city(self):
        self.city_data = pd.read_csv("./"+self.city+".csv")
        

 

    #method to add month and day column
    def column(self):
        #converting Start Time column to a datetime object first
        self.city_data['Start Time']= pd.to_datetime(self.city_data['Start Time'])

        #making month column
        self.city_data['month']= self.city_data['Start Time'].dt.month
        #the next code i searched for internet on how to convert month number to name but i didn't understand lambda fully
        #i tried to use calendar lib without lambda but it didn't take a series arg 
        self.city_data['month']= self.city_data['month'].apply(lambda x: calendar.month_name[x])

        #making day column 
        self.city_data['day']= self.city_data['Start Time'].dt.day_name()

        #making hour column 
        self.city_data['hour'] = self.city_data['Start Time'].dt.hour

    def filter_data(self):
        self.column()
        #print('This is filtering method')
        if self.month_value != None and self.day_value != None:
            #print('Filtering by month and day')
            self.city_data_filtered = self.city_data[self.city_data['month']==self.month_value]
            self.city_data_filtered = self.city_data_filtered[self.city_data_filtered['day']==self.day_value]

        elif self.month_value != None:
            #print("Filtering by month only")
            self.city_data_filtered = self.city_data[self.city_data['month']==self.month_value]

        elif self.day_value !=None:
            #print("Filtering by day only")
            self.city_data_filtered = self.city_data[self.city_data['day']==self.day_value]

        elif self.month_value == None and self.day_value == None:
            self.city_data_filtered = self.city_data
        
        return self.city_data_filtered

    #view head of the data
    def view_data(self):
        print(self.city_data_filtered.head())
    


                                #''' Statistics to be calculated '''
    def most_pop_travel_times(self):
        print("_____________________________________________Popular Travel Times______________________________________________\n")
        start_time = time.time()
        self.most_common_month = self.city_data_filtered['month'].mode()[0]
        self.most_common_day = self.city_data_filtered['day'].mode()[0]
        self.most_common_hour = self.city_data_filtered['hour'].mode()[0]
        print("Most common Month: "+self.most_common_month+"\n"+"Most common day: "+self.most_common_day)
        print("Most Common Hour: {}".format(self.most_common_hour))
        print("Calculated in {} Seconds\n".format(time.time()-start_time))
    def most_pop_stations(self):
        print("_______________________________________________Popular Stations________________________________________________\n")
        start_time = time.time()
        #most common start station
        self.most_common_start_station = self.city_data_filtered.loc[:,'Start Station'].mode()[0]
        #most common end station
        self.most_common_end_station = self.city_data_filtered.loc[:,'End Station'].mode()[0]

        #most common combination between start and end stations
        # 
        lst = "From " + self.city_data_filtered.loc[:,'Start Station'] +" to "+ self.city_data_filtered.loc[:,'End Station'] 
        self.city_data_filtered['Combination Start and End'] = lst
        print("Most common Start Station: "+self.most_common_start_station)
        print("Most common End Station: "+self.most_common_end_station)
        print("Most common Trip: "+self.city_data_filtered['Combination Start and End'].mode()[0])
        print("Calculated in {} Seconds\n".format(time.time()-start_time))


    def trip_statistics(self):
        print("________________________________________________Trip Statistics________________________________________________\n")
        start_time = time.time()
        self.total_travel_time= self.city_data_filtered['Trip Duration'].sum()
        self.average_travel_time = self.city_data_filtered['Trip Duration'].mean()
        print("Total travel time: {} Second".format(self.total_travel_time))
        print("Average travel time: {} Second\n".format(self.average_travel_time))
        print("Calculated in {} Seconds".format(time.time()-start_time))

    def user_info(self):
        print("___________________________________________________User Info___________________________________________________\n")
        start_time=time.time()
        self.Customer_count = self.city_data_filtered['User Type'][self.city_data_filtered['User Type'] == 'Customer'].count()
        self.Subscriber_count = self.city_data_filtered['User Type'][self.city_data_filtered['User Type'] == 'Subscriber'].count()
        print("Count of Customer user type: {}".format(self.Customer_count))
        print("Count of Subscriber user type: {}".format(self.Subscriber_count))
        print("Calculated in {} Seconds\n".format(time.time()-start_time))

    def gender_info(self):
        print("__________________________________________________Gender Info__________________________________________________\n")
        start_time=time.time()
        if self.city.lower() =='chicago' or self.city.lower() == 'new_york_city':
            self.male_count = self.city_data_filtered['Gender'][self.city_data_filtered['Gender'] == 'Male'].count()
            self.female_count = self.city_data_filtered['Gender'][self.city_data_filtered['Gender'] == 'Female'].count()
            print("Count of male gender: {}".format(self.male_count))
            print("Count of female gender: {}\n".format(self.female_count))
        else:
            print("There's no gender data for this city")
        print("Calculated in {} Seconds\n".format(time.time()-start_time))

    def year_info(self):
        print("___________________________________________________Year Info___________________________________________________\n")
        start_time= time.time()
        if self.city.lower() =='chicago' or self.city.lower() == 'new_york_city':
            self.most_common_year = self.city_data_filtered['Birth Year'].mode()[0]
            self.most_recent_year = self.city_data_filtered['Birth Year'].max()
            self.most_earliest_year = self.city_data_filtered['Birth Year'].min()
            print("Most common year: {}".format(int(self.most_common_year)))
            print("Most earliest year: {}".format(int(self.most_earliest_year)))
            print("Most recent year: {}".format(int(self.most_recent_year)))
        else:    
            print("There's no year info for this city\n")
        
        print("Calculated in {} Seconds\n".format(time.time()-start_time))

'''     
Checking that data class is functioning well

#loading chicago_data
chicago_data = data('./chicago.csv')
#loading chicago and printing it 
chicago_data.load_city()
chicago_data.print_city_data()
'''

#welcome message
print("Hello, This is Bikeshare script to explore data\n")


#asking user what city he wants to filter 
city_list = ['Chicago','New York','New york','Washington']

while True:
    while True:
        City_input = input("Would you like to see data for chicago, or New York, or Washington?\n")
        if City_input.capitalize() in city_list:
            break
        else:
            print("You Entered a non valid city name! try again.")

    #adding underscore to new york city and city word to the string to make it as the same as the csv file name

    if City_input.lower() == 'new york':
        City_input = City_input.replace(' ', "_")
        City_input = City_input + "_city"

    #asking user if he wants to filter the data
    list_filter_data = ['Month','Day','Both', 'Not at all']
    while True:
        filter_data = input("Would you like to filter the data by month, day, both, or not at all?\n")
        if filter_data.capitalize() in list_filter_data:
            break
        else: 
            print("You Entered a non valid value! Try again.")

    #formating filter_data properly and extracting month and day values 
    months_not_in_the_data = ['July','August','September','October','November','December']
    months_list = ['January','February','March','April','May','June']

    if filter_data.lower() == 'both':
        while True:
            month = input("Insert the required month to filter data by\n")
            day = input("Insert the required day name to filter data by\n")
            if month.capitalize() in months_list:
                d = data(City_input,month.capitalize(),day.capitalize())

                break
            else: 
                print('You Entered a wrong value or the data for this month is not available.')
            
        
    elif filter_data.lower() == 'month':

        while True:
            month = input("Insert the required month to filter data by\n")
            if month.capitalize() in months_list:
                d = data(City_input,month.capitalize(),None)

                break
            else: 
                print('You Entered a wrong value or the data for this month is not available.')

    elif filter_data.lower() == 'day':
        day = input("Insert the required day name to filter data by\n")
        d = data(City_input,None,day.capitalize())

    elif filter_data.lower() == 'not at all':
        d= data(City_input,None,None)

    else:
        print("You entered wrong value")

    d.load_city()
    d.filter_data()
    d.most_pop_travel_times()
    d.most_pop_stations()
    d.trip_statistics()
    d.user_info()
    d.gender_info()
    d.year_info()

    user_response1= input('Would you like to view some data?y/n')
    if user_response1 =='y' or user_response1 == 'Y':
        d.view_data()
    user_response2 = input("Do you want to see another data?y/n")
    if user_response2 =='y' or user_response2 == 'Y':
        print('okayy')
    else:
        print("Exiting!!")
        break