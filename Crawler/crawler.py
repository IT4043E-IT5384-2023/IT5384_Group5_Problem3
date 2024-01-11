from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os
import json

import time
import pandas as pd

# Set up Chrome options and web driver

chrome_options = Options()
chrome_options.add_argument('--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--ignore-certificate-errors')

    
chrome_path = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
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
            
            # get information tweet: created_at, default_profile, default_profile_image, description, favourites_count, followers_count, friends_count	, geo_enabled, id, lang, location, profile_background_image_url, profile_image_url, statuses_count	, screen_name	, verified, average_tweets_per_day, account_age_days
            try:
                screen_name = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
                created_at = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
                default_profile = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                default_profile_image = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                followers_count = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                friends_count = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                geo_enabled = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                id = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('aria-label')
                lang = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[1]/div[1]/div/span").get_attribute('lang')
                location = tweet.find_element(By.XPATH, '//div[@data-testid="UserProfileHeader_Items"]').text.split('\n')[1]
                profile_background_image_url = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                profile_image_url = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                statuses_count = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                verified = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                average_tweets_per_day = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                account_age_days = tweet.find_element(By.XPATH, ".//div/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/span").get_attribute('aria-label')
                description = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
                favourites_count = tweet.find_element(By.XPATH, ".//div[@data-testid='like']").text
                view_count = tweet.find_element(By.XPATH, ".//a[@role='link']/div/div[2]/span/span/span").text
                repost_count = tweet.find_element(By.XPATH, ".//div[@data-testid='retweet']").text
                reply_count = tweet.find_element(By.XPATH, ".//div[@data-testid='reply']").text

            except:
                time.sleep(10)
                continue

            new_row = {"created_at": created_at, "default_profile": default_profile, "default_profile_image": default_profile_image, "description": description, "favourites_count": favourites_count, "followers_count": followers_count, "friends_count": friends_count, "geo_enabled": geo_enabled, "id": id, "lang": lang, "location": location, "profile_background_image_url": profile_background_image_url, "profile_image_url": profile_image_url, "statuses_count": statuses_count, "screen_name": screen_name, "verified": verified, "average_tweets_per_day": average_tweets_per_day, "account_age_days": account_age_days, "view_count": view_count, "repost_count": repost_count, "reply_count": reply_count}

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