from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from excel_data import get_data
import time
# from datetime import datetime
import sys
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from the .env file (if present)
    load_dotenv()

    USERNAME = os.getenv('USERNAME_MIS')
    PASSWORD = os.getenv('PASSWORD')
    URL = os.getenv('URL_MIS')

    if USERNAME == None or PASSWORD == None:
        print("Exiting the program...")
        sys.exit("Missing env !")

    # lang type - 'TH' or 'EN'
    lang_type = "EN"

    # number of edit button in page 
    arr_edit_btn = list(range(16,1,-1))

    # get data from excel
    excel_data = get_data(lang_type)
    if excel_data == False:
        print("Exiting the program...")
        sys.exit("lang_type must be 'TH' or 'EN'!")

    img_no = list(range(1, 21))
    driver = setup_driver()


    login(driver,URL,USERNAME, PASSWORD)
    navigate_to_ad_management(driver)
    process_page(driver, excel_data, arr_edit_btn, img_no, lang_type)
    

    print("Finishing...")
    driver.quit()



def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')

    # Initialize the Chrome WebDriver
    s = Service('C:/Users/MIS/Desktop/dev/chromedriver-win64/chromedriver.exe')
    return webdriver.Chrome(service=s,options=chrome_options)

def login(driver,url,username,password):
    driver.get(url)
    # Find the search box element and enter a query
    username_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[1]/ul/li[1]/dl/dd/input')))
    username_box.send_keys(username)
    pw_box = driver.find_element(By.XPATH,'/html/body/form/div[3]/div[1]/ul/li[2]/dl/dd/input')
    pw_box.send_keys(password)

    time.sleep(6)

    # Wait for the login button to be clickable and click it
    login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/div[3]/div[1]/ul/li[4]/input')))
    login_btn.click()

def navigate_to_ad_management(driver):
    # Nav
    iframe_left = driver.find_element(By.ID, "left")

    # switch to selected iframe
    driver.switch_to.frame(iframe_left)

    # click on AdvertisingManagement button
    driver.find_element(By.ID, '25').click()
    driver.switch_to.default_content()

    time.sleep(2)


def get_image_path(index, lang_type):
    file_name = f"{index}.jpg"
    folder = "image_en" if lang_type == "EN" else "image"
    return os.path.abspath(os.path.join(os.path.dirname(__file__), folder, file_name))


def process_page(driver, excel_data, arr_edit_btn, img_no, lang_type):
    # Main
    iframe_main = driver.find_element(By.ID, "main")
    driver.switch_to.frame(iframe_main)


    for index in range(len(arr_edit_btn)):
        print(f"round : {index+1}")
        if lang_type == "EN":
            driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/dl/dd[6]/select/option[2]").click()

        # go to page 10 
        driver.find_element(By.XPATH, '/html/body/form/div[3]/div/table[2]/tbody/tr/td/div/a[9]').click()

        # click on Edit button 
        driver.find_element(By.XPATH, f'/html/body/form/div[3]/div/table[1]/tbody/tr[{arr_edit_btn[index]}]/td[13]/a[1]').click()

        fill_form(driver, excel_data[index], img_no[index], lang_type)

def fill_form(driver, data, img_no, lang_type):
    # title input
        title = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[2]/input")
        title.clear()
        title.send_keys(data['Event_name'])

        # link input
        if str(data['Link']) == "nan":
            link = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[4]/input")
            link.clear()
        else:
            link = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[4]/input")
            link.clear()
            link.send_keys(data['Link'])

        # image_upload input
        image_path = get_image_path(img_no, lang_type)
        image_upload = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[3]/input[1]")
        image_upload.send_keys(image_path)

        # check file uploaded name
        assert os.path.basename(image_path) == str(img_no)+".jpg"

        # start time input
        start_time = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[7]/input")
        start_time.clear()
        start_time.send_keys(str(data['start_time']))

        # end time input
        end_time = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/ul/li[8]/input")
        end_time.clear()
        end_time.send_keys(str(data['end_time']))

        time.sleep(2)
        # submit btn 
        driver.find_element(By.XPATH, '/html/body/form/div[3]/div/div/ul/li[21]/input[1]').click()
        time.sleep(2)
        # accept alert
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        driver.switch_to.alert.accept()
        navigate_to_ad_management(driver)

if __name__ == "__main__":
    main()
#  # check end date and now
#     now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#     nowdate = datetime.strptime(now, '%Y/%m/%d %H:%M:%S')
#     end_date =  driver.find_element(By.XPATH,f"/html/body/form/div[3]/div/table[1]/tbody/tr[{arr_edit_btn[index]}]/td[8]").text
#     enddate = datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S')
#     if nowdate < enddate:
#         continue