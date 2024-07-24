import pandas as pd
import sys
import os

def get_data(lang: str):
    if lang == "EN":
        df = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname(__file__), "excel_bot.xlsx")),'EN')
    elif lang == "TH":
        df = pd.read_excel(os.path.abspath(os.path.join(os.path.dirname(__file__), "excel_bot.xlsx")),'TH')
    else:
        return False
    return df.to_dict(orient='records')

if __name__ == '__main__':
    excel_data = get_data("TH")
    if excel_data == False:
        print("Exiting the program...")
        sys.exit("lang_type choose 'TH' or 'EN' !")
    len_edit_btn = list(range(16,1,-1))
    print(len_edit_btn)
    for index in range(len(len_edit_btn)):
        print(index)
    print(f'/html/body/form/div[3]/div/table[1]/tbody/tr[{len_edit_btn[0]}]/td[13]/a[1]')
    print(list(reversed(range(2,17))))
    no = list(range(1, 21))

    for i in range(len(excel_data)):
        if str(excel_data[i]['Link']) == "nan":
            print(  excel_data[i]['Event_name']+ " " + " " + " " + str(excel_data[i]['start_time']) + " " + str(excel_data[i]['end_time']) + " " + str(no[i])+".jpg")
        else:
            print(  excel_data[i]['Event_name']+ " " + str(excel_data[i]['Link'])  + " " + str(excel_data[i]['start_time']) + " " + str(excel_data[i]['end_time'])+ " " + str(no[i])+".jpg")