import argparse
import pandas as pd
from tqdm import tqdm
from src.utils import init_driver, login, process_person, save_progress, load_progress

def main(args):
    # Initialize the driver with headless option
    driver = init_driver(headless=args.headless)
    login(driver, args.username, args.password)

    # Load DataFrame and progress
    df = pd.read_excel(args.excel_path)
    if 'PRENOM' not in df.columns or 'NOM' not in df.columns:
        raise ValueError("Excel file must contain 'PRENOM' and 'NOM' columns.")

    start_index = load_progress()
    results_df = pd.DataFrame()

    # Process each person in the DataFrame starting from the last saved index
    for index, row in tqdm(df.iterrows(), total=len(df), initial=start_index):
        if index < start_index:
            continue  # Skip rows that have already been processed

        try:
            person_results = process_person(driver, row, args.schoolfilter, args.filter_from_year)
            results_df = pd.concat([results_df, pd.DataFrame([person_results])], ignore_index=True)

            # Save results to CSV after each successful data retrieval
            results_df.to_csv('results_backup.csv', index=False)

            # Save the current index as progress
            save_progress(index + 1)
        except Exception as e:
            print(f"Error processing index {index}: {e}")
            break  

    driver.quit()
    print(results_df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process individuals from an Excel file.")
    parser.add_argument('--excel_path', type=str, help='Path to the Excel file containing the data.')
    parser.add_argument('--username', type=str, required=True, help='Username for login.')
    parser.add_argument('--password', type=str, required=True, help='Password for login.')
    parser.add_argument('--schoolfilter', type=str, default=None, help='Optional filter for specific school in education data.')
    parser.add_argument('--filter_from_year', type=int, default=2022, help='Year from which to filter experience data.')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode. Default is False.')
    
    args = parser.parse_args()
    main(args)
