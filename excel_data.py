import pandas as pd
import sys
import os
from datetime import datetime, time


def get_data(lang: str):
    if lang == "EN":
        df = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname(__file__), "excel_bot.xlsx")),'EN')
    elif lang == "TH":
        df = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname(__file__), "excel_bot.xlsx")),'TH')
    else:
        return False
    return df.to_dict(orient='records')

def format_dt(date_str:str,time_str:str):
    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Parse the time string to a time object
    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()

    # Combine date and time into a single datetime object
    merged_datetime = datetime.combine(date_obj.date(), time_obj)
    return merged_datetime.strftime("%Y-%m-%d %H:%M:%S")
if __name__ == '__main__':
    excel_data = get_data("EN")
    if excel_data == False:
        print("Exiting the program...")
        sys.exit("lang_type choose 'TH' or 'EN' !")
    for i in range(len(excel_data)):
        start_time = format_dt(str(excel_data[i]['start_date']),str(excel_data[i]['start_time']))
        end_time = format_dt(str(excel_data[i]['end_date']),str(excel_data[i]['end_time']))
        if str(excel_data[i]['link']) == "ไม่มีลิงก์":
            print(  excel_data[i]['event_name']+ " " + " " + " " + start_time + " " + end_time+"\n" )
        else:
            print(  excel_data[i]['event_name']+ " " + str(excel_data[i]['link'])  + " " + start_time + " " + end_time +"\n")