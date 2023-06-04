import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GSheetReader:
    def __init__(self, cred_path):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path, ['https://spreadsheets.google.com/feeds'])
        self.gc = gspread.authorize(self.credentials)
        
    def read_sheet(self, sheet_id, sheet_name):
        sheet = self.gc.open_by_key(sheet_id).worksheet(sheet_name)
        data = sheet.get_all_values()
        
        filtered_data = [row for row in data if any(cell.strip() for cell in row if cell)]
        header_row = [col for col in filtered_data[0] if col.strip()]
        column_indexes = [i for i, col in enumerate(filtered_data[0]) if col.strip()]
        filtered_data = [[row[i] for i in column_indexes] for row in filtered_data[1:]]
        filtered_data = [row for row in filtered_data if any(cell.strip() for cell in row)]
        
        df = pd.DataFrame(filtered_data, columns=header_row)
        return df
    
    def save_to_csv(self, df, filename):
        df.to_csv(filename, index=False)
        print("Data saved to CSV file:", filename)
        
    def save_to_excel(self, df, filename):
        df.to_excel(filename, index=False)
        print("Data saved to Excel file:", filename)
