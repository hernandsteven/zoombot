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
    current_date = dt.datetime.now()

    dictionary =  {
        "month": current_date.strftime('%m'),
        "day":   current_date.strftime('%d'),
        "year": current_date.strftime('%Y'),
        "hour": current_date.strftime('%H'),
        "minute": current_date.strftime("%M")
    }
    return dictionary

def time_difference(meeting_time):
    meeting_time_hour = int(meeting_time[0:2])
    meeting_time_minute = int(meeting_time[3:5])
    current_time_hour = int(time()['hour'])
    current_time_minute = int(time()['minute'])

    hour_difference = str((meeting_time_hour - current_time_hour))
    minute_difference = str((meeting_time_minute - current_time_minute))
    if(str(hour_difference[0]) == '-'):
        return False
    elif(minute_difference[0] == '-'):
        print(hour_difference)
        if(hour_difference == 0):
            hour_difference = str((int(hour_difference) - 1))
            minute_difference = str(abs((current_time_minute - int(minute_difference[1]))-59))
            return ':'.join([hour_difference, minute_difference])

    difference = ':'.join([hour_difference, minute_difference])
    return difference

def sleep(secs):
    t.sleep(secs)

def csv_to_df():
    if(path.exists('./meetings.csv')):
        # file exists, read the data
        df = pd.read_csv('meetings.csv')
        return df
        
    else:
        columns = [['CLASS', 'DATE', 'TIME','URL', 'PASSWORD',]]

        # file does not exist, create file and write columns
        with open('meetings.csv','w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(columns)
        file.close()

        df = pd.read_csv('meetings.csv')
        return df

def new_entry(column_name, entry,row):
    column_list = ["CLASS", "DATE","TIME", "URL", "PASSWORD"]
    df = csv_to_df()
    if(column_name == 'CLASS'):
        row = (len(df.index))
        df.at[row,column_name] = str(entry)
        df.to_csv('meetings.csv', index=False)
        return row
    else:
        print(row)
        df.at[float(row),column_list[column_list.index(column_name)]] = entry
        df.to_csv('meetings.csv', index=False)
        
def join_meeting(meeting_name, meeting_date, meeting_time, meeting_url, meeting_pw):
    #time_left = time_difference(meeting_time)
    #if(time_left == '0:0'):
    print('Attempting to join ' + meeting_name + '.')
    wb.open_new(meeting_url)
    sleep(3)
    chrome_button = pg.locateOnScreen('./chrome_button.PNG')
    pg.click(chrome_button)
    sleep(2)
    pg.write(meeting_pw)
    pg.press('enter')
    sleep(1)
    no_video_button = pg.locateOnScreen('./no_video_button.PNG')
    pg.click(no_video_button)
    pg.sleep(2)
    join_audio_button = pg.locateOnScreen('./join_audio_button.PNG')
    pg.click(join_audio_button)
    print('Joined meeting succesfully!')
    """    
    else:
        time_left = time_difference(meeting_time)
        hours = time_left[0:int(len(time_left)/2)]
        minutes = time_left[int((len(time_left)/2)+1):int(len(time_left))]
        
        print('\n' + meeting_name + ' starts in ' + hours + ' hours and ' + minutes + ' minutes.')
        sleep(3)

        while(time_left != '0:0'):
            time_left = time_difference(meeting_time)
            print('\nJoining '+ meeting_name + ' in ' + hours + ' hours and ' + minutes + ' minutes.')
            sleep(30)
    """
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
        
        meeting_to_join = str(input('\nWhat meeting would you like to join?: '))

        if meeting_to_join in saved_meetings:
            meeting_row_index = saved_meetings.index(meeting_to_join)
            sleep(1)
            join_meeting(
                meeting_to_join, df.at[meeting_row_index,'DATE'],
                df.at[meeting_row_index,'TIME'],
                df.at[meeting_row_index,'URL'],
                df.at[meeting_row_index,'PASSWORD']
            )

    # User enters 'n', prompting them to save a new meeting
    elif(user_input == "n"):
        row = int(len(df.index))

        input_name = str(input('What name would you like to give the meeting? (what class it?): '))
        new_entry('CLASS',input_name,row)

        input_date = str(input('What day is your meeting? (ex, \"8/31/2021\"): '))
        new_entry('DATE', input_date,row)

        input_time = str(input('What time is your meeting? (In 24hr format, 5:00pm would be 17:00): '))
        new_entry('TIME', input_time,row)

        input_url = str(input('Please paste the zoom meeting url (make sure theres no extra spaces!): ').strip())
        new_entry('URL', input_url, row)

        input_password = str(input('Enter meeting password, if there\'s none press Enter: '))
        new_entry('PASSWORD', input_password, row)

        print('Awesome, your meeting information is saved!')
    else:
        print('Hmm, seems like you entered \"' + user_input + '\". Lets try that again.')
        sleep(1)
        intro()

def main():
   csv_to_df()
   intro()
   
main()


