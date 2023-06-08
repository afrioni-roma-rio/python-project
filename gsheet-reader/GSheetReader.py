import gspread
import psycopg2
import pymysql
import yaml
from sqlalchemy import create_engine
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class GSheetReader:
    def __init__(self, cred_path):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_path, ['https://spreadsheets.google.com/feeds'])
        self.gc = gspread.authorize(self.credentials)
        
    def read_sheet(self, sheet_id, sheet_name):
        sheet = self.gc.open_by_key(sheet_id).worksheet(sheet_name)
        data = sheet.get_all_values(value_render_option='UNFORMATTED_VALUE')        
        filtered_data = [row for row in data if any(cell.strip() for cell in row if cell)]
        header_row = [col for col in filtered_data[0] if col.strip()]
        column_indexes = [i for i, col in enumerate(filtered_data[0]) if col.strip()]
        filtered_data = [[row[i] for i in column_indexes] for row in filtered_data[1:]]
        filtered_data = [row for row in filtered_data if any(cell.strip() for cell in row)]
        
        df = pd.DataFrame(filtered_data, columns=header_row)
        
        # Convert columns with date/time values to standard datetime format
        for col in df.columns:
            if df[col].dtype == 'object':  # Check if the column contains strings
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except ValueError:
                    pass
        return df
    
    def save_to_csv(self, df, filename):
        df.to_csv(filename, index=False)
        print("Data saved to CSV file:", filename)
        
    def save_to_excel(self, df, filename):
        df.to_excel(filename, index=False)
        print("Data saved to Excel file:", filename)

class GSheetToDatabase:
    def __init__(self, credentials_file):
        """
        Initializes the GSheetToDatabase instance.

        Args:
            credentials_file (str): The path to the YAML file containing the database credentials.
        """
        with open(credentials_file, 'r') as file:
            credentials = yaml.safe_load(file)
        
        self.username = credentials['username']
        self.password = credentials['password']
        self.db_name = credentials['db_name']
        self.db_type = credentials['db_type']
        self.engine = self._create_engine()
        
    def _create_engine(self):
        db_url = self._get_db_url()
        return create_engine(db_url)
    
    def _get_db_url(self):
        if self.db_type == 'postgresql':
            return f'postgresql://{self.username}:{self.password}@localhost/{self.db_name}'
        elif self.db_type == 'mysql':
            return f'mysql+pymysql://{self.username}:{self.password}@localhost/{self.db_name}'
        elif self.db_type == 'redshift':
            return f'redshift+psycopg2://{self.username}:{self.password}@localhost/{self.db_name}'
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def create_schema(self, schema_name):
        """
        Creates a new schema in the database if it doesn't exist.

        Args:
            schema_name (str): The name of the schema to create.

        Returns:
            None
        """
        query = f"CREATE SCHEMA IF NOT EXISTS {schema_name};"
        with self.engine.connect() as conn:
            conn.execute(query)
        print("Schema created:", schema_name)
    
    def save_to_database(self, df, schema_name, table_name, insert_type='replace'):
        """
        Saves the DataFrame to the specified database table.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            schema_name (str): The name of the database schema.
            table_name (str): The name of the database table.
            insert_type (str, optional): The type of insertion (e.g., 'replace', 'append', 'fail').
                Defaults to 'replace'.

        Returns:
            None
        """
        full_table_name = f"{schema_name}.{table_name}"

        df.to_sql(full_table_name, self.engine, if_exists=insert_type, index=False)
        print("Data saved to database table:", full_table_name)


