# Steven Hernandez 
# 8/31/2021
# All rights reserved 
import pyautogui as pg
import time as t
import webbrowser as wb
from os import path
import pandas as pd
import csv
import datetime as dt

def time():
    """
        Provide the current time as a dictionary

        :param None
        :return type: dict
    """
    current_date = dt.datetime.now()
    
    dictionary =  {
        "month": current_date.strftime('%m'),
        "day":   current_date.strftime('%d'),
        "year": current_date.strftime('%Y'),
        "hour": current_date.strftime('%H'),
        "minute": current_date.strftime("%M"),
    }

    return dictionary
   

def time_difference(meeting_time):
    current_time_val = dt.datetime.strptime(dt.datetime.now().strftime('%m/%d/%Y %H:%M'),'%m/%d/%Y %H:%M')
    meeting_time_val = dt.datetime.strptime(meeting_time,"%m/%d/%Y %H:%M")
    remaining_time = meeting_time_val - current_time_val
    return remaining_time

    
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes
   
def sleep(secs):
    t.sleep(secs)

def csv_to_df():
    if(path.exists('./meetings.csv')):
        # file exists, read the data
        df = pd.read_csv('meetings.csv')
        return df
        
    else:
        columns = [['CLASS', 'DATETIME','URL', 'PASSWORD',]]

        # file does not exist, create file and write columns
        with open('meetings.csv','w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(columns)
        file.close()

        df = pd.read_csv('meetings.csv')
        return df

def new_entry(column_name,entry,row):
    column_list = ["CLASS", "DATETIME", "URL", "PASSWORD"]
    df = csv_to_df()
    #if adding a new row
    if(column_name == 'CLASS'):
        row = (len(df.index))
        df.at[row,column_name] = str(entry)
        df.to_csv('meetings.csv', index=False)
        return row
    else:
        print(row)
        df.at[float(row),column_list[column_list.index(column_name)]] = entry
        df.to_csv('meetings.csv', index=False)

def join_meeting(meeting_name, meeting_datetime, meeting_url, meeting_pw):
    """
    Join zoom meeting

    :param str meeting_name: The name of the meeting
    :param str meeting_dateime: The date and time of the meeting
    :param str meeting url:  The url for zoom meeting
    :param str meeting_pw:   The password for the meeting
    :return type: void

    """

    remaining_hours, remaining_minutes = convert_timedelta(time_difference(meeting_datetime))
    
    if remaining_minutes <= 0:
        #Open zoom url in browser
        print('Attempting to join ' + meeting_name + '.')
        wb.open_new(meeting_url)
        sleep(3)

        #Click on button to join zoom meeting
        chrome_button = pg.locateOnScreen('./images/chrome_button.PNG')
        pg.click(chrome_button)
        sleep(5)

        #If password enter password
        pg.write(meeting_pw)
        pg.press('enter')
        sleep(3)

        #Enter zoom meeting with no video
        no_video_button = pg.locateOnScreen('./images/no_video_button.PNG')
        pg.click(no_video_button)
        sleep(2)

        #Join audio
        join_audio_button = pg.locateOnScreen('./images/join_audio_button.PNG')
        pg.click(join_audio_button)
        print('Joined meeting succesfully!')
 
    else:
        remaining_hours, remaining_minutes = convert_timedelta(time_difference(meeting_datetime))
        
        print('\n' + meeting_name + ' starts in ' + str(remaining_hours) + ' hours and ' + str(remaining_minutes) + ' minutes.')
        sleep(3)

        rem = str(remaining_hours)+":"+str(remaining_minutes)
        
        while rem != '0:0':
            remaining_hours, remaining_minutes = convert_timedelta(time_difference(meeting_datetime))
            rem = str(remaining_hours)+":"+str(remaining_minutes)
            print('\nJoining '+ meeting_name + ' in ' + str(remaining_hours) + ' hours and ' + str(remaining_minutes) + ' minutes.')
            sleep(1)

        join_meeting(meeting_name, meeting_datetime, meeting_url, meeting_pw)
def intro():
    df = csv_to_df()

    print('Hello, this is Zoombot. I can help you join your zoom meetings while you\'re AFK. \n')
    
    print('Would you like to join a previously saved zoom meeting?\n')

    user_input = str(input('Enter [y] or [n]: ')).lower().strip()

    # User enters 'y', show them all the saved meetings
    if(user_input == "y"):
        saved_meetings = []

        print('\nHere are your saved meetings --> \n')

        for i in range(len(df.index)):
            saved_meetings.append(df.at[i,'CLASS'])
        
        print('\n\n'.join(saved_meetings))
        
        meeting_to_join = str(input('\nWhat meeting would you like to join?: ').strip())

        if meeting_to_join in saved_meetings:
            meeting_row_index = saved_meetings.index(meeting_to_join)
            
            join_meeting(
                meeting_to_join, 
                df.at[meeting_row_index,'DATETIME'],
                df.at[meeting_row_index,'URL'],
                df.at[meeting_row_index,'PASSWORD']
            )

    # User enters 'n', prompting them to save a new meeting
    elif(user_input == "n"):
        row = int(len(df.index))

        input_name = str(input('What name would you like to give the meeting? (what class it?): '))
        new_entry('CLASS',input_name,row)

        input_datetime = str(input('What day and time is your meeting? (ex, \"8/31/2021 15:23\"): '))
        new_entry('DATETIME', input_datetime,row)

        input_url = str(input('Please paste the zoom meeting url (make sure theres no extra spaces!): ').strip())
        new_entry('URL', input_url, row)

        input_password = str(input('Enter meeting password, if there\'s none press Enter: '))
        new_entry('PASSWORD', input_password, row)

        print('Awesome, your meeting information is saved!')

        intro()
    else:
        print('Hmm, seems like you entered \"' + user_input + '\". Lets try that again.')
        sleep(1)
        intro()

def main():
   csv_to_df()
   intro()

  #print(convert_timedelta(time_difference('02/25/2022 18:30')))
   
   
main()


