# LinkedIn Profile Scraper

This project provides tools for scraping LinkedIn profiles to extract detailed information on education and professional experiences. It is intended for academic and research purposes, aiming to facilitate data gathering for analyses of career paths and educational backgrounds.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

1. **Clone the repository:**

```bash
git clone https://github.com/LaFerraille/LinkedIn_scraper.git
cd project
```

2. **Install dependencies:**

You can install the necessary Python packages using `pip`:

`pip install -r requirements.txt`

3. **Chromedriver:**
Ensure you have ChromeDriver installed in the same directory as this project or in your PATH. Ensure that ChromeDriver match the version of your Google Chrome browser. Go this website to download the right version for your [Google Chrome version](https://chromedriver.chromium.org/downloads).

## Usage

To run the scraper, you need to provide the path to the Excel file containing LinkedIn profile first names and last names. The script supports optional arguments for filtering by school and specifying a starting year for experience entries. Please don't modify the size of the pop-up chrome screen while the code is running when you are not on headless mode.

```bash
python main.py --excel_path /path/to/your/excelfile.xlsx --username "your_username" --password "your_password" --schoolfilter "Optional School Name" --filter_from_year 2022 --headless
```

### Arguments 

- `--excel_path` (required): The path to the Excel file with LinkedIn profile URLs and the names of the individuals.
- `--username` (required): Your LinkedIn username or email to login.
- `--password` (required): Your LinkedIn password for login.
- `--schoolfilter` (optional): Filter profiles by a specific school name.
- `--filter_from_year` (optional): Specify the starting year to filter experiences, only including experiences from this year onwards.
- `--headless` (optional): Run the browser in headless mode. Use --headless to enable this mode.

## Improvements 

~ - Enhance the experience scraper to handle the multiple structure scenarios. Correct the internships labeling that is not perfectly implemented so far.
- Implement asynchronous processing or multi-threading to handle multiple profiles concurrently, reducing total runtime.
- Develop a GUI to facilitate non-technical users' operation of the script.
