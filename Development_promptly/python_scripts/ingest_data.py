import pandas as pd
import psycopg2
import logging
import argparse
import numpy as np

from psycopg2.extras import execute_values

from config import DB_CONFIG


class IngestData:
    """
    This class is responsible for uploading a CSV file and inserting data into the 'raw_patient' table.
    """

    # Logging configuration
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def get_connection(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise
    
    def handle_missing_data(self, df):
        """
        Handles missing data in the CSV by filling missing birth_date and address fields 
        and validate if blood_type column have a correct value.
        """

        valid_blood_types = ['A-', 'A+', 'O-', 'O+', 'B-', 'B+', 'AB-', 'AB+']

        df['birth_date'] = df['birth_date'].fillna('1000-01-01')
        df['address'] = df['address'].fillna('Not Provided')
        df['blood_type'] = df['blood_type'].apply(lambda x: x if x in valid_blood_types else np.nan)
        df['state'] = df['state'].apply(lambda x: None if pd.isnull(x) or (len(str(x)) > 2) else x)

        return df

    def insert_data(self, df):
        """
        Inserts the data into the 'raw_patient' table in the database using bulk insert for efficiency.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Prepare data for bulk insertion
        data_to_insert = [
            (
                row['first_name'], row['last_name'], row['birth_date'], row['gender'], row['address'],
                row['city'], row['state'], row['zip_code'], row['phone_number'], row['email'],
                row['emergency_contact_name'], row['emergency_contact_phone'], row['blood_type'],
                row['insurance_provider'], row['insurance_number'], row['marital_status'],
                row['preferred_language'], row['nationality'], row['allergies'], row['last_visit_date']
            )
            for _, row in df.iterrows()
        ]

        try:
            # Bulk insert using execute_values
            insert_query = """
                INSERT INTO raw_patient (first_name, last_name, birth_date, gender, address, city, state, zip_code, 
                                         phone_number, email, emergency_contact_name, emergency_contact_phone, 
                                         blood_type, insurance_provider, insurance_number, marital_status, 
                                         preferred_language, nationality, allergies, last_visit_date)
                VALUES %s;
            """
            execute_values(cursor, insert_query, data_to_insert)
            conn.commit()
        
        except Exception as e:
            logging.error(f"Error inserting data: {e}")
            conn.rollback()
        
        cursor.close()
        conn.close()


    def ingest_data(self, csv_file):
        """
        Reads a CSV file, handles missing data, and prints its contents.
        """
        logging.info(f"Data ingestion initiated from file: {csv_file}")

        try:
            df = pd.read_csv("source_files/" + csv_file)

            # Handle missing data by calling the instance method
            df = self.handle_missing_data(df)

            # Insert data:
            self.insert_data(df)

            logging.info(f"Data ingestion completed successfully.")
 
        except Exception as e:
            logging.error(f"Error in the ingestion process: {e}")
            
    
if __name__ == "__main__":
    # Configure argparse to accept a --file argument
    parser = argparse.ArgumentParser(description="Patient data ingestion into the database.")
    parser.add_argument("--file", required=True, help="Name CSV file to be ingested.")

    args = parser.parse_args()

    # Create an instance of the IngestData class and execute data ingestion
    ingestor = IngestData()
    ingestor.ingest_data(args.file)
