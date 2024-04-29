import time
from datetime import datetime
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import sys
sys.path.append('..')


def init_driver(headless=False):

    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--incognito")
    if headless : 
        options.add_argument("--headless") 
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def login(driver, username, password):
    url = 'https://www.linkedin.com/login/fr?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(url)
    time.sleep(3)

    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[class='btn__primary--large from__button--floating']").click()
    time.sleep(3)


def get_profile(driver, firstname, lastname, schoolfilter=None):
    if schoolfilter:
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={firstname}%20{lastname}&origin=FACETED_SEARCH&schoolFreetext=%22{schoolfilter}%22&"
    else:
        search_url = f"https://www.linkedin.com/search/results/people/?keywords={firstname}%20{lastname}&origin=GLOBAL_SEARCH_HEADER"
    driver.get(search_url)
    time.sleep(3)
    try:
        # Attempt to click the first profile link in the search results
        profile_link = driver.find_element(By.CSS_SELECTOR, "div[class^='entity-result']").find_element(By.CSS_SELECTOR, "a[class^='app-aware-link']")
        profile_link.click()
        time.sleep(3)
        return driver.current_url  # Returns the URL of the profile
    except Exception as e:
        print(f"Failed to find or navigate to profile for {firstname} {lastname} with error: {e}")
        return None
    

def convert_date_range_to_standard_format(date_range):
    """
    Converts a date range from 'mm. yyyy - mm. yyyy' to 'dd/mm/yyyy - dd/mm/yyyy'.
    Strips any extraneous text such as durations and descriptions.
    """
    month_mapping = {
        "janv": "01", "févr": "02", "mars": "03", "avr": "04",
        "mai": "05", "juin": "06", "juil": "07", "août": "08",
        "sept": "09", "oct": "10", "nov": "11", "déc": "12"
    }
    
    # Remove unwanted text like durations
    date_range = re.sub(r' · .*$', '', date_range)

    # Split the date range into start and end parts
    parts = date_range.split(' - ')
    formatted_dates = []

    for part in parts:
        month_found = False
        for month_abbr, month_num in month_mapping.items():
            if month_abbr in part:
                year = re.search(r'\d{4}', part).group()  # Find the year
                formatted_date = f"01/{month_num}/{year}"
                formatted_dates.append(formatted_date)
                month_found = True
                break
        if not month_found:  # Handle cases where a month might not be found due to text issues
            formatted_dates.append("Unknown date")

    # Join only the first and last elements to avoid duplication in case of similar start and end dates
    if len(formatted_dates) > 1:
        return f"{formatted_dates[0]} - {formatted_dates[-1]}"
    elif formatted_dates:
        return formatted_dates[0]
    else:
        return "Date range error"


def clean_text(text, handling_dates=False):
    """
    Removes unnecessary new lines and reduces multiple spaces to a single space.
    """
    if handling_dates:
        text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces/newlines with a single space and strip trailing spaces
        return text
    
    else :
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces or new lines with single space
        parts = text.split()
        # Remove duplicates by converting to a set while preserving order
        seen = set()
        parts = [x for x in parts if not (x in seen or seen.add(x))]
        return ' '.join(parts)

def is_internship(text):
    """
    Checks if the text contains keywords that indicate an internship.
    """
    keywords = {"intern", "internship", "stage", "summer", "off-cycle", "trainee", "assistant", "stagiaire"}
    return any(keyword.lower() in text.lower() for keyword in keywords)

def get_experiences(driver, filter_from_year=2022):
    experiences = []
    temp_company = None  # To store company name when dates are detected in the company field
    using_temp_company = False 
    pattern = r'\b(janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)\.? \d{4} -'
    i = 0
    try:
        # Attempt to locate the experience section using more general selectors
        profile_section = driver.find_elements(By.XPATH, "//section[contains(@class, 'artdeco-card') and contains(@class, 'pv-profile-card')]")
        for section in profile_section:
            header = section.find_element(By.TAG_NAME, "h2").text
            if "Expérience" in header:
                exp_items = section.find_elements(By.CSS_SELECTOR, "div > ul:first-of-type > li")
                for item in exp_items:
                    try:
                        
                        # Generalize selectors to handle different layouts
                        title_div = item.find_element(By.CSS_SELECTOR, "div.display-flex.flex-column.full-width")
                        job_title_elements = title_div.find_elements(By.CSS_SELECTOR, "div.t-bold span")
                        company_elements = title_div.find_elements(By.CSS_SELECTOR, "span.t-14.t-normal")
                        try : 
                            company = clean_text(company_elements[0].text.split('·')[0].strip()) if not using_temp_company else temp_company
                            job_title = clean_text(title_div.find_element(By.CSS_SELECTOR, "div.t-bold span").text.split('\t')[0].strip())
                        except :
                            raw_company = clean_text(' '.join([elem.text for elem in company_elements if elem.text.strip()])).split('·')[0].strip()
                            if len(item.find_elements(By.CSS_SELECTOR, "li")) > 0:
                                job_title = title_div.find_element(By.CSS_SELECTOR, "div.t-bold span").text.split('\t')[0].strip()
                                company = raw_company.split('·')[0] if not using_temp_company else temp_company
                            else : 
                                job_title = clean_text(' '.join([elem.text for elem in job_title_elements if elem.text.strip()]))
                                company = re.sub(pattern+r".*\'", '', raw_company).strip()

                        date_range = title_div.find_elements(By.CSS_SELECTOR, "span.t-14.t-normal.t-black--light")[0].text
                        location_elements = title_div.find_elements(By.CSS_SELECTOR, "span.t-14.t-normal.t-black--light")
                        if len(location_elements) > 1:
                            location = clean_text(location_elements[1].text.split('·')[0])
                        else:
                            location = "Unknown location"  # Default to unknown if no location is present

                        internship = is_internship(job_title + " " + company)
                        pattern = r'\b(janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)\.? \d{4} -|CDD|CDI'
                        if re.search(pattern, company):
                            if i == 0:
                                using_temp_company = True
                                temp_company = job_title
                                i += 1
                                continue
                            else : 
                                company = temp_company
                        else:
                            using_temp_company = False

                        # Convert and filter dates
                        date_range = convert_date_range_to_standard_format(date_range)
                        if date_range.split(' - ')[-1] == "Unknown date":
                            end_year = datetime.now().year
                        else : 
                            end_year = int(date_range.split(' - ')[-1].split('/')[2])
                        if end_year < filter_from_year:
                            continue

                    
                        experiences.append({
                            'title': job_title,
                            'company': company,
                            'date_range': date_range,
                            'location': location,
                            'internship': internship
                        })


                    except Exception as exp_err:
                        pass

    except Exception as e:
        print(f"Error getting experiences: {e}")
                
    return experiences


def get_education(driver):
    educations = []
    try:
        # Attempt to locate the experience section using more general selectors
        profile_section = driver.find_elements(By.XPATH, "//section[contains(@class, 'artdeco-card') and contains(@class, 'pv-profile-card')]")
        for section in profile_section:
            header = section.find_element(By.TAG_NAME, "h2").text
            if "Formation" in header:
                edu_items = section.find_elements(By.CSS_SELECTOR, "div > ul:first-of-type > li")
                for item in edu_items:
                    try:
                        # Education details are within a flex-column div
                        title_div = item.find_element(By.CSS_SELECTOR, "div.display-flex.flex-column.full-width")
                        school_title_elements = title_div.find_elements(By.CSS_SELECTOR, "div.t-bold span")
                        school_name = clean_text(' '.join([elem.text for elem in school_title_elements if elem.text.strip()]))
                        degree_and_program = ''#title_div.find_element(By.CSS_SELECTOR, "span.t-14.t-normal").text.strip()

                        # # Extracting additional details like the date range, handled similarly to experiences
                        # date_text = title_div.find_elements(By.CSS_SELECTOR, "span.t-14.t-normal.t-black--light")[-1].text.strip()
                        # start_year = int(re.search(r'\d{4}', date_text).group())  # Extract the start year from the date text
                        
                        # Add to educations list only if it meets the year filter
                        educations.append({
                            'school': school_name,
                        })
                    except Exception as e:
                        pass

    except Exception as e:
        print(f"Error getting experiences: {e}")
        

    return educations


def process_person(driver, row, schoolfilter, filter_from_year):

    # Get profile
    url = get_profile(driver, row['PRENOM'], row['NOM'], schoolfilter)    
    experiences = get_experiences(driver, filter_from_year)
    educations = get_education(driver)
    
    # Creating data structure for this person
    person_data = {
        'first name': row['PRENOM'],
        'last name': row['NOM'],
        'link': url,
    }
    
    # Add experiences to person_data
    for i, exp in enumerate(experiences, start=1):
        person_data[f'title_{i}'] = exp['title']
        person_data[f'company_{i}'] = exp['company']
        person_data[f'date_range_{i}'] = exp['date_range']
        person_data[f'location_{i}'] = exp['location']
        person_data[f'internship_{i}'] = exp['internship']
    
    # Add educations to person_data
    for j, edu in enumerate(educations, start=1):
        person_data[f'school_{j}'] = edu['school']
    
    return person_data

def save_progress(index):
    with open('progress.txt', 'w') as f:
        f.write(str(index))

def load_progress():
    try:
        with open('progress.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0




