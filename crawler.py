from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import json

import time
import pandas as pd

# Set up Chrome options and web driver
profile = f"/home/truongxl/.config/google-chrome/Profile 1"

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={profile}")
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--ignore-certificate-errors')

    
chrome_path = '/usr/bin/google-chrome-stable'
chrome_options.binary_location = chrome_path

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://twitter.com/login")
time.sleep(4)

def load_config(config_file):
    with open(config_file, "r") as f:
        config = json.load(f)
    return config

config = load_config("config.json")
username = config["username"]
password = config["password"]
topics = config["topics"]
data_dir = config["data_dir"]
num_scrolls = config["num_scroll"]
num_tweet_per_topic = config["num_tweet_per_topic"]


##################################LOGIN#############################################
# Find the username and password input fields and enter your credentials
username = driver.find_element(By.XPATH,"//input[@name='text']")
username.send_keys(username)
next_button = driver.find_element(By.XPATH,"//span[contains(text(),'Next')]")
next_button.click()
time.sleep(5)
password = driver.find_element(By.XPATH,"//input[@name='password']")
password.send_keys(password)
log_in = driver.find_element(By.XPATH,"//span[contains(text(),'Log in')]")
time.sleep(5)
log_in.click()
#####################################################################################


df = pd.DataFrame(columns=["Topic", "Username", "Tweet", "Likes", "Views", "Reposts", "Replies", "Date"])


while 1:
    # Crawl data for each topic
    for topic in topics:
        # Search for a specific topic
        try:
            search_input = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//input[@data-testid="SearchBox_Search_Input"]'))
            )
            search_input.send_keys(Keys.CONTROL + "a")  # Select all text
            search_input.send_keys(Keys.BACKSPACE)  # Clear the input field
            search_input.send_keys(topic)
            time.sleep(2)
            search_input.submit()
            time.sleep(2)
        except:
            print("Error searching for topic:", topic)
            time.sleep(10)
            driver.refresh()
            continue

        # Wait for the search results page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="primaryColumn"]'))
        )

        # Scroll to load more tweets
        for _ in range(num_scrolls):
            # Scroll down to load more tweets
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(5)  # Adjust the sleep time as needed

        # Crawl data from the loaded tweets
        try:
            tweets = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
            )
        except:
            time.sleep(10)
            continue

        for tweet in tweets:
            if len(df) >= num_tweet_per_topic:
                break
            try:
                username = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                tweet_content = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                like_count = tweet.find_element(By.XPATH, ".//div[@data-testid='like']").text
                view_count = tweet.find_element(By.XPATH, ".//a[@role='link']/div/div[2]/span/span/span").text
                repost_count = tweet.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
                reply_count = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']").text
                date = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
            except:
                time.sleep(10)
                continue
            
            print("Username:", username)
            print("Tweet:", tweet_content)
            print("Likes:", like_count)
            print("Views:", view_count)
            print("Reposts:", repost_count)
            print("Replies:", reply_count)
            print("Date:", date)
            print("---------------------------")
            existing_tweet = df[
                (df["Username"] == username) &
                (df["Tweet"] == tweet_content)
                ].any(axis=None)

            if existing_tweet:
                continue

            new_row = {"Topic": topic, "Username": username, "Tweet": tweet_content, "Likes": like_count, "Views": view_count, "Reposts": repost_count, "Replies": reply_count, "Date": date}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.execute_script("window.history.go(-(window.history.length));")
        driver.refresh()

# save the dataframe to an excel file exist
        if os.path.isfile(os.path.join(data_dir, "tweet_information.xlsx")):
            # read the existing excel file
            existing_df = pd.read_excel(os.path.join(data_dir, "tweet_information.xlsx"))
            # append the new data to the existing file
            df = pd.concat([existing_df, df], ignore_index=True)
            # save the updated dataframe
            df.to_excel(os.path.join(data_dir, "tweet_information.xlsx"), index=False)
        else:
        # Save the DataFrame to an Excel file
            output_file = os.path.join(data_dir, "tweet_information.xlsx")
            df.to_excel(output_file, index=False)

        # Quit the driver
driver.quit()
