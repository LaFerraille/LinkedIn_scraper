# LinkedIn Scraper

Welcome to the LinkedIn Scraper project! This notebook is designed for scraping LinkedIn to retrieve basic information about people, adaptable for specific use-cases.

## Prerequisites

- **Python 3.6+** is required.
- **Selenium**, **BeautifulSoup (bs4)**, **Pandas**, and **undetected_chromedriver** must be installed.
- **Google Translator** and **langid** libraries for optional text translation.
- **Chromedriver** must be installed in the same directory as this project for Selenium to interact with Google Chrome.

## Setup

1. **Clone the Repository**: Clone this repo to your local machine.
2. **Chromedriver**: Download and place `chromedriver` in the project directory. Ensure it matches your Chrome version.
3. **Dataframe Setup**: Prepare a Pandas DataFrame named `df` with at least `FIRST_NAME` and `LAST_NAME` columns.
4. **Configuration**: Enter your LinkedIn credentials in the provided placeholders within the code.
5. **Run**: Execute the notebook cells sequentially to start scraping. Adjust the search parameters as needed for your specific use-case.

## Note

This project is for educational purposes. Be mindful of LinkedIn's terms of service regarding automated data collection.

