# Reconix
Reconix is a A Python-based tool that allows you to scrape Google search results for specific dorks. You can either provide a single dork or a file containing a list of dorks to search.

python Reconix.py -D "Dorks"

python Reconix.py -F <dorks_file>


Options:
-D, --dork:
Description: Use this option to specify a single Google dork.
Example:
python3 Reconix.py -D "inurl:/admin/login.php"

Result: The tool will search Google using the specified dork and scrape the results.
-F, --file:

Description: Use this option to provide a file containing a list of Google dorks (one per line).
Example:
python Reconix.py -F dorks.txt
Result: The tool will read each dork from the file and perform a Google search, scraping the results for each dork sequentially.

Output:
The results of the scraping will be saved in a file named scraped.txt in the same directory as the script.
The output file will contain the URLs that match the dork searches, excluding any URLs containing "google".

# GeckoDriver Install

Download geckodriver:
Visit the geckodriver releases page on GitHub.
https://github.com/mozilla/geckodriver/releases
Download the version suitable for your operating system (Windows, macOS, Linux).
2. Install geckodriver:
Linux/macOS:

Extract the downloaded file:
tar -xvzf geckodriver-v0.32.0-linux64.tar.gz
Move it to a directory in your system's PATH:
sudo mv geckodriver /usr/local/bin/

Windows:
Extract the downloaded .zip file.
Move geckodriver.exe to a directory included in your PATH, or add the directory containing geckodriver.exe to your PATH.
3. Verify Installation:
Open a terminal or command prompt and run:
geckodriver --version
You should see output showing the version of geckodriver installed.
