from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

# Initialize the Chrome WebDriver
s = Service('C:/Users/MIS/Desktop/dev/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=s)

# Open Google
driver.get("http://www.google.com")
# Find the search box element and enter a query
search_box = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/textarea')
search_box.send_keys("Selenium Python tutorial")
# Perform the search
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(3)

# Close the browser
driver.quit()