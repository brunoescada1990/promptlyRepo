import psycopg2
import json
import hashlib
import logging

from config import DB_CONFIG

class TransformAndInsertData:
    """
    This class is responsible for read table 'raw_patient' transform data and insert in table 'fhir_patient'.
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


    def generate_id(self, first_name, last_name, birth_date):
        """
        Generates a unique ID based on first_name, last_name, and birth_date.
        """

        unique_string = f"{first_name}{last_name}{birth_date}"
        unique_string = hashlib.md5(unique_string.encode()).hexdigest()

        return f"{first_name}_{last_name}_{birth_date}_{unique_string}"


    def get_raw_data(self, conn):
        """
        Get necessary data from the 'raw_patient' table.
        """

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT first_name, last_name, birth_date, gender, address, 
                           phone_number, email, marital_status, insurance_number, nationality
                    FROM raw_patient;
                """)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error to get data from raw_patient: {e}")
            raise
    

    def transform_data(self, raw_data):
        """
        Transforms raw patient data into the FHIR format.
        """
        transformed_data = []
        for patient in raw_data:
            first_name, last_name, birth_date, gender, address, phone, email, marital_status, insurance_number, nationality = patient

            fhir_id = self.generate_id(first_name, last_name, birth_date)
            full_name = f"{first_name} {last_name}"
            telecom = json.dumps({"phone": phone, "email": email})  # JSON válido

            transformed_data.append((fhir_id, full_name, birth_date, gender, address, telecom, marital_status, insurance_number, nationality))

        return transformed_data


    def insert_transformed_data(self, transformed_data):
        """
        Inserts transformed data into the 'fhir_patient' table.
        """
        try:
            conn = self.get_connection()
            insert_query = """
                INSERT INTO fhir_patient (id, full_name, birth_date, gender, address, telecom, marital_status, insurance_number, nationality)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """

            with conn.cursor() as cursor:
                cursor.executemany(insert_query, transformed_data)
                conn.commit()
                logging.info(f"Inserted {cursor.rowcount} records into fhir_patient.")
        except Exception as e:
            logging.error(f"Error inserting transformed data: {e}")
            raise
        finally:
            if conn:
                conn.close()


    def transform_and_insert(self):
        """
        Orchestrates the transformation and insertion process.
        """
        try:
            conn = self.get_connection()
            raw_data = self.get_raw_data(conn)
            transformed_data = self.transform_data(raw_data)
            self.insert_transformed_data(transformed_data)

        except Exception as e:
            logging.error(f"Error in transformation and insertion process: {e}")
            raise
    
if __name__ == "__main__":
    transformAndInsertData = TransformAndInsertData()
    transformAndInsertData.transform_and_insert() 