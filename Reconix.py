import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

# File paths
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
def scrape_dork(dork, max_pages):
    try:
        print(f"Processing dork: {dork.strip()}")  # Debugging line
        # Construct the Google search URL
        search_url = f"https://www.google.com/search?q={dork.strip()}"

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

        page_count = 0
        while True:
            # Manually iterate over search result links
            links = driver.find_elements(By.XPATH, "//a[@href]")
            print(f"Found {len(links)} links on page {page_count + 1}.")  # Debugging line

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

            # Increment page counter
            page_count += 1

            # Check if we've reached the max number of pages
            if page_count >= max_pages:
                print(f"Reached the maximum number of pages ({max_pages}) for this dork.")
                break

            # Check if there's a "Next" button to go to the next page
            try:
                next_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
                next_button.click()
                time.sleep(3)  # Wait for the next page to load
            except NoSuchElementException:
                print("No more pages left.")
                break

    except Exception as e:
        print(f"An error occurred for dork: {dork} -> {e}")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Google Dork Scraper")
    parser.add_argument("-D", "--dork", help="Single Google dork to use", required=False)
    parser.add_argument("-F", "--file", help="File containing a list of Google dorks", required=False)
    parser.add_argument("-P", "--pages", help="Maximum number of pages to scrape per dork (default: 5, max: 30)", type=int, default=5)

    args = parser.parse_args()

    # Validate the number of pages
    max_pages = min(max(1, args.pages), 30)

    # Check if the user provided a dork or a file
    if args.dork:
        scrape_dork(args.dork, max_pages)
    elif args.file:
        if os.path.isfile(args.file):
            with open(args.file, 'r') as file:
                dorks = file.readlines()
                for dork in dorks:
                    scrape_dork(dork, max_pages)
                    time.sleep(10)  # Sleep to prevent being flagged
        else:
            print(f"File {args.file} does not exist.")
    else:
        print("Please provide a dork with -D or a file of dorks with -F.")

    # Close the browser
    driver.quit()
    print("Scraping completed. Results are saved in scraped.txt")

if __name__ == "__main__":
    main()
