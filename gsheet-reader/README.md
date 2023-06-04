# GSheetReader

GSheetReader is a Python class that allows you to extract data from a Google Sheet, filter out empty rows and columns, and save the data to CSV and Excel files.

## Prerequisites

- Python 3.7 or above
- The following packages are required (see the `requirements.txt` file for the specific versions):
  - gspread
  - oauth2client
  - pandas

## Installation

1. Clone or download the repository to your local machine.
2. Install the required packages by running the following command:

`pip install -r requirements.txt`


## Usage

1. Obtain the Google Sheets API credentials JSON file from the Google Cloud Console.
2. Create an instance of the `GSheetReader` class by providing the path to the credentials JSON file:

      ```python
      from GSheetReader import GSheetReader

      gsheet_reader = GSheetReader('path/to/your/credentials.json')
      ```
      Replace `'path/to/your/credentials.json'` with the actual path to your credentials JSON file.

3. Use the `read_sheet()` method to read data from a specific Google Sheet:
      ```python
      df = gsheet_reader.read_sheet('Your Google Sheet ID', 'Your Sheet Name')
      ```
      Replace `'Your Google Sheet ID'` and `'Your Sheet Name'` with the appropriate values.

4. Save the DataFrame to a CSV file using the `save_to_csv()` method:
      ```python
      gsheet_reader.save_to_csv(df, 'output.csv')
      ```
5. Save the DataFrame to an Excel file using the `save_to_excel()` method:
      ```python
      gsheet_reader.save_to_excel(df, 'output.xlsx')
      ```
6. Make sure to adjust the paths and filenames according to your specific setup.