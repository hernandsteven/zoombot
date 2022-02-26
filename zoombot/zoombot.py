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
    return None

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
"""
Join zoom meeting

:param str meeting_name: The name of the meeting
:param str meeting_date: The date of the meeting
:param str meeting_time: The time of the meeting
:param str meeting url:  The url for zoom meeting
:param str meeting_pw:   The password for the meeting
:return type: void

"""
def join_meeting(meeting_name, meeting_date, meeting_time, meeting_url, meeting_pw):
    #time_left = time_difference(meeting_time)
    #if(time_left == '0:0'):
    print('Attempting to join ' + meeting_name + '.')
    wb.open_new(meeting_url)
    sleep(3)

    chrome_button = pg.locateOnScreen('./images/chrome_button.PNG')
    pg.click(chrome_button)
    sleep(5)

    pg.write(meeting_pw)
    pg.press('enter')
    sleep(3)

    no_video_button = pg.locateOnScreen('./images/no_video_button.PNG')
    pg.click(no_video_button)
    pg.sleep(2)

    join_audio_button = pg.locateOnScreen('./images/join_audio_button.PNG')
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
            
            join_meeting(
                meeting_to_join, 
                df.at[meeting_row_index,'DATE'],
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

        intro()
    else:
        print('Hmm, seems like you entered \"' + user_input + '\". Lets try that again.')
        sleep(1)
        intro()

def main():
   csv_to_df()
   intro()
   
   
main()


