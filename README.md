# Reconix
Reconix is a A Python-based tool that allows you to scrape Google search results for specific dorks. You can either provide a single dork or a file containing a list of dorks to search.

python Reconix.py -D "<dork>"
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
