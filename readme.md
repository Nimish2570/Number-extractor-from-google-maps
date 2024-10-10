# Number extractor from google maps  

This project is a Python application that uses Tkinter for the GUI and Playwright for web automation to scrape phone numbers and names from Google Maps based on a user-defined search keyword. The results are saved into a CSV file for easy access and analysis.

## Features

- User-friendly GUI for inputting search keywords and specifying the minimum number of results.
- Scrapes phone numbers and names from Google Maps.
- Validates user inputs for better error handling.
- Generates a CSV file with the search results.

## Requirements

To run this application, ensure you have the following installed:

- Python 3.6 or higher
- Playwright
- BeautifulSoup
- Tkinter (comes pre-installed with Python)
- CSV module (comes pre-installed with Python)

You can install Playwright and BeautifulSoup using pip:

```bash
pip install playwright beautifulsoup4


After installing, make sure to install the required browsers for Playwright:

bash
Copy code
playwright install
Usage
Clone this repository to your local machine:

bash
Copy code

Run the application:
bash
Copy code
python your_script_name.py
Enter a search keyword in the provided input box.

Specify the minimum number of results you want to retrieve (up to 500).

Click on the "Generate CSV" button.

The results will be saved in a CSV file named <search_keyword>_search_results.csv.

Input Validation
Minimum number of results should be at least 1.
Maximum number of results is capped at 500.
The search keyword cannot be empty.


License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Playwright - For web automation.
BeautifulSoup - For HTML parsing.
markdown
Copy code

### Notes:
- Replace `<repository_url>` and `<repository_directory>` with the actual URL and directory name of your GitHub repository.
- Update `your_script_name.py` with the actual name of your script.
- Add a screenshot if available, and replace `screenshot.png` with the correct path to your