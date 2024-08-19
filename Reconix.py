from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# File paths
dorks_file = "dorks.txt"
output_file = "scraped.txt"

# Setup Firefox with Geckodriver
options = Options()
options.headless = True  # Run Firefox in headless mode
driver = webdriver.Firefox(options=options)

# Function to check for CAPTCHA
def check_for_captcha():
    try:
        # Check if the CAPTCHA div is present
        captcha_present = driver.find_element(By.ID, "captcha-form")
        return True if captcha_present else False
    except NoSuchElementException:
        return False

# Function to filter URLs
def is_valid_url(url):
    # Skip any URLs containing 'google'
    if url and "google" not in url.lower():
        return True
    return False

# Function to handle user acceptance prompts
def wait_for_user_acceptance():
    print("Please accept any cookies or agreements if prompted.")
    accepted = False
    while not accepted:
        time.sleep(5)
        try:
            # Assume user has accepted the prompts and the content is loaded
            driver.find_element(By.TAG_NAME, "body")  # Check if body is present
            accepted = True
        except NoSuchElementException:
            print("Waiting for user to accept the prompt...")
            continue

# Function to scrape Google search results for a given dork
def scrape_dork(dork):
    try:
        print(f"Processing dork: {dork.strip()}")  # Debugging line
        # Construct the Google search URL
        search_url = f"https://www.google.com/search?q=inurl:\"{dork.strip()}\""

        # Open the Google search URL
        driver.get(search_url)
        time.sleep(3)  # Wait for the page to load

        # Check if a CAPTCHA is present
        if check_for_captcha():
            print("CAPTCHA detected. Please solve it manually.")
            solved = False
            while not solved:
                time.sleep(10)
                solved = not check_for_captcha()  # Continue only if CAPTCHA is solved
            if solved:
                print("CAPTCHA solved. Continuing...")
            else:
                print("CAPTCHA not solved after waiting. Moving on.")
                return  # Skip this dork if CAPTCHA is still present

        # Wait for the user to accept any prompts
        wait_for_user_acceptance()

        # Manually iterate over search result links
        links = driver.find_elements(By.XPATH, "//a[@href]")
        print(f"Found {len(links)} links.")  # Debugging line

        with open(output_file, 'a') as f:
            for link in links:
                try:
                    url = link.get_attribute("href")
                    if is_valid_url(url):
                        # Capture URLs that do not contain 'google'
                        print(f"Saving URL: {url}")  # Output to console
                        f.write(url + "\n")  # Write to file
                    else:
                        print(f"Skipping URL: {url}")  # Skip Google-related URLs
                except NoSuchElementException:
                    print("Element not found. Skipping...")
                    continue

    except Exception as e:
        print(f"An error occurred for dork: {dork} -> {e}")

# Read dorks from the file
with open(dorks_file, 'r') as file:
    dorks = file.readlines()

# Iterate over all dorks and scrape Google search results
for dork in dorks:
    scrape_dork(dork)
    time.sleep(10)  # Sleep to prevent being flagged

# Close the browser
driver.quit()

print("Scraping completed. Results are saved in scraped.txt")
